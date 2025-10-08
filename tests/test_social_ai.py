# tests/test_social_ai.py

import unittest
from unittest.mock import patch, MagicMock
import networkx as nx

from storyteller import npc_manager
from storyteller.memory_manager import MemoryManager

# ... (imports)
class TestSocialAI(unittest.TestCase):
    # ... (setUp method) ...
    @patch('storyteller.npc_manager.analyze_player_tone')
    def test_polite_interaction(self, mock_analyze_tone):
        """social: Tests if a polite tone correctly increases an NPC's relationship score."""
        # ... (test logic) ...

    @patch('storyteller.npc_manager.analyze_player_tone')
    def test_rude_interaction(self, mock_analyze_tone):
        """social: Tests if a rude tone correctly decreases an NPC's score and changes their emotion."""
        # ... (test logic) ...

class TestSocialAI(unittest.TestCase):
    """
    Validates the Dynamic NPC Relationship & Emotion System.
    """

    def setUp(self):
        """Set up a fresh memory manager with a mock graph for each test."""
        # We use a mock MemoryManager to isolate the NPC logic
        self.mock_memory = MagicMock()
        self.mock_memory.rag.graph = nx.DiGraph()
        # Add a test NPC to the graph
        self.mock_memory.rag.graph.add_node("Boric", type="npc", relationship_score=0, emotional_state="Neutral")

    @patch('storyteller.npc_manager.analyze_player_tone')
    def test_polite_interaction(self, mock_analyze_tone):
        """Tests if a polite tone correctly increases the relationship score."""
        print("\n--- Running Social AI (Polite Tone) Test ---")
        
        # 1. Arrange: Mock the tone analysis to always return 'Polite'
        mock_analyze_tone.return_value = "Polite"

        # 2. Act: Simulate a polite interaction with Boric
        user_input = "Hello Boric, that's a fine hammer you have."
        tone = npc_manager.analyze_player_tone(user_input)
        npc_manager.update_npc_state(self.mock_memory.rag.graph, "Boric", tone)

        # 3. Assert: Check if the score and emotion were updated correctly
        boric_state = self.mock_memory.rag.graph.nodes["Boric"]
        self.assertEqual(boric_state['relationship_score'], 5)
        self.assertEqual(boric_state['emotional_state'], "Neutral") # Score isn't high enough to change emotion yet
        print("Polite Tone Test: PASS")

    @patch('storyteller.npc_manager.analyze_player_tone')
    def test_rude_interaction(self, mock_analyze_tone):
        """Tests if a rude tone correctly decreases the score and changes emotion."""
        print("\n--- Running Social AI (Rude Tone) Test ---")

        # 1. Arrange: Mock the tone analysis to always return 'Rude'
        mock_analyze_tone.return_value = "Rude"
        
        # 2. Act: Simulate two rude interactions
        npc_manager.update_npc_state(self.mock_memory.rag.graph, "Boric", "Rude") # Score becomes -10
        npc_manager.update_npc_state(self.mock_memory.rag.graph, "Boric", "Rude") # Score becomes -20
        
        # 3. Assert: Check the final state
        boric_state = self.mock_memory.rag.graph.nodes["Boric"]
        self.assertEqual(boric_state['relationship_score'], -20)
        self.assertEqual(boric_state['emotional_state'], "Annoyed")
        print("Rude Tone Test: PASS")


if __name__ == '__main__':
    unittest.main()