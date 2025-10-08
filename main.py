import customtkinter as ctk
import json
import random
from threading import Thread

from storyteller.llm_client import client
from storyteller.memory_manager import MemoryManager
from storyteller import config
from frontend.app import ChatApp

def determine_skill(user_input):
    """Determines the relevant D&D skill and modifier from user input."""
    action_phrases = ["i try to", "i attempt to", "i want to"]
    if any(user_input.lower().startswith(phrase) for phrase in action_phrases):
        for skill, keywords in config.DND_RULES['skills'].items():
            if any(keyword in user_input.lower() for keyword in keywords):
                return skill
    return None

def game_logic_thread(user_input, ui_queue):
    """The final game logic loop using the 'Master AI' approach."""
    global memory_manager
    try:
        # D&D Skill Check
        skill_to_check = determine_skill(user_input)
        if skill_to_check:
            roll = random.randint(1, 20)
            player_attrs = memory_manager.graph.nodes.get("Player", {})
            modifier = player_attrs.get(skill_to_check, 0)
            total = roll + modifier
            ui_queue.put(("roll", f"Attempting {skill_to_check.upper()}... (Roll: {roll} + Mod: {modifier} = Total: {total})"))
            user_input += f" (D&D Skill Check Result: {total})"
        
        retrieved_context = memory_manager.retrieve_context(user_input)
        memory_context = "\n".join(retrieved_context)
        
        active_plot_point = memory_manager.get_active_plot_point()
        
        prompt_context = f"Active Plot Point: {active_plot_point}\n\nRelevant Context:\n{memory_context}\n\nPlayer Action: {user_input}"
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": config.MASTER_SYSTEM_PROMPT},
                {"role": "user", "content": prompt_context}
            ],
            model=config.LLM_MODEL,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)

        narrative = data.get("narrative", "The DM seems lost in thought...")
        facts = data.get("facts", [])
        plot_completed = data.get("plot_completed", False)

        ui_queue.put(("dm_response", narrative))
        
        turn_text = f"Player: {user_input}\nDM: {narrative}"
        turn_id = memory_manager.add_turn_to_log(turn_text)
        memory_manager.update_graph_with_facts(facts, turn_id)

        if plot_completed and active_plot_point:
            memory_manager.update_plot_point(active_plot_point)

    except Exception as e:
        ui_queue.put(("dm_response", f"An error occurred: {e}"))

def create_character_window(memory, app):
    """Creates a top-level window for character creation."""
    window = ctk.CTkToplevel(app)
    window.title("Character Creation")
    window.geometry("300x250")

    ctk.CTkLabel(window, text="Enter your character's name:").pack(pady=10)
    name_entry = ctk.CTkEntry(window)
    name_entry.pack(pady=5)

    ctk.CTkLabel(window, text="Choose your class:").pack(pady=10)
    class_var = ctk.StringVar(value="Fighter")
    class_menu = ctk.CTkOptionMenu(window, variable=class_var, values=["Fighter", "Rogue", "Wizard"])
    class_menu.pack(pady=5)

    def submit():
        name = name_entry.get()
        p_class = class_var.get()
        if name and p_class:
            class_info = config.DND_RULES["classes"][p_class]
            attributes = {
                "name": name,
                "class": p_class,
                "type": "player",
                class_info["modifier"]: class_info["value"]
            }
            memory.graph.add_node("Player", **attributes)
            
            app.ui_queue.put(("update_char_info", attributes))
            
            app.display_message(f"Welcome, {name} the {p_class}! Your adventure begins...\n\n", "dm")
            window.destroy()

    submit_button = ctk.CTkButton(window, text="Submit", command=submit)
    submit_button.pack(pady=15)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    
    memory_manager = MemoryManager()
    
    app = ChatApp(game_logic_runner=game_logic_thread)
    create_character_window(memory_manager, app)
    app.start_game()
    app.mainloop()