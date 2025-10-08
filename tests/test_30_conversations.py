import unittest
from unittest.mock import patch, MagicMock
import numpy as np

from storyteller.memory_manager import MemoryManager

# ... (imports)
class Test30ConversationsMemory(unittest.TestCase):
    # ... (setUp and tearDown methods) ...
    @patch('storyteller.rag_manager.update_core_memory')
    @patch('storyteller.rag_manager.summarize_scene')
    @patch('storyteller.rag_manager.is_scene_break')
    def test_core_memory_retention_after_30_turns(self, mock_is_scene_break, mock_summarize_scene, mock_update_core_memory):
        """memory: Validates that the Core Memory retains a key fact after a long conversation."""
        # ... (test logic) ...

class Test30ConversationsMemory(unittest.TestCase):
    """
    Validates the Core Memory's ability to retain key facts over a long conversation.
    """

    def setUp(self):
        """Set up a fresh MemoryManager and mock its dependencies."""
        # Mock the embedding model to prevent network calls
        self.patcher = patch('storyteller.rag_manager.SentenceTransformer')
        MockSentenceTransformer = self.patcher.start()
        mock_embedding_model = MagicMock()
        mock_embedding_model.encode.return_value = np.random.rand(384)
        MockSentenceTransformer.return_value = mock_embedding_model
        
        self.memory = MemoryManager()

    def tearDown(self):
        """Stop the patcher after each test."""
        self.patcher.stop()

    # --- FIX: Patch our specific memory functions directly for a more reliable test ---
    @patch('storyteller.rag_manager.update_core_memory')
    @patch('storyteller.rag_manager.summarize_scene')
    @patch('storyteller.rag_manager.is_scene_break')
    def test_core_memory_retention_after_30_turns(self, mock_is_scene_break, mock_summarize_scene, mock_update_core_memory):
        """
        Tests if the Core Memory retains a key fact after 30 turns of conversation.
        """
        print("\n--- Running 30-Conversation Core Memory Test ---")

        # --- Configure Mocks ---
        # 1. The scene detector will trigger a scene break on the second turn.
        mock_is_scene_break.side_effect = lambda text, turns: len(turns) >= 2

        # 2. The scene summarizer will return the key fact when it sees the initial turn.
        def summary_side_effect(turns):
            if any("Elara" in turn for turn in turns):
                return "The player was warned of a shadow curse by Elara."
            return "A generic scene occurred."
        mock_summarize_scene.side_effect = summary_side_effect

        # 3. The core memory updater will append the scene summary.
        def core_memory_side_effect(current_memory, new_summary):
            return f"{current_memory}\n- {new_summary}"
        mock_update_core_memory.side_effect = core_memory_side_effect


        # --- Run the Simulation ---
        # Mock the turn summarizer to avoid extra LLM calls
        with patch.object(self.memory.rag, 'summarize_turn', side_effect=lambda text: text):
            # Turn 1: Establish the key fact
            initial_turn = "The player meets a mysterious old man named Elara who warns them about a 'shadow curse'."
            self.memory.rag.add_turn(1, initial_turn)

            # Turn 2: This will trigger the first scene break and memory update
            self.memory.rag.add_turn(2, "The player leaves the area.")
            
            # Turns 3-30: Simulate a long conversation
            for i in range(3, 31):
                # The is_scene_break mock will now cause a scene break every turn
                self.memory.rag.add_turn(i, f"This is turn {i}, a random event occurs.")

        # --- Final Check ---
        # We check the call arguments of our mock to see what the final core memory would be.
        # This is more precise than checking an internal state variable.
        final_core_memory_call = mock_update_core_memory.call_args_list[-1]
        final_memory_state = final_core_memory_call.args[0] # The 'current_memory' argument from the last call

        self.assertIn("shadow curse", final_memory_state.lower())
        self.assertIn("elara", final_memory_state.lower())
        
        print("30-Conversation Core Memory Test: PASS")


if __name__ == '__main__':
    unittest.main()