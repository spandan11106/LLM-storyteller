import customtkinter as ctk
from threading import Thread
import queue

class ChatApp(ctk.CTk):
    def __init__(self, game_logic_runner):
        super().__init__()
        self.title("AI Dungeon Master")
        self.geometry("800x600")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(self, state="disabled", wrap="word", font=("Arial", 14))
        self.textbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.entry = ctk.CTkEntry(self, placeholder_text="What do you do?", font=("Arial", 14))
        self.entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.game_logic_runner = game_logic_runner
        self.ui_queue = queue.Queue()
        self.after(100, self.process_queue)
        
        self.textbox.tag_config("dm", foreground="#00FF00")
        self.textbox.tag_config("roll", foreground="#FFA500")

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            self.display_message(f"You: {message}\n\n", "user")
            self.entry.delete(0, "end")
            Thread(target=self.game_logic_runner, args=(message, self.ui_queue), daemon=True).start()

    def display_message(self, message, tag):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", message, tag)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def process_queue(self):
        try:
            message_type, content = self.ui_queue.get_nowait()
            if message_type == "dm_response":
                self.display_message(f"DM: {content}\n\n", "dm")
            elif message_type == "roll":
                self.display_message(f"🎲 {content}\n\n", "roll")
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_queue)

    def start_game(self):
        """Displays the initial welcome message."""
        welcome_text = "You find yourself in a dimly lit tavern...\n\nWhat do you do?\n"
        self.display_message(f"DM: {welcome_text}", "dm")