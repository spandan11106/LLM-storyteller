import unittest
from unittest.mock import patch
import json
from storyteller.memory_manager import MemoryManager

class GraphMemoryTest(unittest.TestCase):
    """
    A dedicated test suite to validate the 'Indexed Narrative' graph database.
    """
    def setUp(self):
        """Set up a fresh MemoryManager for each test."""
        self.memory = MemoryManager()
        print("\n--- Running Indexed Narrative Graph Test ---")

    @patch('storyteller.memory_manager.client')
    def test_indexed_narrative_storage(self, mock_client):
        """Tests if facts are added with correct pointers to the narrative log."""
        mock_ai_response = {"facts": [{"subject": "Boric", "relation": "gives", "object": "Key"}]}
        mock_client.chat.completions.create.return_value.choices[0].message.content = json.dumps(mock_ai_response)

        self.memory.save_memory("The room is empty.", "test 1")
        self.memory.save_memory("Boric gives a Key.", "test 2")
        
        self.assertEqual(len(self.memory.narrative_log), 2)
        self.assertEqual(self.memory.graph.nodes["Boric"]['source_id'], 1)
        print("Indexed Narrative Storage: PASS")

    def test_two_stage_retrieval(self):
        """Tests if retrieval correctly fetches context from the log."""
        self.memory.narrative_log = ["Turn 0", "Turn 1: Boric gives you a rusty key.", "Turn 2"]
        self.memory.graph.add_node("Boric", source_id=1)
        
        results = self.memory.retrieve_memories("What about Boric?")
        
        self.assertEqual(len(results), 1)
        self.assertIn("Turn 1: Boric gives you a rusty key.", results)
        print("Two-Stage Retrieval: PASS")
        
    def generate_report(self):
        """Runs all tests and returns a simple report."""
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(GraphMemoryTest))
        runner = unittest.TextTestRunner(verbosity=0)
        result = runner.run(suite)
        
        report = "\n--- Indexed Narrative Graph Test Report ---\n"
        if result.wasSuccessful():
            report += "Verdict: **PASS**\nAnalysis: The graph database successfully stored facts with pointers and retrieved the precise context."
        else:
            report += "Verdict: **FAIL**\nAnalysis: An error occurred in the graph logic."
        return report

def main():
    test_suite = GraphMemoryTest("generate_report")
    print(test_suite.generate_report())

if __name__ == "__main__":
    main()