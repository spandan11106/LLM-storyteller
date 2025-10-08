import time
import re
from .rag_manager import RAGManager
from . import config


class MemoryManager:
    """High-level MemoryManager that composes a RAGManager plus simple plot-point state."""

    def __init__(self):
        print("Initializing Final Production Memory Manager (v3.0)...")
        self.rag = RAGManager()
        self.graph = self.rag.graph
        
        # --- FIX: Call the function to initialize NPCs ---
        self._initialize_npcs()

        self.plot_points = {p: "inactive" for p in config.PLOT_POINTS}
        if config.PLOT_POINTS:
            self.plot_points[config.PLOT_POINTS[0]] = "active"
        self._turn_counter = 0
        print("Graph Manager Initialized.")

    def add_turn_to_log(self, turn_text):
        """Adds a turn and returns a stable turn id (int)."""
        self._turn_counter += 1
        tid = self._turn_counter
        self.rag.add_turn(tid, turn_text)
        return tid
    
    def _initialize_npcs(self):
        """Adds the initial NPC data to the knowledge graph."""
        for npc_name, attributes in config.INITIAL_NPC_STATES.items():
            self.graph.add_node(npc_name, **attributes)
        print("Initial NPC states loaded into graph.")

    def save_memory(self, turn_text, user_input=None):
        """Compatibility wrapper for older tests."""
        tid = self.add_turn_to_log(turn_text)
        try:
            if user_input:
                # Use the robust LLM extractor
                facts = self.rag.extract_facts_llm(user_input)
                if facts:
                    self.rag.add_facts(facts, tid)
        except Exception:
            pass
        return tid

    def retrieve_memories(self, query, n_results=3):
        """Compatibility wrapper for older tests."""
        return self.rag.retrieve(query, n_results=n_results)

    def update_graph_with_facts(self, facts, turn_id):
        self.rag.add_facts(facts, turn_id)

    def update_plot_point(self, point_name):
        print(f"[PLOT] Completed: {point_name}")
        self.plot_points[point_name] = "completed"
        current_index = config.PLOT_POINTS.index(point_name)
        if current_index + 1 < len(config.PLOT_POINTS):
            next_point = config.PLOT_POINTS[current_index + 1]
            self.plot_points[next_point] = "active"
            print(f"[PLOT] New Active Point: {next_point}")
        else:
            print("[PLOT] Adventure Completed!")

    def retrieve_context(self, query):
        return self.rag.retrieve(query, n_results=5)

    def get_active_plot_point(self):
        for point, status in self.plot_points.items():
            if status == "active":
                return point
        return None