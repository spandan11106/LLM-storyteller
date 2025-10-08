import time
import re
from .rag_manager import RAGManager
from . import config


class MemoryManager:
    """High-level MemoryManager that composes a RAGManager plus simple plot-point state.

    This keeps the external API stable for the rest of the codebase while moving RAG logic
    into `storyteller/rag_manager.py`.
    """

    def __init__(self):
        print("Initializing Final Production Memory Manager (v3.0)...")
        self.rag = RAGManager()
        # Expose a `graph` attribute for backward compatibility with older callers
        # (many scripts expect memory.graph to be a networkx graph)
        self.graph = self.rag.graph
        self.plot_points = {p: "inactive" for p in config.PLOT_POINTS}
        if config.PLOT_POINTS:
            self.plot_points[config.PLOT_POINTS[0]] = "active"
        # internal counter for turn ids to avoid relying on chroma internals
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
        """Compatibility wrapper: create a turn and ensure deterministic facts from the turn/user_input are stored."""
        tid = self.add_turn_to_log(turn_text)
        # Also attempt to extract facts from user_input and the full turn_text
        try:
            if user_input:
                facts = self.rag.extract_facts(user_input)
                if facts:
                    self.rag.add_facts(facts, tid)
            # also run extractor on the combined turn_text (rag.add_turn already calls extractor on turn_text)
        except Exception:
            pass
        return tid

    def retrieve_memories(self, query, n_results=3):
        """Return a list of retrieved turn_text strings for compatibility with older tests."""
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

    def _is_plot_point_complete(self, turn_text, plot_point_name):
        # Keep a conservative heuristic here (delegating to rag.extract_facts might be possible later)
        if not turn_text or not plot_point_name:
            return False
        keywords = [w.lower() for w in re.sub(r'[_\-]+', ' ', plot_point_name).split()]
        text = turn_text.lower()
        matches = sum(1 for k in keywords if k and k in text)
        return matches >= 1

    def _complete_plot_point(self, point_name):
        return self.update_plot_point(point_name)