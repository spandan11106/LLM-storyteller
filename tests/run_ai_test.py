import json
import random
import time

# Import from your existing storyteller package
from storyteller.llm_client import client
from storyteller.memory_manager import MemoryManager
from storyteller import config

# --- 1. THE NEW, "ACTOR" PLAYER AI ---
PLAYER_SYSTEM_PROMPT = (
    "You are role-playing as Valerius, a heroic Fighter in a D&D game. "
    "Your persona is: **Brave and heroic, but also deeply suspicious of strangers and motivated by the promise of treasure.**\n"
    "Your primary goal is to complete the 'Active Plot Point', but your personality often leads you to take unexpected actions.\n"
    "Based on the Dungeon Master's last message, decide on your next action. "
    "Sometimes, choose one of the DM's suggestions. Other times, do something creative based on your suspicious or greedy nature. "
    "Describe your action in a short, first-person sentence. Example: 'I don't trust this Finnley. I'll try to sneak a look at the book he was reading.'"
)

def get_ai_player_action(conversation_history, active_plot_point):
    """An AI function that decides the player's next move based on its persona."""
    prompt = (
        f"Here is the story so far:\n{json.dumps(conversation_history, indent=2)}\n\n"
        f"Your current goal is to complete the plot point: '{active_plot_point}'.\n"
        "Based on your persona, what is your next action?"
    )
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": PLAYER_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        model=config.LLM_MODEL,
    )
    return response.choices[0].message.content

# --- 2. THE NEW, "MASTER IMPROVISER" DM AI ---
IMPROVISER_DM_SYSTEM_PROMPT = (
    "You are a Master Storyteller. You must follow these Golden Rules:\n"
    "1. **EMBRACE PLAYER CREATIVITY:** The player may do something unexpected. Your primary job is to say 'Yes, and...'—accept their action and creatively weave it back into the Active Plot Point. Never block the player's creativity.\n"
    "2. **THE PRESENT IS KING:** Your response MUST be a direct continuation of the player's most recent action. Use older memories only as background context.\n"
    "3. **MAINTAIN CONSISTENCY:** You are FORBIDDEN from changing an NPC's name, gender, or location within a scene.\n"
    "4. **BE INTERACTIVE:** Keep descriptions to 2-5 sentences and ALWAYS end by asking 'What do you do?' often with 2-3 clear choices.\n"
    "5. **FORMAT DIALOGUE:** Separate description from speech. Example: \nBoric: \"Welcome to my forge.\""
)

# --- The AI Referee (Unchanged) ---
def is_plot_point_complete(turn_text, active_plot_point):
    """Uses an AI referee to determine if a plot point was completed."""
    referee_prompt = f"The current objective is: '{active_plot_point}'. Based on this text, has the player completed it? Answer YES or NO.\n\n{turn_text}"
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": referee_prompt}],
        model=config.LLM_MODEL
    )
    return "YES" in response.choices[0].message.content.upper()

# --- The AI Auditor (Unchanged) ---
AUDITOR_SYSTEM_PROMPT = (
    "You are a master literary analyst and game critic. Audit a game transcript for quality.\n"
    "1. **Narrative Coherence:** Does the story make sense?\n"
    "2. **Character Consistency:** Do NPCs act consistently?\n"
    "3. **Location Consistency:** Does the scene ever teleport randomly?\n"
    "4. **Plot Adherence:** Did the DM successfully guide the player through all plot points?\n\n"
    "Provide a brief analysis and a final verdict: 'VERDICT: PASS' or 'VERDICT: FAIL'."
)

def run_final_audit(transcript, plot_points):
    """An AI function that analyzes the entire game session for errors."""
    prompt = (
        f"Required Plot Points:\n{json.dumps(plot_points, indent=2)}\n\n"
        f"Full Game Transcript:\n{transcript}"
    )
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": AUDITOR_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        model=config.LLM_MODEL,
    )
    return response.choices[0].message.content

# --- Main Test Runner ---
def main():
    """Main function to run the AI vs. AI automated test."""
    print("--- Starting AI vs. AI Story Consistency Test (v3 - Persona Driven) ---")
    
    dm_memory = MemoryManager()
    dm_memory.knowledge_graph["Player"] = {
        'properties': [
            {"entity": "Player", "property": "name", "value": "Valerius"},
            {"entity": "Player", "property": "class", "value": "Fighter"},
            {"entity": "Player", "property": "strength", "value": 3}
        ], 'relationships': []
    }
    
    conversation_history = []
    full_transcript = "--- START OF GAME ---\n"
    
    dm_response = "You find yourself in the Whispering Woods antique shop. The air smells of old parchment and mystery. The shopkeeper, Mr. Finnley, looks up as you enter.\n\nFinnley: \"Welcome, traveler. What brings you to my humble shop?\""
    conversation_history.append({"role": "assistant", "content": dm_response})
    full_transcript += f"DM: {dm_response}\n\n"
    print(f"DM: {dm_response}")

    num_turns = 10
    for i in range(num_turns):
        active_plot = dm_memory.get_active_plot_point()
        if not active_plot:
            print("\n--- Story Complete! ---")
            break
        
        print(f"\n--- [Turn {i+1}/{num_turns} | Active Plot: {active_plot}] ---")

        player_action = get_ai_player_action(conversation_history, active_plot)
        conversation_history.append({"role": "user", "content": player_action})
        full_transcript += f"Valerius (AI Player): {player_action}\n\n"
        print(f"Valerius (AI Player): {player_action}")

        prompt_context = f"Active Plot Point: {active_plot}"
        messages_for_api = [
            {"role": "system", "content": IMPROVISER_DM_SYSTEM_PROMPT}, # Use the new DM prompt
            {"role": "system", "content": prompt_context},
            *conversation_history[-3:]
        ]
        
        response = client.chat.completions.create(
            messages=messages_for_api, model=config.LLM_MODEL
        )
        dm_response = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": dm_response})
        full_transcript += f"DM: {dm_response}\n\n"
        print(f"DM: {dm_response}")

        turn_text = f"Player: {player_action}\nDM: {dm_response}"
        if is_plot_point_complete(turn_text, active_plot):
            dm_memory._complete_plot_point(active_plot)
            
        dm_memory.save_memory(turn_text, player_action)
        time.sleep(1)

    full_transcript += "--- END OF GAME ---\n"
    
    print("\n\n--- Game Simulation Complete. Running Final Audit... ---")
    audit_report = run_final_audit(full_transcript, config.PLOT_POINTS)
    print("\n--- AUDIT REPORT ---")
    print(audit_report)
    print("--------------------")

if __name__ == "__main__":
    main()
