import json
import time
from storyteller.llm_client import client
from storyteller.memory_manager import MemoryManager
from storyteller import config

# --- AI PERSONAS FOR THE DYNAMIC TEST ---

def get_orchestrator_goal(test_phase, turn_number):
    """The 'Director' AI that sets the high-level goal for the Player AI."""
    instruction = ""
    if test_phase == "ESTABLISH_SECRET":
        instruction = "Your goal is to establish a non-obvious, specific secret about the NPC 'Finnley'. Generate an action where you learn this secret from him."
    elif test_phase == "GENERATE_NOISE":
        instruction = f"Your goal is to create a distraction. Take the story in a completely new direction, away from Finnley and his secret. Perhaps explore a nearby forest or talk about goblin raids for the next {20 - turn_number} turns."
    elif test_phase == "TEST_RECALL":
        instruction = "Your goal is to test the DM's long-term memory. Return to the original topic and ask a specific question that requires the DM to recall the secret you established in the first turn."

    prompt = f"You are a test orchestrator. Your job is to provide a goal for a Player AI. The current test phase is '{test_phase}'.\nYour instruction to the player is: {instruction}"
    # In a real scenario, this could also be an LLM call for more dynamic goals.
    # For reliability, we'll keep it deterministic for now.
    return instruction

def get_ai_player_action(history, goal):
    """The 'Actor' AI that generates an in-character action to meet the goal."""
    player_persona = (
        "You are Valerius, a heroic Fighter. You are playing a D&D game. "
        "You have been given a high-level goal. Your task is to generate the specific, creative, in-character action to achieve this goal. "
        "State your action in a short, first-person sentence."
    )
    prompt = f"Here is the story so far:\n{json.dumps(history)}\n\nYour current high-level goal: '{goal}'.\n\nYour specific action is:"
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": player_persona}, {"role": "user", "content": prompt}],
        model=config.LLM_MODEL
    )
    return response.choices[0].message.content

def get_audit_report(full_transcript):
    """The 'Judge' AI that analyzes the full transcript for a final verdict."""
    auditor_persona = (
        "You are an AI Test Auditor. I will give you a full game transcript. Your job is to determine if the test was a success. "
        "1. First, read the beginning of the transcript and identify the specific 'secret' that was established. "
        "2. Second, read the end of the transcript and determine if the Dungeon Master's final response correctly recalled that specific secret. "
        "3. Finally, provide a brief analysis and a definitive verdict: 'VERDICT: PASS' or 'VERDICT: FAIL'."
    )
    prompt = f"Here is the full game transcript:\n\n{full_transcript}"
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": auditor_persona}, {"role": "user", "content": prompt}],
        model=config.LLM_MODEL
    )
    return response.choices[0].message.content


class DynamicLongTermMemoryTest:
    """
    An advanced stress test that uses an AI player to dynamically generate
    a 20-turn story to test long-term recall.
    """
    def run_and_generate_report(self):
        """Runs the full simulation and returns the final auditor's report."""
        print("--- Starting Dynamic 20-Turn Long-Term Memory Stress Test ---")
        memory = MemoryManager()
        memory.graph.add_node("Player", name="Valerius", class_name="Fighter", strength=3)

        history = []
        full_transcript = "--- START OF DYNAMIC TEST ---\n"
        
        dm_response = "You are in Mr. Finnley's antique shop.\n\nFinnley: \"Welcome, traveler. I sense you are here for a reason.\""
        history.append({"role": "assistant", "content": dm_response})
        full_transcript += f"DM: {dm_response}\n\n"
        print(f"DM: {dm_response}")

        for i in range(20):
            test_phase = ""
            if i == 0:
                test_phase = "ESTABLISH_SECRET"
            elif i == 19:
                test_phase = "TEST_RECALL"
            else:
                test_phase = "GENERATE_NOISE"

            print(f"\n[Turn {i+1}/20 | Phase: {test_phase}]")
            
            orchestrator_goal = get_orchestrator_goal(test_phase, i + 1)
            
            player_action = get_ai_player_action(history[-2:], orchestrator_goal)
            history.append({"role": "user", "content": player_action})
            full_transcript += f"Valerius (AI Player): {player_action}\n\n"
            print(f"Valerius (AI Player): {player_action}")

            context = "\n".join(memory.retrieve_memories(player_action))
            plot_point = memory.get_active_plot_point()
            prompt_context = f"Plot: {plot_point}\nContext:\n{context}"
            
            messages = [
                {"role": "system", "content": config.GAME_SYSTEM_PROMPT},
                {"role": "system", "content": prompt_context},
                {"role": "user", "content": player_action}
            ]
            response = client.chat.completions.create(messages=messages, model=config.LLM_MODEL)
            dm_response = response.choices[0].message.content
            history.append({"role": "assistant", "content": dm_response})
            full_transcript += f"DM: {dm_response}\n\n"
            print(f"DM: {dm_response}")

            memory.save_memory(f"Player: {player_action}\nDM: {dm_response}", player_action)
            time.sleep(1)

        full_transcript += "--- END OF DYNAMIC TEST ---\n"
        
        print("\n--- Simulation Complete. Requesting Final Audit from Judge AI... ---")
        audit_report = get_audit_report(full_transcript)

        report = "\n--- Dynamic Long-Term Memory Test Report (20 Turns) ---\n"
        report += "Methodology: A 'Director' AI guided an 'Actor' AI through a 20-turn game to test the DM's memory. A final 'Judge' AI audited the transcript for success.\n\n"
        report += "**Auditor's Final Report:**\n"
        report += audit_report
        return report

if __name__ == "__main__":
    test = DynamicLongTermMemoryTest()
    print(test.run_and_generate_report())