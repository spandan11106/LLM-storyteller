# storyteller/ui/gui.py
"""
🎨 Your Beautiful Adventure Interface - Where Magic Meets User-Friendly Design!

This is the gorgeous graphical interface that makes interacting with your AI
storyteller feel like playing the most amazing adventure game ever created!
Think of it as your personal adventure cockpit with all the controls you need.
"""

import customtkinter as ctk
from tkinter import messagebox
import json
from typing import Optional
from threading import Thread
import queue

from ..core.engine import StorytellingEngine
from ..config import GUI_WINDOW_SIZE, GUI_TITLE


class StorytellerGUI(ctk.CTk):
    """🖼️ Your Amazing Adventure Interface - Beautiful, Intuitive, and Fun!"""
    
    def show_game_instructions(self):
        """📜 Share the exciting game instructions with our adventurer!"""
        instructions = (
            "🎉 Welcome to Your Amazing AI Storytelling Adventure!\n\n"
            "Get ready for an incredible journey through 15 epic quests that will take you "
            "through ancient mysteries, medieval legends, and futuristic worlds!\n"
            "Each quest gets more challenging and exciting than the last. You have the power "
            "to do anything you can imagine, but remember - every choice shapes your destiny!\n"
            "There are up to 5 different endings waiting for you based on the paths you choose.\n\n"
            "🎮 How to Play and Have Amazing Adventures:\n"
            "- Simply type what you want to do in the input box below\n"
            "- Chat with fascinating characters, explore mysterious places, engage in epic battles\n"
            "- Make important decisions that will determine your hero's fate\n"
            "- At the start of each quest, you'll see beautiful pixel art that sets the scene\n"
            "- When dragons appear, you'll see incredible fire-breathing pixel art!\n"
            "- Your AI Dungeon Master will guide you, but YOU control your own epic story\n"
            "- Most importantly: Have fun and let your imagination run wild!\n"
            "\n🌟 Your adventure awaits, brave hero!\n"
        )
        self.display_message(f"[🎭 Game Guide]\n{instructions}\n\n", tag="instructions")
    
    def __init__(self):
        import os
        # Start fresh with each new adventure session
        char_file = os.path.join("memory_docs", "character.json")
        if os.path.exists(char_file):
            try:
                os.remove(char_file)  # Clean slate for new adventures
            except Exception:
                pass
        super().__init__()
        self.title(GUI_TITLE)
        self.geometry("1200x800")
        # Make it look absolutely amazing
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        # Initialize the storytelling engine
        self.engine = StorytellingEngine()
        # UI state
        self.character_created = self.engine.has_character()
        self.adventure_started = False
        # Queue for threading
        self.ui_queue = queue.Queue()
        self.setup_ui()
        # Start processing queue
        self.after(100, self.process_queue)
        # If character exists, update status
        if self.character_created:
            self._update_character_info()
    
    def setup_ui(self):
        """Setup the user interface with sidebar design"""
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")
        self.sidebar_frame.grid_rowconfigure(2, weight=1)
        
        # Character Frame
        self.character_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.character_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.char_label = ctk.CTkLabel(self.character_frame, text="Character", font=ctk.CTkFont(size=20, weight="bold"))
        self.char_label.pack(anchor="w", pady=(0, 5))
        
        self.char_info_text = ctk.CTkLabel(self.character_frame, text="No character created", justify="left", font=("Arial", 12), wraplength=220)
        self.char_info_text.pack(anchor="w", pady=5)
        
        # Character creation UI (main window, not popup)
        self.name_entry = ctk.CTkEntry(self.character_frame, width=200, placeholder_text="Enter character name")
        self.name_entry.pack(pady=5)
        self.create_char_btn = ctk.CTkButton(self.character_frame, text="Create Character", command=self.create_character_main)
        self.create_char_btn.pack(pady=5)
        
        # NPCs Frame
        self.npc_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.npc_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.npc_label = ctk.CTkLabel(self.npc_frame, text="NPCs", font=ctk.CTkFont(size=20, weight="bold"))
        self.npc_label.pack(anchor="w", pady=(0, 5))
        
        self.npc_info_frame = ctk.CTkFrame(self.npc_frame)
        self.npc_info_frame.pack(fill="x", pady=5)
        
        # Memory info
        self.memory_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent") 
        self.memory_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.memory_label = ctk.CTkLabel(self.memory_frame, text="Memory", font=ctk.CTkFont(size=16, weight="bold"))
        self.memory_label.pack(anchor="w", pady=(0, 5))
        
        self.memory_info_text = ctk.CTkLabel(self.memory_frame, text="0 conversations\n0 facts", justify="left", font=("Arial", 10))
        self.memory_info_text.pack(anchor="w")
        
        # Main chat area
        self.chat_frame = ctk.CTkFrame(self, corner_radius=10)
        self.chat_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        # Chat display with colored text support
        self.textbox = ctk.CTkTextbox(self.chat_frame, state="disabled", wrap="word", font=("Arial", 14))
        self.textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Store the textbox for easier access to underlying widget
        self.text_widget = None
        
        # Configure text colors after the widget is created
        def setup_colors():
            try:
                # Try different methods to access the underlying text widget
                if hasattr(self.textbox, '_textbox'):
                    self.text_widget = self.textbox._textbox
                elif hasattr(self.textbox, 'textbox'):
                    self.text_widget = self.textbox.textbox
                else:
                    # Search for Text widget in children
                    for child in self.textbox.winfo_children():
                        if child.winfo_class() == 'Text':
                            self.text_widget = child
                            break
                
                if self.text_widget:
                    self.text_widget.tag_config("player", foreground="#00BFFF")     # Bright blue for player
                    self.text_widget.tag_config("dm", foreground="#32CD32")         # Lime green for DM
                    self.text_widget.tag_config("instructions", foreground="#FFA500")  # Orange for instructions
                    self.text_widget.tag_config("quest_name", foreground="#FF69B4")    # Hot pink for quest names
                    self.text_widget.tag_config("error", foreground="#FF4444")         # Bright red for errors
                    print("✨ Color tags configured successfully!")
                else:
                    print("⚠️ Could not find underlying text widget")
            except Exception as e:
                print(f"⚠️ Could not configure text colors: {e}")
        
        # Schedule color setup after widget is fully initialized
        self.after(100, setup_colors)
        
        # Input area
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Start adventure button
        self.start_btn = ctk.CTkButton(self.input_frame, text="Start Adventure", command=self.start_adventure)
        self.start_btn.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")
        
        # Action input
        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="What do you do?", font=("Arial", 14))
        self.entry.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="ew")
        self.entry.bind("<Return>", self.send_message)
        
        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message, width=80)
        self.send_button.grid(row=1, column=1, pady=5, sticky="e")
        
        # Status label
        self.status_label = ctk.CTkLabel(self.input_frame, text="")
        
        # Initially disable inputs if no character
        if not self.character_created:
            self.entry.configure(state="disabled")
            self.send_button.configure(state="disabled")
            self.start_btn.configure(state="disabled")
    
    def create_character_main(self):
        """Create character from main window entry, assign random attributes"""
        import random
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a character name!")
            return
        background = "A mysterious adventurer."
        personality = "Brave and curious."
        goals = "To complete the quests."
        attributes = {
            'strength': random.randint(8, 18),
            'dexterity': random.randint(8, 18),
            'intelligence': random.randint(8, 18),
            'charisma': random.randint(8, 18)
        }
        try:
            result = self.engine.create_character(name, background, personality, goals, **attributes)
            messagebox.showinfo("Success", result)
            self.character_created = True
            self._update_character_info()
            self.name_entry.configure(state="disabled")
            self.create_char_btn.configure(state="disabled")
            self.entry.configure(state="normal")
            self.send_button.configure(state="normal")
            self.start_btn.configure(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create character: {e}")
    
    def _update_character_info(self):
        """Update character information display"""
        char_info = self.engine.get_character_info()
        if char_info:
            info_text = f"Name: {char_info['name']}\nClass: Fighter\nStr: {char_info['attributes'].get('strength', 10)}\nDex: {char_info['attributes'].get('dexterity', 10)}\nInt: {char_info['attributes'].get('intelligence', 10)}\nCha: {char_info['attributes'].get('charisma', 10)}"
            self.char_info_text.configure(text=info_text)
            self.create_char_btn.configure(text="Edit Character")
    
    def _update_npc_info(self, npc_states):
        """Update NPC information display for currently present NPCs"""
        # Clear existing NPC widgets
        for widget in self.npc_info_frame.winfo_children():
            widget.destroy()
        
        if not npc_states:
            no_npc_label = ctk.CTkLabel(self.npc_info_frame, text="No NPCs present", font=("Arial", 10))
            no_npc_label.pack(pady=2)
            return
        
        # Add header
        header_label = ctk.CTkLabel(self.npc_info_frame, text="Currently Present:", font=ctk.CTkFont(size=12, weight="bold"))
        header_label.pack(anchor="w", padx=5, pady=(0, 5))
        
        for npc_name, data in npc_states.items():
            npc_frame = ctk.CTkFrame(self.npc_info_frame)
            npc_frame.pack(fill="x", pady=2)
            
            name_label = ctk.CTkLabel(npc_frame, text=npc_name, font=ctk.CTkFont(weight="bold"))
            name_label.pack(anchor="w", padx=5)
            
            info_text = f"{data['occupation'].title()}\n{data['emotion']} ({data['score']:+d})"
            info_label = ctk.CTkLabel(npc_frame, text=info_text, font=("Arial", 10), justify="left")
            info_label.pack(anchor="w", padx=5, pady=(0, 5))
    
    def _update_memory_info(self):
        """Update memory information display"""
        try:
            memory_info = self.engine.get_memory_summary()
            info_text = f"{memory_info['total_conversations']} conversations\n{memory_info['total_facts']} facts"
            self.memory_info_text.configure(text=info_text)
        except Exception:
            pass
    
    def start_adventure(self):
        """Start the adventure with DM instructions and quest art in main chat area"""
        if not self.character_created:
            messagebox.showerror("Error", "Please create a character first!")
            return
        self.show_game_instructions()
        self.start_btn.configure(state="disabled", text="Starting...")
        self.show_status("Starting adventure...")
        def start_thread():
            try:
                quests = self.engine.get_plot()
                first_quest = quests[0]
                self.display_quest_name(first_quest)
                intro = self.engine.start_adventure()
                self.ui_queue.put(("dm_response", intro))
                self.ui_queue.put(("adventure_started", True))
            except Exception as e:
                self.ui_queue.put(("error", f"Failed to start adventure: {e}"))
        Thread(target=start_thread, daemon=True).start()

    def display_quest_name(self, quest):
        """Show only the creative quest name in the main chat area before each quest"""
        quest_names = {
            "dragon": "The Ember Maw Awakens",
            "artifact": "Relic of the Forgotten Mind",
            "battle": "The Shattered Arena"
        }
        art_type = quest.get("art", "battle")
        name = quest_names.get(art_type, quest["title"])
        self.display_message(f"[Quest: {name}]\n\n", tag="quest_name")
    
    def send_message(self, event=None):
        """Send a message"""
        if not self.adventure_started:
            return
        
        message = self.entry.get().strip()
        if not message:
            return
        
        self.entry.delete(0, "end")
        self.send_button.configure(state="disabled")
        self.show_status("DM is thinking...")
        
        # Add player message to display with nice formatting and visual distinction
        player_prefix = "🔵 YOU: "  # Blue circle to indicate player
        self.display_message(f"{player_prefix}{message}\n\n", "player")
        
        def process_thread():
            try:
                response = self.engine.process_player_action(message)
                self.ui_queue.put(("dm_response", response))
                self.ui_queue.put(("update_npcs", None))
            except Exception as e:
                self.ui_queue.put(("error", f"Error: {e}"))
        
        Thread(target=process_thread, daemon=True).start()
    
    def display_message(self, message, tag=""):
        """✨ Display a message in the chat with beautiful colors!"""
        self.textbox.configure(state="normal")
        
        if tag and self.text_widget:
            try:
                # Insert with color tag for different speakers using the underlying text widget
                start_pos = self.text_widget.index("end-1c")  # Get position before inserting
                self.textbox.insert("end", message)
                end_pos = self.text_widget.index("end-1c")    # Get position after inserting
                self.text_widget.tag_add(tag, start_pos, end_pos)  # Apply color tag
            except Exception as e:
                print(f"⚠️ Color tagging failed, using default: {e}")
                # Fallback: just insert without color
                self.textbox.insert("end", message)
        else:
            # Default text (no color or no text widget found)
            self.textbox.insert("end", message)
            
        self.textbox.see("end")
        self.textbox.configure(state="disabled")
    
    def show_status(self, message):
        """Show status message"""
        self.status_label.configure(text=message)
        self.status_label.grid(row=2, column=0, columnspan=2, pady=5)
    
    def hide_status(self):
        """Hide status message"""
        self.status_label.grid_forget()
        self.send_button.configure(state="normal")
    
    def process_queue(self):
        """Process UI queue for thread communication"""
        try:
            while True:
                message_type, content = self.ui_queue.get_nowait()
                
                if message_type == "dm_response":
                    dm_prefix = "🟢 DM: "  # Green circle to indicate DM
                    self.display_message(f"{dm_prefix}{content}\n\n", "dm")
                    self.hide_status()
                elif message_type == "adventure_started":
                    self.adventure_started = True
                    self.start_btn.configure(text="Adventure in Progress", state="disabled")
                    self.entry.focus()
                elif message_type == "update_npcs":
                    # Get current NPCs instead of all NPCs
                    current_npc_states = self.engine.get_current_npc_states()
                    self._update_npc_info(current_npc_states)
                    self._update_memory_info()
                elif message_type == "error":
                    # Show error in chat as well as popup
                    self.display_message(f"⚠️ Error: {content}\n\n", "error")
                    messagebox.showerror("Error", content)
                    self.hide_status()
                    if not self.adventure_started:
                        self.start_btn.configure(state="normal", text="Start Adventure")
        except queue.Empty:
            pass
        
        self.after(100, self.process_queue)


class CharacterCreationDialog(ctk.CTkToplevel):
    """Character creation dialog"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.title("Create Character")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        
        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def setup_ui(self):
        """Setup character creation UI"""
        # Title
        title_label = ctk.CTkLabel(self, text="Create Your Character", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)
        
        # Name
        ctk.CTkLabel(self, text="Character Name:").pack(pady=(10, 5))
        self.name_entry = ctk.CTkEntry(self, width=300)
        self.name_entry.pack(pady=5)
        
        # Background
        ctk.CTkLabel(self, text="Background:").pack(pady=(10, 5))
        self.background_entry = ctk.CTkTextbox(self, width=300, height=60)
        self.background_entry.pack(pady=5)
        
        # Personality
        ctk.CTkLabel(self, text="Personality:").pack(pady=(10, 5))
        self.personality_entry = ctk.CTkTextbox(self, width=300, height=60)
        self.personality_entry.pack(pady=5)
        
        # Goals
        ctk.CTkLabel(self, text="Goals:").pack(pady=(10, 5))
        self.goals_entry = ctk.CTkTextbox(self, width=300, height=60)
        self.goals_entry.pack(pady=5)
        
        # Attributes (random, display only)
        attr_frame = ctk.CTkFrame(self)
        attr_frame.pack(pady=20)
        ctk.CTkLabel(attr_frame, text="Attributes (Random)", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        import random
        self.random_attributes = {
            'strength': random.randint(8, 18),
            'dexterity': random.randint(8, 18),
            'intelligence': random.randint(8, 18),
            'charisma': random.randint(8, 18)
        }
        for attr, value in self.random_attributes.items():
            attr_row = ctk.CTkFrame(attr_frame)
            attr_row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(attr_row, text=f"{attr.capitalize()}: {value}", width=120).pack(side="left", padx=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)
        
        ctk.CTkButton(button_frame, text="Create", command=self.create_character).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Cancel", command=self.destroy).pack(side="left", padx=10)
    
    def create_character(self):
        """Create the character (attributes random, name uneditable after creation)"""
        name = self.name_entry.get().strip()
        background = self.background_entry.get("1.0", "end").strip()
        personality = self.personality_entry.get("1.0", "end").strip()
        goals = self.goals_entry.get("1.0", "end").strip()
        if not all([name, background, personality, goals]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        attributes = self.random_attributes
        try:
            result = self.parent.engine.create_character(name, background, personality, goals, **attributes)
            messagebox.showinfo("Success", result)
            self.name_entry.configure(state="disabled")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create character: {e}")


def run_gui():
    """Run the GUI application"""
    app = StorytellerGUI()
    app.mainloop()


if __name__ == "__main__":
    run_gui()