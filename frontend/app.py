import customtkinter as ctk
from threading import Thread
import queue
from storyteller import config # Import config to use DND_RULES

class ChatApp(ctk.CTk):
    # --- FIX: Properly handle custom arguments in the constructor ---
    def __init__(self, *args, **kwargs):
        # Pop our custom arguments from kwargs before calling the parent class
        self.game_logic_runner = kwargs.pop('game_logic_runner', None)
        self.memory_manager = kwargs.pop('memory_manager', None)

        # Now, initialize the parent CTk class with any remaining standard arguments
        super().__init__(*args, **kwargs)

        # Assert that our required arguments were provided
        if not self.game_logic_runner or not self.memory_manager:
            raise ValueError("ChatApp requires 'game_logic_runner' and 'memory_manager' arguments.")

        self.title("AI Dungeon Master")
        self.geometry("900x700")
        
        # --- The rest of the __init__ method is the same ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        self.player_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.player_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        
        self.char_label = ctk.CTkLabel(self.player_frame, text="Character", font=ctk.CTkFont(size=20, weight="bold"))
        self.char_label.pack(anchor="w")
        
        self.char_info_text = ctk.CTkLabel(self.player_frame, text="", justify="left", font=("Arial", 14), wraplength=180)
        self.char_info_text.pack(anchor="w", pady=5)

        self.npc_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.npc_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.npc_label = ctk.CTkLabel(self.npc_frame, text="NPCs", font=ctk.CTkFont(size=20, weight="bold"))
        self.npc_label.pack(anchor="w")
        self.npc_widgets = {}

        self.chat_frame = ctk.CTkFrame(self, corner_radius=10)
        self.chat_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        self.textbox = ctk.CTkTextbox(self.chat_frame, state="disabled", wrap="word", font=("Arial", 16))
        self.textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkTextbox(self.input_frame, height=100, font=("Arial", 16))
        self.entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        
        self.status_label = ctk.CTkLabel(self.input_frame, text="AI is thinking...", font=ctk.CTkFont(size=12))
        
        self.ui_queue = queue.Queue()
        self.after(100, self.process_queue)
        
        self.textbox.tag_config("dm", foreground="#00FF00")
        self.textbox.tag_config("roll", foreground="#FFA500")

    def send_message(self, event=None):
        if event and event.state & 1:
            return
        
        message = self.entry.get("1.0", "end-1c").strip()
        if message:
            self.display_message(f"You: {message}\n\n", "user")
            self.entry.delete("1.0", "end")
            self.show_status("AI is thinking...")
            Thread(target=self.game_logic_runner, args=(message, self.ui_queue, self.memory_manager), daemon=True).start()
        
        return "break"

    def display_message(self, message, tag):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", message, tag)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def process_queue(self):
        try:
            message_type, content = self.ui_queue.get_nowait()
            if message_type == "dm_response":
                self.hide_status()
                self.display_message(f"DM: {content}\n\n", "dm")
            elif message_type == "roll":
                self.display_message(f"🎲 {content}\n\n", "roll")
            elif message_type == "update_char_info":
                self.update_character_info(content)
            elif message_type == "update_npc_info":
                self.update_npc_info(content)
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_queue)

    def show_status(self, message):
        self.status_label.configure(text=message)
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5)
        self.send_button.configure(state="disabled")

    def hide_status(self):
        self.status_label.grid_forget()
        self.send_button.configure(state="normal")

    def update_character_info(self, info_dict):
        """Updates the character info panel."""
        info_str = ""
        if "name" in info_dict and "class" in info_dict:
            info_str += f"Name: {info_dict['name']}\n"
            info_str += f"Class: {info_dict['class']}\n"
        
        p_class = info_dict.get("class")
        if p_class:
            class_info = config.DND_RULES["classes"].get(p_class, {})
            mod = class_info.get("modifier")
            if mod:
                val = info_dict.get(mod, 0)
                info_str += f"{mod.capitalize()}: {val}\n"

        if "state" in info_dict:
            info_str += f"State: {info_dict['state']}\n"
        
        self.char_info_text.configure(text=info_str)


    def update_npc_info(self, npc_data: dict):
        """Dynamically updates the NPC list in the sidebar."""
        for npc_name, data in npc_data.items():
            score = data.get("score")
            emotion = data.get("emotion")
            info_str = f"Score: {score}\nEmotion: {emotion}"
            
            if npc_name not in self.npc_widgets:
                frame = ctk.CTkFrame(self.npc_frame)
                frame.pack(fill="x", pady=5, anchor="n")
                name_label = ctk.CTkLabel(frame, text=npc_name, font=ctk.CTkFont(weight="bold"))
                name_label.pack(anchor="w", padx=5)
                info_label = ctk.CTkLabel(frame, text=info_str, justify="left")
                info_label.pack(anchor="w", padx=5)
                self.npc_widgets[npc_name] = info_label
            else:
                self.npc_widgets[npc_name].configure(text=info_str)

    def start_game(self):
        """Displays the initial welcome message."""
        welcome_text = "You find yourself in a dimly lit tavern...\n\nWhat do you do?\n"
        self.display_message(f"DM: {welcome_text}", "dm")