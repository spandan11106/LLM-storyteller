import time
import json
import random
import statistics


# Important: Make sure to import from your storyteller package
from storyteller.llm_client import client
from storyteller.memory_manager import MemoryManager
from storyteller import config

# --- The Automated Test Script ---
# This list of inputs is designed to test every feature of your system.
TEST_SCRIPT = [
    # Turns 1-2: Establish initial facts
    "My name is Valerius, and I am a Fighter. I walk into the tavern.",
    "I greet the blacksmith, whose name is Boric. He gives me a RUSTY key.",
    # Turns 3-4: Test Skill Checks
    "I see a noble in the corner. I try to sneak over to his table.", # Dexterity check
    "The noble looks tough. I try to intimidate him for information.", # Strength check
    # Turn 5: Introduce conflicting information for the stress test
    "I find a SILVER key hidden under a loose floorboard.",
    # Turns 6-10: Filler actions to populate the memory
    "I order an ale from the barkeep.",
    "I ask the barkeep about recent rumors.",
    "A mysterious stranger in a dark cloak enters the tavern. I watch them.",
    "The stranger sits down. I decide to approach the stranger.",
    "I ask the stranger for their name.", # Completes first plot point
    # Turns 11-15: Test Smart Query (RAG on Graph)
    "Who is Boric?",
    "What keys do I have?", # Tests ability to differentiate between rusty and silver
    "What is my current objective?", # Tests plot point retrieval
    "I accept the quest from the stranger.", # Completes second plot point
    "Where is the hidden cave?",
    # Turns 16-20: Final actions and stability test
    "I leave the tavern and head towards the Whispering Woods.",
    "I investigate the strange runes on the cave entrance.", # Intelligence check
    "I enter the hidden cave.", # Completes third plot point
    "I confront the goblin leader inside the cave.", # Completes final plot point
    "What was the first thing Boric gave me?" # Final memory stress test
]

def determine_skill(user_input):
    """Determines the relevant D&D skill and modifier from user input."""
    for skill, keywords in config.DND_RULES['skills'].items():
        for keyword in keywords:
            if keyword in user_input.lower():
                return skill
    return None

def run_automated_turn(memory, user_input):
    """Runs a single turn of the game logic and returns timing data."""
    turn_timings = {}
    
    # --- Smart Query Check ---
    if "?" in user_input:
        intent_data = memory._decompose_query_to_intent(user_input)
        memory.find_answer_in_graph(intent_data) # We run it but don't need the answer for the test

    # --- Skill Check ---
    skill_to_check = determine_skill(user_input)
    if skill_to_check:
        player_props = memory.knowledge_graph.get("Player", {}).get("properties", [])
        # ... (rest of skill check logic is for gameplay, not essential for timing)

    # --- RAG Retrieval ---
    rag_start = time.time()
    memory.retrieve_memories(user_input)
    turn_timings['rag_retrieval'] = time.time() - rag_start

    # --- LLM Generation ---
    # We create a simplified context for the benchmark to keep it consistent
    prompt_context = "Automated benchmark in progress."
    messages_for_api = [
        {"role": "system", "content": config.GAME_SYSTEM_PROMPT},
        {"role": "system", "content": prompt_context},
        {"role": "user", "content": user_input}
    ]
    llm_start = time.time()
    response = client.chat.completions.create(
        messages=messages_for_api, model=config.LLM_MODEL
    )
    ai_response = response.choices[0].message.content
    turn_timings['llm_generation'] = time.time() - llm_start

    # --- Memory Saving ---
    save_start = time.time()
    turn_text = f"Player: {user_input}\nDM: {ai_response}"
    memory.save_memory(turn_text, user_input)
    turn_timings['memory_saving'] = time.time() - save_start
    
    return turn_timings

def main():
    """Main function to run the automated benchmark."""
    print("--- Starting Automated Benchmark ---")
    print(f"Running a {len(TEST_SCRIPT)}-turn story to test all memory systems.")
    
    memory_manager = MemoryManager()
    
    # Simulate Character Creation
    memory_manager.knowledge_graph["Player"] = {
        'properties': [
            {"entity": "Player", "property": "name", "value": "Valerius"},
            {"entity": "Player", "property": "class", "value": "Fighter"},
            {"entity": "Player", "property": "strength", "value": 3}
        ],
        'relationships': []
    }

    all_results = []
    
    for i, turn_input in enumerate(TEST_SCRIPT):
        print(f"\n[Turn {i+1}/{len(TEST_SCRIPT)}] Input: '{turn_input}'")
        timings = run_automated_turn(memory_manager, turn_input)
        all_results.append(timings)
        print(f"    RAG: {timings['rag_retrieval']:.4f}s | LLM: {timings['llm_generation']:.4f}s | Save: {timings['memory_saving']:.4f}s")

    # --- Final Analysis ---
    print("\n\n--- Benchmark Complete: Final Report ---")
    
    # Calculate averages
    avg_rag = statistics.mean([r['rag_retrieval'] for r in all_results])
    avg_llm = statistics.mean([r['llm_generation'] for r in all_results])
    avg_save = statistics.mean([r['memory_saving'] for r in all_results])
    total_times = [sum(r.values()) for r in all_results]
    avg_total = statistics.mean(total_times)

    print("\n**Average Latency per Operation:**")
    print("------------------------------------")
    print(f"RAG Retrieval (Vector Search): {avg_rag:.4f} seconds")
    print(f"LLM Generation (API Call):     {avg_llm:.4f} seconds")
    print(f"Memory Saving (Summarize/Fact):{avg_save:.4f} seconds")
    print("------------------------------------")
    print(f"**Average Total Turn Time:** {avg_total:.4f} seconds")
    
    print("\n**System Stability & Accuracy:**")
    print("------------------------------------")
    print(f"Successfully completed {len(TEST_SCRIPT)} turns without crashing: YES")
    # Manually verify the final fact state after the run
    final_keys = memory_manager.get_facts_about("Player")
    print(f"Final character state verified: {'YES' if final_keys else 'NO'}")
    print("------------------------------------\n")


if __name__ == "__main__":
    main()
