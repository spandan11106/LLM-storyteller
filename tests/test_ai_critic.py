# tests/test_ai_critic.py

import unittest
from unittest.mock import patch, MagicMock
import json
import time

from storyteller.memory_manager import MemoryManager
from storyteller.engine import game_logic_thread
from storyteller.llm_client import client
from storyteller import config

# --- AI PERSONAS FOR THE TEST ---

def get_ai_player_action(history: list, goal: str) -> str:
    """An AI that acts as the player."""
    player_persona = (
        "You are Valerius, a heroic Fighter playing a D&D game. "
        "You will be given the last few turns of the story and a high-level goal. "
        "Your task is to generate the specific, in-character action to achieve this goal. "
        "State your action in a single, first-person sentence."
    )
    prompt = f"Story so far:\n{json.dumps(history[-4:])}\n\nYour current goal: '{goal}'.\n\nYour Action:"
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": player_persona},
            {"role": "user", "content": prompt}
        ],
        model=config.LLM_MODEL
    )
    return response.choices[0].message.content

def get_ai_critic_report(full_transcript: str) -> str:
    """An AI that acts as a game critic."""
    critic_persona = (
        "You are an expert AI Game Critic. I will provide a full 10-turn transcript of a D&D game. " # Updated to 10
        "Your task is to evaluate the Dungeon Master's (DM) performance based on three criteria:\n"
        "1. **Coherence:** Did the DM's replies logically follow the player's actions?\n"
        "2. **Memory:** Did the DM remember key facts, NPC states, and events from earlier in the conversation?\n"
        "3. **Creativity:** Was the story interesting and engaging? Did the DM introduce new elements effectively?\n\n"
        "Please provide a short, bulleted analysis for each criterion and a final, one-word verdict: **PASS** or **FAIL**."
    )
    prompt = f"Here is the full game transcript:\n\n{full_transcript}"

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": critic_persona},
            {"role": "user", "content": prompt}
        ],
        model=config.LLM_MODEL 
    )
    return response.choices[0].message.content


class TestAICritic(unittest.TestCase):
    """
    An end-to-end test where an AI player interacts with the AI DM,
    and a final AI critic evaluates the entire conversation.
    """
    
    def test_run_simulation_and_get_report(self):
        """Runs the 10-turn simulation and prints the final critic report."""
        print("\n--- Starting AI Critic Simulation (10 Turns) ---")
        print("This will take a minute as it involves many LLM calls...")

        memory = MemoryManager()
        history = []
        full_transcript = "--- START OF GAME ---\n"

        dm_response = "You are in the town of Silver Creek. You see the town blacksmith, Boric, looking distressed near his forge. What do you do?"
        history.append({"role": "assistant", "content": dm_response})
        full_transcript += f"Turn 0 (DM): {dm_response}\n\n"
        print(f"Turn 0 (DM): {dm_response}")

        # --- UPDATED: Goals list is now multiplied by 2 for 10 turns ---
        goals = [
            "Ask Boric what is wrong.",
            "Offer to help Boric find his stolen hammer.",
            "Ask Boric who might have stolen his hammer.",
            "Learn about the 'Shadow Goblins' who live in the nearby woods.",
            "Decide to go to the Whispering Woods to find the goblins.",
        ] * 2

        # --- UPDATED: Loop now runs for 10 turns ---
        for i in range(10):
            turn_num = i + 1
            print(f"\n--- Turn {turn_num}/10 ---")
            
            player_action = get_ai_player_action(history, goals[i])
            history.append({"role": "user", "content": player_action})
            full_transcript += f"Turn {turn_num} (Player): {player_action}\n"
            print(f"Turn {turn_num} (Player): {player_action}")

            class MockQueue:
                def __init__(self): self.items = []
                def put(self, item): self.items.append(item)
                def get(self): return self.items.pop(0)

            mock_ui_queue = MockQueue()
            game_logic_thread(player_action, mock_ui_queue, memory)
            
            message_type, dm_response = mock_ui_queue.get()
            
            history.append({"role": "assistant", "content": dm_response})
            full_transcript += f"Turn {turn_num} (DM): {dm_response}\n\n"
            print(f"Turn {turn_num} (DM): {dm_response}")
            
            # --- UPDATED: Delay is no longer needed for 10 turns ---
            # time.sleep(10)

        full_transcript += "--- END OF GAME ---"
        print("\n--- Simulation Complete. Generating AI Critic Report... ---")

        critic_report = get_ai_critic_report(full_transcript)
        
        print("\n\n========================================")
        print("    🤖 AI CRITIC FINAL REPORT 🤖")
        print("========================================")
        print(critic_report)
        
        self.assertIn("Verdict:", critic_report)


if __name__ == '__main__':
    unittest.main()