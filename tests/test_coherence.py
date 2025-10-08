# tests/test_coherence.py

import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import json

class TestCoherence(unittest.TestCase):
    """
    Validates that the DM's narrative is contextually relevant.
    """
    def setUp(self):
        """Set up mocks for each test."""
        # Manually start the patcher to avoid class decorator issues
        self.patcher = patch('sentence_transformers.SentenceTransformer')
        MockSentenceTransformer = self.patcher.start()
        mock_embedding_model = MagicMock()
        mock_embedding_model.encode.return_value = np.random.rand(384)
        MockSentenceTransformer.return_value = mock_embedding_model

    def tearDown(self):
        """Stop the patcher after each test."""
        self.patcher.stop()

    @patch('storyteller.llm_client.client.chat.completions.create')
    def test_contextual_response(self, mock_llm_create):
        """coherence: Validates that the DM's narrative is contextually relevant to the player's action."""
        print("\n--- Running Coherence (Contextual Reply) Test ---")
        
        mock_narrative = "You speak to Boric in a calm voice, and he seems to relax slightly. 'Thank you,' he grumbles."
        mock_response_content = json.dumps({
            "narrative": mock_narrative,
            "facts": [{"subject": "Boric", "property": "state", "value": "relaxed slightly"}],
            "plot_completed": False
        })
        
        mock_choice = MagicMock()
        mock_choice.message.content = mock_response_content
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_llm_create.return_value = mock_response

        response_data = json.loads(mock_llm_create(messages=[], model="").choices[0].message.content)
        final_narrative = response_data.get("narrative")

        self.assertIn("calm", final_narrative.lower())
        self.assertIn("relax", final_narrative.lower())
        print("Coherence Test: PASS")

if __name__ == '__main__':
    unittest.main()