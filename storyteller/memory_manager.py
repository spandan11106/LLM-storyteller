# storyteller/memory_manager.py
import json
import chromadb
from sentence_transformers import SentenceTransformer
from .llm_client import client  # Use relative import
from . import config           # Use relative import

class MemoryManager:
    """Handles all memory operations, including a simple knowledge graph."""
    
    def __init__(self):
        print("Initializing Memory Manager...")
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        db_client = chromadb.Client()
        self.collection = db_client.get_or_create_collection(name=config.DB_COLLECTION_NAME)
        self.turn_count = 0
        self.knowledge_graph = {}
        print("Memory Manager Initialized.")

    def _get_summary(self, text):
        """Generates a one-sentence summary of a turn for memory storage."""
        summary_prompt = (
            f"Summarize the following RPG turn exchange in a single, concise sentence:\n\n{text}"
        )
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": summary_prompt}], model=config.LLM_MODEL
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating summary: {e}")
            return ""

    def _extract_and_update_facts(self, text, user_input):
        """Extracts facts and uses keywords to update quest statuses for reliability."""
        
        quests_in_graph = self.knowledge_graph.get("Quests", {})
        if quests_in_graph:
            for quest_name, status in quests_in_graph.items():
                if status == "active" and "summons" in quest_name.lower() and "answer" in user_input.lower():
                    self.knowledge_graph["Quests"][quest_name] = "completed"
                    print(f"[📜 Quest Updated: '{quest_name}' status set to completed]")

        fact_extraction_prompt = f"""
Analyze the following game text to extract structured data.
Respond with a single JSON object containing a "facts" key.

1.  **facts**: A list of objects.
    - Relationships: {{"subject": "entity", "relation": "verb", "object": "entity"}}
    - Properties: {{"entity": "entity", "property": "description"}}
    - NPC Mood Changes: If an NPC's disposition towards the player changes (e.g., becomes friendly, annoyed), extract it as: {{"entity": "NPC_Name", "property": "disposition", "value": "mood"}}

If no facts are found, return an empty list.

**Game Text:**
---
{text}
---
"""
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": fact_extraction_prompt}],
                model=config.LLM_MODEL,
                response_format={"type": "json_object"},
            )
            data = json.loads(response.choices[0].message.content)
            
            facts = data.get('facts', [])
            if isinstance(facts, list):
                print(f"\n[🧠 Extracted Facts: {facts}]")
                for fact in facts:
                    if isinstance(fact, dict):
                        entity_name = fact.get('subject') or fact.get('entity')
                        if not entity_name: continue
                        if entity_name not in self.knowledge_graph:
                            self.knowledge_graph[entity_name] = {'properties': [], 'relationships': []}
                        if 'subject' in fact: self.knowledge_graph[entity_name]['relationships'].append(fact)
                        elif 'entity' in fact: self.knowledge_graph[entity_name]['properties'].append(fact)
        except Exception as e:
            print(f"Error extracting facts: {e}")

    def save_memory(self, turn_text, user_input):
        """Saves both episodic and semantic (fact-based) memory."""
        self.turn_count += 1
        summary = self._get_summary(turn_text)
        if summary:
            print(f"\n[📝 Saving memory: '{summary}']")
            embedding = self.embedding_model.encode(summary).tolist()
            self.collection.add(
                embeddings=[embedding], documents=[summary], ids=[f"turn_{self.turn_count}"]
            )
        self._extract_and_update_facts(turn_text, user_input)

    def retrieve_memories(self, query, n_results=3):
        """Retrieves the most relevant memories for a given query."""
        if self.collection.count() == 0: return []
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, self.collection.count())
        )
        return results['documents'][0]
    
    def get_facts_about(self, entity_name):
        """Retrieves all known facts about a specific entity."""
        return self.knowledge_graph.get(entity_name, None)