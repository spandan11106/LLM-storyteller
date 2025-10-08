import json
import time
from storyteller.llm_client import client
from storyteller.memory_manager import MemoryManager
from storyteller import config

# --- AI PERSONAS FOR THE HIGH-SPEED DYNAMIC TEST ---

def get_orchestrator_goal(turn_number):
    """The 'Director' AI that sets the high-level goal for the Player AI."""
    if turn_number == 1:
        return "Your goal is to establish a secret password with the blacksmith, Boric. The password is 'Ironscale'. Be direct."
    elif turn_number == 30:
        return "Your goal is to test the DM's long-term memory. Ask Boric for the secret password he told you in Turn 1."
    else:
        return "Your goal is to create a distraction. Go on a brief, unrelated adventure in the nearby woods."

def get_ai_player_action(history, goal):
    """The 'Actor' AI that generates a concise, in-character action."""
    player_persona = (
        "You are Valerius, a Fighter. You are playing a D&D game. "
        "Your goal is to achieve the objective you've been given. "
        "**BE VERY BRIEF.** State your action in a single, concise, first-person sentence. "
        "Example: 'I ask Boric for the secret password.'"
    )
    prompt = f"Story so far:\n{json.dumps(history)}\n\nYour Goal: '{goal}'.\n\nYour Action (be brief):"
    response = client.chat.completions.create(messages=[{"role": "system", "content": player_persona}, {"role": "user", "content": prompt}], model=config.LLM_MODEL)
    return response.choices[0].message.content

def summarize_transcript(full_transcript):
    """Uses an AI to summarize the long transcript to avoid token limits."""
    prompt = f"Provide a concise summary of the key events in this game transcript, focusing on the secret from Turn 1 and the final question in Turn 30:\n\n{full_transcript}"
    response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=config.LLM_MODEL)
    return response.choices[0].message.content

def get_audit_report(summary):
    """The 'Judge' AI that analyzes the summary for a final verdict."""
    auditor_persona = "You are an AI Test Auditor. Your job is to determine if the test was a success. 1. Identify the 'secret password' from the start of the summary. 2. Determine if the DM's final response correctly recalled that password. 3. Provide a brief analysis and a 'VERDICT: PASS' or 'VERDICT: FAIL'."
    prompt = f"Here is the summary of the game:\n\n{summary}"
    response = client.chat.completions.create(messages=[{"role": "system", "content": auditor_persona}, {"role": "user", "content": prompt}], model=config.LLM_MODEL)
    return response.choices[0].message.content

# A dedicated, simple prompt for this test that also enforces brevity
VALIDATION_DM_PROMPT = (
    "You are a D&D Dungeon Master. Respond to the player's action based on the context. "
    "**BE EXTREMELY BRIEF.** Keep your entire response under 50 words. "
    "Always end by asking 'What do you do?'"
)

class FinalValidationTest:
    """
    The definitive 'Needle in the Haystack' stress test to validate long-term recall
    over a 30-turn, dynamically generated story.
    """
    def run_and_generate_report(self):
        """Runs the full simulation and returns the final auditor's report."""
        print("--- Running Final 30-Turn Long-Term Recall Validation ---")
        print("This is the definitive test and will take several minutes...")
        memory = MemoryManager()
        memory.graph.add_node("Player", name="Valerius", class_name="Fighter")

        history = []
        full_transcript = "--- START OF 30-TURN VALIDATION ---\n"
        
        dm_response = "You are at the forge with Boric the blacksmith.\n\nBoric: \"Welcome, Valerius.\""
        history.append({"role": "assistant", "content": dm_response})
        full_transcript += f"DM: {dm_response}\n\n"
        print(f"DM: {dm_response}")

        for i in range(30):
            turn_number = i + 1
            print(f"\n[Turn {turn_number}/30]")
            
            orchestrator_goal = get_orchestrator_goal(turn_number)
            
            player_action = get_ai_player_action(history[-2:], orchestrator_goal)
            history.append({"role": "user", "content": player_action})
            full_transcript += f"Valerius (AI Player): {player_action}\n\n"
            print(f"Valerius (AI Player): {player_action}")

            context = "\n".join(memory.retrieve_context(player_action))
            plot_point = memory.get_active_plot_point()
            prompt_context = f"Plot: {plot_point}\nContext:\n{context}\nAction: {player_action}"
            
            messages = [
                {"role": "system", "content": VALIDATION_DM_PROMPT},
                {"role": "system", "content": prompt_context},
                {"role": "user", "content": player_action}
            ]
            response = client.chat.completions.create(messages=messages, model=config.LLM_MODEL)
            dm_response = response.choices[0].message.content
            
            history.append({"role": "assistant", "content": dm_response})
            full_transcript += f"DM: {dm_response}\n\n"
            print(f"DM: {dm_response}")

            # Call the correct, separated memory functions
            turn_text = f"Player: {player_action}\nDM: {dm_response}"
            turn_id = memory.add_turn_to_log(turn_text)
            # Use a simplified fact extraction for this test to keep it fast
            facts = [{"subject": "Player", "relation": "did", "object": player_action[:30]}]
            memory.update_graph_with_facts(facts, turn_id)

            if plot_point and memory._is_plot_point_complete(turn_text, plot_point):
                 memory._complete_plot_point(plot_point)

            time.sleep(1.5)

        full_transcript += "--- END OF 30-TURN VALIDATION ---\n"
        
        print("\n--- Simulation Complete. Summarizing transcript for final audit... ---")
        summary = summarize_transcript(full_transcript)
        
        print("--- Summary Complete. Requesting Final Verdict from Auditor AI... ---")
        audit_report = get_audit_report(summary)

        report = "\n--- Final Long-Term Recall Validation Report (30 Turns) ---\n"
        report += "Methodology: A 'Director' AI guided an 'Actor' AI to establish a secret password on Turn 1, create a 28-turn distraction, and then test recall on Turn 30. A final 'Judge' AI audited a summary of the transcript for success.\n\n"
        report += "**Auditor's Final Verdict:**\n"
        report += audit_report
        return report

# --- This is the corrected entry point ---
if __name__ == "__main__":
    test = FinalValidationTest()
    print(test.run_and_generate_report())