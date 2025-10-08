import time
import re
import chromadb
import networkx as nx
from sentence_transformers import SentenceTransformer
from .llm_client import client
from . import config


class RAGManager:
    """A small RAG manager: embeddings (SentenceTransformers) + Chroma vector store + NetworkX graph.

    Responsibilities:
    - store embeddings + documents (turn summaries) in Chroma
    - provide retrieve(query) combining vector search and graph node matches
    - expose graph insertion helpers for facts
    - provide a lightweight, deterministic fact extractor fallback
    """

    def __init__(self, collection_name=None):
        self.collection_name = collection_name or config.DB_COLLECTION_NAME
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        self.graph = nx.DiGraph()

    def summarize_turn(self, turn_text):
        """Try an LLM summary, fall back to a deterministic short snippet."""
        prompt = f"Summarize this turn in one short sentence:\n\n{turn_text}"
        try:
            resp = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=config.LLM_MODEL)
            summary = resp.choices[0].message.content
            return summary.encode('utf-8', errors='replace').decode('utf-8')
        except Exception:
            # deterministic fallback
            return (turn_text.strip().replace('\n', ' ')[:200]).strip()

    def add_turn(self, turn_id, turn_text, summary=None):
        """Adds a turn to the vector store. turn_id is a stable id (int or str)."""
        if summary is None:
            summary = self.summarize_turn(turn_text)
        emb = self.embedding_model.encode(summary).tolist()
        # ensure id is str
        _id = str(turn_id)
        try:
            self.collection.add(embeddings=[emb], documents=[summary], ids=[_id], metadatas=[{"turn_text": turn_text}])
        except Exception:
            # chroma may raise if id exists; try delete+add
            try:
                self.collection.delete(ids=[_id])
            except Exception:
                pass
            self.collection.add(embeddings=[emb], documents=[summary], ids=[_id], metadatas=[{"turn_text": turn_text}])
        # Auto-extract deterministic facts and add them to the graph (non-blocking)
        try:
            facts = self.extract_facts(turn_text)
            if facts:
                self.add_facts(facts, turn_id)
        except Exception:
            # never fail storage because of extractor errors
            pass

    def retrieve(self, query, n_results=5):
        """Retrieve relevant turn_texts for a query using vector search + graph signals."""
        vector_docs = self._vector_search(query, n_results)
        graph_docs = self._graph_search(query)

        # combine, prefer graph_docs first then vector_docs (dedupe)
        seen = set()
        combined = []
        for doc in graph_docs + vector_docs:
            if doc and doc not in seen:
                combined.append(doc)
                seen.add(doc)
            if len(combined) >= n_results:
                break
        return combined

    def _vector_search(self, query, n_results):
        """Performs a vector search in ChromaDB."""
        q_emb = self.embedding_model.encode(query).tolist()
        if self.collection.count() == 0:
            return []
        
        results = self.collection.query(
            query_embeddings=[q_emb], 
            n_results=min(n_results, self.collection.count())
        )
        
        vector_docs = []
        try:
            docs = results.get('documents', [[]])[0]
            metas = results.get('metadatas', [[]])[0]
            for d, m in zip(docs, metas):
                vector_docs.append(m.get('turn_text', d))
        except Exception:
            pass
        return vector_docs

    def _graph_search(self, query):
        """Searches the knowledge graph for matching nodes."""
        q_words = set(re.sub(r"[^\w\s]", "", query).lower().split())
        matched_turn_ids = set()
        for node, data in self.graph.nodes(data=True):
            node_text = str(node).lower()
            if any(w in node_text for w in q_words):
                sid = data.get('source_id')
                if sid is not None:
                    matched_turn_ids.add(int(sid))
            
            for k, v in data.items():
                try:
                    if isinstance(v, str) and any(w in v.lower() for w in q_words):
                        sid = data.get('source_id')
                        if sid is not None:
                            matched_turn_ids.add(int(sid))
                except Exception:
                    continue

        graph_docs = []
        for tid in sorted(matched_turn_ids):
            try:
                res = self.collection.get(ids=[str(tid)])
                metas = res.get('metadatas', [[]])[0]
                if metas and isinstance(metas[0], dict) and 'turn_text' in metas[0]:
                    graph_docs.append(metas[0]['turn_text'])
                else:
                    docs = res.get('documents', [[]])[0]
                    if docs:
                        graph_docs.append(docs[0])
            except Exception:
                continue
        return graph_docs

    def extract_facts(self, text):
        """Deterministic, small extractor to produce facts usable for the graph.
        Returns a list of fact dicts matching the `update_graph_with_facts` format.
        """
        facts = []
        if not text:
            return facts

        # 1) transfer pattern: 'Boric gives me a RUSTY key.' or 'Boric gave me a RUSTY key.'
        m = re.search(r"(?P<entity>[A-Z][A-Za-z0-9_'\-]+).*?(?:gives|gave|hands) (?:me|the player) a (?P<item>[A-Za-z0-9 _-]+)\.?", text)
        if m:
            subj = m.group('entity').split()[0].capitalize()
            obj = m.group('item').strip()
            facts.append({'subject': subj, 'relation': 'gave', 'object': obj})

        # 2) explicit password sharing pattern: "I tell Boric the password 'Ironscale'" or similar
        m2 = re.search(r"(?:tell|told|whisper)\b.*?\b(?P<recipient>[A-Z][A-Za-z0-9_'\-]+).*?password\s*(?:is|:)?\s*[\"]?(?P<pw>[A-Za-z0-9_\- ]{2,80})[\"]?", text, flags=re.IGNORECASE)
        if m2:
            recipient = m2.group('recipient').split()[0].capitalize()
            pw = m2.group('pw').strip()
            # store as recipient received_password, and also as a player-shared-password fact
            facts.append({'entity': recipient, 'property': 'received_password', 'value': pw})
            facts.append({'subject': 'Player', 'relation': 'told_password_to', 'object': pw})

        # 3) simple attribute pattern: 'X is Y' or 'X was Y'
        for m in re.finditer(r"(?P<entity>[A-Z][A-Za-z0-9_'\-]+) (?:is|was|are) (?P<attr>[A-Za-z0-9 _-]+)\.?", text):
            subj = m.group('entity').split()[0].capitalize()
            val = m.group('attr').strip()
            facts.append({'entity': subj, 'property': 'desc', 'value': val})

        return facts

    def add_facts(self, facts, turn_id):
        """Add facts to the internal graph. Facts are list of dicts.
        Accepts both {'subject','relation','object'} and {'entity','property','value'} formats.
        """
        if not facts: return
        for fact in facts:
            if 'subject' in fact and 'relation' in fact and 'object' in fact:
                subj = str(fact['subject']).capitalize()
                rel = str(fact['relation'])
                obj = str(fact['object']).capitalize()
                self.graph.add_node(subj, source_id=turn_id)
                self.graph.add_node(obj, source_id=turn_id)
                self.graph.add_edge(subj, obj, label=rel)
            elif 'entity' in fact and 'property' in fact and 'value' in fact:
                ent = str(fact['entity']).capitalize()
                prop = str(fact['property'])
                val = str(fact.get('value', 'True'))
                if not self.graph.has_node(ent):
                    self.graph.add_node(ent, source_id=turn_id)
                self.graph.nodes[ent][prop] = val