from storyteller.memory_manager import MemoryManager

class MemoryBenchmark:
    """
    Runs a 'Memory Stress Test' to evaluate the RAG system's ability to
    differentiate between similar but distinct facts.
    """
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.test_script = [
            ("Boric the blacksmith gives me a RUSTY key.", "Fact established."),
            ("I talk to the barkeep.", "Filler action."),
            ("I find a SILVER key in a chest.", "Conflicting fact established."),
            ("I explore the town square.", "Filler action."),
            ("I ask Boric: What did you give me earlier?", "Test question.")
        ]

    def run_test(self):
        """Runs the stress test and returns the final turn's AI response."""
        from storyteller.llm_client import client
        from storyteller import config
        
        ai_response = ""
        for i, (user_input, _) in enumerate(self.test_script):
            # Simulate a full game turn to populate memory
            context = f"Active Plot Point: TEST\nMemories: \nFacts: \nContinue."
            messages = [
                {"role": "system", "content": config.MASTER_SYSTEM_PROMPT},
                {"role": "system", "content": context},
                {"role": "user", "content": user_input}
            ]
            response = client.chat.completions.create(messages=messages, model=config.LLM_MODEL)
            ai_response = response.choices[0].message.content
            turn_text = f"Player: {user_input}\nDM: {ai_response}"
            self.memory.save_memory(turn_text, user_input)
            # Before the final question, for realism include retrieved memories in the message
            if i == len(self.test_script) - 2:
                # this is the turn before the final question; collect memories now
                pass

        # For the final question, include the memory retrieval context so the LLM can reference stored facts
        final_query = self.test_script[-1][0]
        retrieved = self.memory.retrieve_memories(final_query, n_results=5)
        memory_context = "\n".join(retrieved) if retrieved else ""
        final_messages = [
            {"role": "system", "content": config.MASTER_SYSTEM_PROMPT},
            {"role": "system", "content": f"Relevant Memories:\n{memory_context}"},
            {"role": "user", "content": final_query}
        ]
        final_response = client.chat.completions.create(messages=final_messages, model=config.LLM_MODEL)
        ai_response = final_response.choices[0].message.content

        return ai_response # Return the answer to the final question

    def generate_report(self):
        """Analyzes the test result deterministically by inspecting the memory graph."""
        # Run the script to populate memory
        _ = self.run_test()

        report = "\n--- Memory Efficiency (Accuracy) Report ---\n"
        report += "Test Scenario: Introduced a 'RUSTY key' from Boric and a 'SILVER key' from a chest, then asked Boric what he gave the player.\n"

        # Inspect the knowledge graph for a 'gave' edge from Boric to an object containing 'rusty'
        boric_facts = self.memory.rag.graph.out_edges("Boric", data=True) if self.memory.rag.graph.has_node("Boric") else []
        found_rusty = False
        for _, obj, data in boric_facts:
            label = data.get('label', '')
            if label and label.lower() == 'gave':
                if 'rusty' in str(obj).lower() or 'rusty' in str(self.memory.rag.graph.nodes[obj].get('desc', '')).lower():
                    found_rusty = True
                    break

        if found_rusty:
            verdict = "PASS"
            explanation = "The graph contains a 'gave' relation from Boric to a Rusty item — memory stored correctly."
        else:
            verdict = "FAIL"
            explanation = "The graph does not contain the expected 'gave' relation for Boric -> RUSTY key."

        report += f"Verdict: **{verdict}**\n"
        report += f"Analysis: {explanation}\n"
        return report