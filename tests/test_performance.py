import unittest
from unittest.mock import patch, MagicMock
import time
import queue
import json

# --- FIX: Import the logic from the new, correct location ---
from storyteller.engine import game_logic_thread 

# ... (imports)
class TestPerformance(unittest.TestCase):
    # ... (setUp method) ...
    @patch('storyteller.engine.client')
    def test_narrative_latency(self, mock_client):
        """performance: Ensures narrative response time is below the acceptable threshold."""
        # ... (test logic) ...

class TestPerformance(unittest.TestCase):
    """
    Validates the application's responsiveness.
    """
    # --- FIX: Patch the client where it is now used, in the engine ---
    @patch('storyteller.engine.client')
    def test_narrative_latency(self, mock_client):
        """
        Ensures narrative response time is below the acceptable threshold.
        """
        print("\n--- Running Performance (UI Latency) Test ---")
        
        mock_response_content = json.dumps({
            "narrative": "This is a test narrative.",
            "facts": [],
            "plot_completed": False
        })
        
        def delayed_response(*args, **kwargs):
            time.sleep(1) # Simulate 1 second of LLM processing time
            mock_choice = MagicMock()
            mock_choice.message.content = mock_response_content
            mock_response = MagicMock()
            mock_response.choices = [mock_choice]
            return mock_response

        mock_client.chat.completions.create.side_effect = delayed_response

        mock_memory_manager = MagicMock()
        mock_memory_manager.retrieve_context.return_value = ["Some context."]
        mock_memory_manager.get_active_plot_point.return_value = "A plot point."

        ui_queue = queue.Queue()
        user_input = "Test input"

        start_time = time.time()
        
        game_logic_thread(user_input, ui_queue, mock_memory_manager)
        
        try:
            message_type, content = ui_queue.get(timeout=3)
            end_time = time.time()
            latency = end_time - start_time
            
            self.assertLess(latency, 1.5)
            self.assertEqual(message_type, "dm_response")
            
            print(f"UI Latency: {latency:.2f}s")
            print("Performance Test: PASS")

        except queue.Empty:
            self.fail("The UI queue did not receive a response in time.")


if __name__ == '__main__':
    unittest.main()