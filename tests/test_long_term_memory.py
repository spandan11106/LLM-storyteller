# tests/test_long_term_memory.py

import unittest
from unittest.mock import patch, MagicMock
import numpy as np

from storyteller.memory_manager import MemoryManager

# ... (imports)
class TestLongTermMemory(unittest.TestCase):
    # ... (setUp and tearDown methods) ...
    @patch('storyteller.llm_client.client.chat.completions.create')
    def test_three_tier_retrieval(self, mock_llm_create):
        """memory: Validates that a query retrieves info from all three memory tiers (Core, Scene, Turn)."""
        # ... (test logic) ...

class TestLongTermMemory(unittest.TestCase):
    """
    Validates the three-tier memory architecture.
    """

    def setUp(self):
        """Set up a fresh MemoryManager and start mocks for each test."""
        self.patcher = patch('storyteller.rag_manager.SentenceTransformer')
        MockSentenceTransformer = self.patcher.start()

        mock_embedding_model = MagicMock()
        mock_embedding_model.encode.return_value = np.random.rand(384)
        MockSentenceTransformer.return_value = mock_embedding_model
        
        self.memory = MemoryManager()

    def tearDown(self):
        """Stop the patcher after each test to clean up."""
        self.patcher.stop()

    @patch('storyteller.llm_client.client.chat.completions.create')
    def test_three_tier_retrieval(self, mock_llm_create):
        """
        Tests if a query retrieves information from all three memory tiers.
        """
        print("\n--- Running Three-Tier Memory Retrieval Test ---")

        # --- Setup the Memory Tiers ---
        # L3 - Core Memory
        self.memory.rag.core_memory = "The main quest is to find the Sunstone."
        
        # L2 - Scene Memory (mock the vector DB result)
        mock_scene_summary = "In a past scene, the player learned the Sunstone is in the Crystal Caves."
        
        # L1 - Turn Memory (mock the vector DB result)
        mock_recent_turn = "The player is currently talking to a guard near the caves."

        # Mock the database queries to return our test data
        with patch.object(self.memory.rag.turn_collection, 'query', return_value={'metadatas': [[{'turn_text': mock_recent_turn}]]}):
            with patch.object(self.memory.rag.scene_collection, 'query', return_value={'documents': [[mock_scene_summary]]}):
                
                # --- Test the Retrieval ---
                retrieved_memories = self.memory.retrieve_context("Where is the Sunstone?")
                retrieved_text = " ".join(retrieved_memories)

                # --- Verify ---
                # Check that information from all three tiers is present
                self.assertIn("main quest", retrieved_text.lower())      # From Core Memory
                self.assertIn("crystal caves", retrieved_text.lower()) # From Scene Memory
                self.assertIn("guard", retrieved_text.lower())          # From Turn Memory
                
                print("Three-Tier Memory Retrieval Test: PASS")


if __name__ == '__main__':
    unittest.main()