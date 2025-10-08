import customtkinter as ctk
import json
import random

from storyteller.llm_client import client
from storyteller.memory_manager import MemoryManager
from storyteller import config
from frontend.app import ChatApp

def determine_skill(user_input):
    """Determines the relevant D&D skill and modifier from user input."""
    for skill, keywords in config.DND_RULES['skills'].items():
        for keyword in keywords:
            if keyword in user_input.lower():
                return skill
    return None

def game_logic_thread(user_input, ui_queue):
    """Contains the core game logic and runs in a separate thread."""
    global memory_manager
    try:
        # Smart Query: Check if the user is asking a direct question
        if "?" in user_input:
            intent_data = memory_manager._decompose_query_to_intent(user_input)
            answer = memory_manager.find_answer_in_graph(intent_data)
            if answer:
                # If we found a direct answer, show it and bypass story generation
                ui_queue.put(("dm_response", f"(From Memory): {answer}"))
                return # End the turn here

        # D&D Skill Check System
        skill_to_check = determine_skill(user_input)
        if skill_to_check:
            roll = random.randint(1, 20)
            player_props = memory_manager.knowledge_graph.get("Player", {}).get("properties", [])
            modifier = 0
            for prop in player_props:
                if prop.get("property") == skill_to_check:
                    modifier = prop.get("value", 0)
            
            total = roll + modifier
            ui_queue.put(("roll", f"You attempt a {skill_to_check.upper()} check... (Roll: {roll} + Modifier: {modifier} = Total: {total})"))
            user_input += f" (D&D Skill Check Result: {total})"
        
        relevant_memories = memory_manager.retrieve_memories(user_input)
        memory_context = "\n".join(relevant_memories)
        
        known_facts = []
        for entity in memory_manager.knowledge_graph.keys():
            if entity.lower() in user_input.lower() or entity == "Player":
                facts = memory_manager.get_facts_about(entity)
                if facts:
                    known_facts.append(f"Facts about {entity}: {json.dumps(facts)}")
        fact_context = "\n".join(known_facts)

        active_plot_point = memory_manager.get_active_plot_point()
        plot_directive = f"Active Plot Point (Your Goal): {active_plot_point}" if active_plot_point else "No active plot point."

        prompt_context = f"{plot_directive}\n\nRelevant Memories:\n{memory_context}\n\nKnown Facts:\n{fact_context}\n\nContinue the story."
        
        messages_for_api = [
            {"role": "system", "content": config.GAME_SYSTEM_PROMPT},
            {"role": "system", "content": prompt_context},
            {"role": "user", "content": user_input}
        ]

        chat_completion = client.chat.completions.create(
            messages=messages_for_api,
            model=config.LLM_MODEL,
        )
        ai_response = chat_completion.choices[0].message.content
        ui_queue.put(("dm_response", ai_response))

        turn_text = f"Player: {user_input}\nDM: {ai_response}"
        memory_manager.save_memory(turn_text, user_input)

    except Exception as e:
        ui_queue.put(("dm_response", f"An error occurred: {e}"))

def create_character(memory):
    """Guides the player through character creation in the terminal."""
    print("--- Character Creation ---")
    name = input("Enter your character's name: ")
    print("Choose your class: Fighter, Rogue, Wizard")
    p_class = ""
    while p_class not in config.DND_RULES["classes"]:
        p_class = input("> ").capitalize()

    memory.knowledge_graph["Player"] = {'properties': [], 'relationships': []}
    memory.knowledge_graph["Player"]["properties"].append({"entity": "Player", "property": "name", "value": name})
    memory.knowledge_graph["Player"]["properties"].append({"entity": "Player", "property": "class", "value": p_class})
    
    class_info = config.DND_RULES["classes"][p_class]
    memory.knowledge_graph["Player"]["properties"].append({
        "entity": "Player", "property": class_info["modifier"], "value": class_info["value"]
    })
    print(f"Welcome, {name} the {p_class}! Your adventure begins...")
    print("--------------------------")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    memory_manager = MemoryManager()
    
    create_character(memory_manager)
    
    app = ChatApp(game_logic_runner=game_logic_thread)
    app.start_game()
    app.mainloop()