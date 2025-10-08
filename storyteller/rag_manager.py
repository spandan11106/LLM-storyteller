# storyteller/rag_manager.py

import time
import re
import json
import chromadb
import networkx as nx
from sentence_transformers import SentenceTransformer

from .llm_client import client
from . import config
from .memory.summarizer import summarize_scene
from .memory.scene_detector import is_scene_break
from .memory.core_memory import update_core_memory
from .utils import sanitize_data_for_graph


class RAGManager:
    """
    Manages a three-tier memory system for robust, long-term recall.
    """

    def __init__(self, collection_name=None):
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        self.db_client = chromadb.Client()
        
        self.turn_collection = self.db_client.get_or_create_collection(name=config.DB_COLLECTION_NAME)
        self.scene_collection = self.db_client.get_or_create_collection(name=config.SCENE_COLLECTION_NAME)
        
        self.graph = nx.DiGraph()
        
        self.current_scene_turns = []
        self._scene_counter = 0
        
        self.core_memory = "The story has just begun."

    def add_turn(self, turn_id, turn_text, summary=None):
        """Adds a turn to short-term memory and checks for a scene break."""
        if summary is None:
            summary = self.summarize_turn(turn_text)
        
        emb = self.embedding_model.encode(summary).tolist()
        _id = str(turn_id)
        
        self.turn_collection.add(
            embeddings=[emb], documents=[summary], ids=[_id], metadatas=[{"turn_text": turn_text}]
        )
        
        if is_scene_break(turn_text, self.current_scene_turns):
            self.archive_scene()

        self.current_scene_turns.append(turn_text)

        try:
            facts = self.extract_facts_llm(turn_text)
            if facts:
                self.add_facts(facts, turn_id)
        except Exception:
            pass

    def archive_scene(self):
        """Summarizes the scene, archives it, and updates core memory."""
        if not self.current_scene_turns:
            return

        print("[Memory] Scene break detected. Archiving scene...")
        
        scene_summary = summarize_scene(self.current_scene_turns)
        
        if scene_summary:
            self._scene_counter += 1
            scene_id = f"scene_{self._scene_counter}"
            emb = self.embedding_model.encode(scene_summary).tolist()
            
            self.scene_collection.add(
                embeddings=[emb], documents=[scene_summary], ids=[scene_id]
            )
            print(f"[Memory] Scene '{scene_id}' archived: {scene_summary}")

            self.core_memory = update_core_memory(self.core_memory, scene_summary)
            print(f"[Memory] Core Memory updated.")

        self.current_scene_turns = []


    def retrieve(self, query, n_results=5):
        """Retrieve from all three tiers of memory: Core, Scenes, and Turns."""
        q_emb = self.embedding_model.encode(query).tolist()
        
        turn_texts = []
        scene_docs = []

        # --- FIX: Check if collections have documents before querying ---
        # L1 (Turns): Get the most recent, relevant turns.
        if self.turn_collection.count() > 0:
            n_turn_results = min(2, self.turn_collection.count())
            turn_results = self.turn_collection.query(
                query_embeddings=[q_emb], n_results=n_turn_results
            )
            turn_texts = [meta.get('turn_text', '') for meta in turn_results.get('metadatas', [[{}]])[0]]

        # L2 (Scenes): Get the most relevant scene summaries.
        if self.scene_collection.count() > 0:
            n_scene_results = min(2, self.scene_collection.count())
            scene_results = self.scene_collection.query(
                query_embeddings=[q_emb], n_results=n_scene_results
            )
            scene_docs = scene_results.get('documents', [[]])[0]

        # L3 (Core Memory): Always include the core memory for foundational context.
        final_docs = [self.core_memory] + scene_docs + turn_texts
        
        # Deduplicate and finalize
        seen = set()
        unique_docs = [doc for doc in final_docs if doc and not (doc in seen or seen.add(doc))]
        
        return unique_docs[:n_results]

    # ... (the rest of your RAGManager methods remain the same) ...
    def summarize_turn(self, turn_text):
        """Try an LLM summary, fall back to a deterministic short snippet."""
        prompt = f"Summarize this turn in one short sentence:\n\n{turn_text}"
        try:
            resp = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=config.LLM_MODEL)
            summary = resp.choices[0].message.content
            return summary.encode('utf-8', errors='replace').decode('utf-8')
        except Exception:
            return (turn_text.strip().replace('\n', ' ')[:200]).strip()

    def extract_facts_llm(self, text):
        """Uses an LLM to extract facts, with a regex fallback."""
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": config.FACT_EXTRACTION_PROMPT},
                    {"role": "user", "content": text}
                ],
                model=config.LLM_MODEL,
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            facts = data.get("facts", [])

            # --- FIX: Sanitize the facts immediately after receiving them ---
            sanitized_facts = sanitize_data_for_graph(facts)
            return sanitized_facts
            
        except Exception:
            return self.extract_facts_regex(text)

# (The add_facts method no longer needs the try...except block, as the data is now guaranteed to be clean)
    def add_facts(self, facts, turn_id):
        """Add facts to the internal graph. Assumes facts have been sanitized."""
        if not facts: return
        for fact in facts:
            if 'subject' in fact and 'relation' in fact and 'object' in fact:
                subj = str(fact['subject']).capitalize()
                obj = str(fact['object']).capitalize()
                rel = str(fact['relation'])

                if not self.graph.has_node(subj): self.graph.add_node(subj, source_id=turn_id)
                if not self.graph.has_node(obj): self.graph.add_node(obj, source_id=turn_id)
                self.graph.add_edge(subj, obj, label=rel)

            elif 'entity' in fact:
                ent = str(fact['entity']).capitalize()
                if not self.graph.has_node(ent): self.graph.add_node(ent, source_id=turn_id)

                if 'entity_type' in fact:
                    entity_type = 'npc' if str(fact['entity_type']) == 'person' else str(fact['entity_type'])
                    self.graph.nodes[ent]['type'] = entity_type
                
                if 'property' in fact and 'value' in fact:
                    prop = str(fact['property'])
                    val = str(fact.get('value', 'True'))
                    self.graph.nodes[ent][prop] = val