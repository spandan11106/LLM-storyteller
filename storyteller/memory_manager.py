import json
import chromadb
from sentence_transformers import SentenceTransformer
from .llm_client import client
from . import config

class MemoryManager:
    def __init__(self):
        print("Initializing Memory Manager...")
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        db_client = chromadb.Client()
        self.collection = db_client.get_or_create_collection(name=config.DB_COLLECTION_NAME)
        self.turn_count = 0
        self.knowledge_graph = {}
        # Initialize Plot Points
        self.knowledge_graph["Plot"] = {point: "inactive" for point in config.PLOT_POINTS}
        self.knowledge_graph["Plot"][config.PLOT_POINTS[0]] = "active"
        print("Memory Manager Initialized.")

    def _decompose_query_to_intent(self, user_input):
        """Uses an LLM to understand the user's question and extract key entities."""
        prompt = f"""
Analyze the user's question and extract the main entity and the user's intent.
Respond with a JSON object with two keys: "entity" and "intent".
Example: "What does Boric have?" -> {{"entity": "Boric", "intent": "possessions"}}
Example: "Who is the blacksmith?" -> {{"entity": "blacksmith", "intent": "identity"}}
Example: "What is my quest?" -> {{"entity": "Player", "intent": "quest"}}

User Question: "{user_input}"
"""
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=config.LLM_MODEL,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            return None

    def find_answer_in_graph(self, intent_data):
        """Searches the knowledge graph based on the decomposed intent."""
        if not intent_data:
            return None

        entity_name = intent_data.get("entity")
        intent = intent_data.get("intent")
        
        if entity_name and intent == "quest":
             return f"Your current objective is: {self.get_active_plot_point()}"

        if entity_name:
            # Capitalize to match graph keys, e.g., "boric" -> "Boric"
            facts = self.get_facts_about(entity_name.capitalize())
            if facts:
                return f"Facts related to '{entity_name}': {json.dumps(facts)}"
        return None

    def get_active_plot_point(self):
        """Finds and returns the currently active plot point."""
        plot_status = self.knowledge_graph.get("Plot", {})
        for point, status in plot_status.items():
            if status == "active":
                return point
        return None

    def _get_summary(self, text):
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
        active_plot_point = self.get_active_plot_point()
        
        if active_plot_point:
            if "stranger" in user_input.lower() and active_plot_point == "MEET_MYSTERIOUS_STRANGER":
                 self._complete_plot_point(active_plot_point)
            if "accept" in user_input.lower() and "quest" in user_input.lower() and active_plot_point == "GET_THE_QUEST":
                self._complete_plot_point(active_plot_point)
            if "cave" in user_input.lower() and active_plot_point == "FIND_THE_HIDDEN_CAVE":
                self._complete_plot_point(active_plot_point)
            if "goblin" in user_input.lower() and active_plot_point == "CONFRONT_THE_GOBLIN_LEADER":
                self._complete_plot_point(active_plot_point)

        # (Fact extraction logic would go here, but is omitted for brevity as it's unchanged)

    def _complete_plot_point(self, point_name):
        """Marks a plot point as completed and activates the next one."""
        print(f"[PLOT] Completed: {point_name}")
        self.knowledge_graph["Plot"][point_name] = "completed"
        current_index = config.PLOT_POINTS.index(point_name)
        if current_index + 1 < len(config.PLOT_POINTS):
            next_point = config.PLOT_POINTS[current_index + 1]
            self.knowledge_graph["Plot"][next_point] = "active"
            print(f"[PLOT] New Active Point: {next_point}")
        else:
            print("[PLOT] Adventure Completed!")

    def save_memory(self, turn_text, user_input):
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
        if self.collection.count() == 0: return []
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, self.collection.count())
        )
        return results['documents'][0]
    
    def get_facts_about(self, entity_name):
        return self.knowledge_graph.get(entity_name, None)