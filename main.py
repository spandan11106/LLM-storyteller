# main.py

import customtkinter as ctk

from storyteller.memory_manager import MemoryManager
from storyteller import config
from storyteller.engine import game_logic_thread
from frontend.app import ChatApp

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
            
            # --- UPDATED: Removed inventory from initial attributes ---
            attributes = {
                "name": name,
                "class": p_class,
                "type": "player",
                class_info["modifier"]: class_info["value"],
                "state": "Healthy"
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
    
    app = ChatApp(game_logic_runner=game_logic_thread, memory_manager=memory_manager)
    create_character_window(memory_manager, app)
    app.start_game()
    app.mainloop()