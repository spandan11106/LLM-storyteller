import time
import json
import statistics
from storyteller.llm_client import client
from storyteller.memory_manager import MemoryManager
from storyteller import config

class FinalBenchmark:
    """
    The final, definitive benchmark suite. It tests the 'Unified AI Core'
    for speed and the 'CoT Query Engine' for accuracy.
    """
    def __init__(self):
        self.memory = MemoryManager()
        self.time_results = []

    def run_time_test(self, num_turns=5):
        """Measures the latency of the final 'Unified AI Core' architecture."""
        print("\n--- [1/2] Running Time Efficiency Benchmark ---")
        for i in range(num_turns):
            total_start = time.time()
            user_input = f"Benchmark turn {i+1}"
            context = "\n".join(self.memory.retrieve_context(user_input))
            plot = self.memory.get_active_plot_point()
            prompt = f"Plot:{plot}\nContext:{context}\nAction:{user_input}"
            
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": config.MASTER_SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                model=config.LLM_MODEL, response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            
            turn_id = self.memory.add_turn_to_log(data.get("narrative", ""))
            self.memory.update_graph_with_facts(data.get("facts", []), turn_id)
            if data.get("plot_completed", False) and plot:
                self.memory.update_plot_point(plot)
            
            self.time_results.append(time.time() - total_start)
        
        avg_time = statistics.mean(self.time_results)
        print("--- Time Efficiency Report ---")
        print(f"**Average Total Turn Time (Unified AI Core):** {avg_time:.4f} seconds\n")

    def run_accuracy_test(self):
        """Runs the 'Rusty Key vs. Silver Key' stress test with the CoT Engine."""
        print("\n--- [2/2] Running Memory Accuracy Stress Test ---")
        test_script = [
            "Boric the blacksmith gives me a RUSTY key.",
            "I find a SILVER key in a chest.",
            "What did Boric give me earlier?"
        ]
        final_response = ""
        for user_input in test_script:
            context = "\n".join(self.memory.retrieve_context(user_input))
            prompt = f"Context:\n{context}\nAction:{user_input}"
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": config.MASTER_SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                model=config.LLM_MODEL, response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            final_response = data.get("narrative", "")
            turn_id = self.memory.add_turn_to_log(final_response)
            self.memory.update_graph_with_facts(data.get("facts", []), turn_id)
        
        print("--- Memory Accuracy Report ---")
        if "rusty" in final_response.lower() and "silver" not in final_response.lower():
            print("Verdict: **PASS**")
            print("Analysis: The system successfully retrieved the precise context for 'Boric', ignoring the irrelevant 'silver key' fact.")
        else:
            print("Verdict: **FAIL**")
            print("Analysis: The system was unable to differentiate between the two similar facts.")

def main():
    print("==================================================")
    print("  RUNNING FINAL, DEFINITIVE BENCHMARK SUITE")
    print("==================================================")
    
    benchmark = FinalBenchmark()
    benchmark.run_time_test()
    benchmark.run_accuracy_test()

    print("\n==================================================")
    print("            ALL TESTS COMPLETE")
    print("==================================================")

if __name__ == "__main__":
    main()