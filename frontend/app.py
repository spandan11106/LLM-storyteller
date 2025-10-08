import customtkinter as ctk
from threading import Thread
import queue

class ChatApp(ctk.CTk):
    def __init__(self, game_logic_runner):
        super().__init__()
        self.title("AI Dungeon Master")
        self.geometry("900x700")

        # Main layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Character Info Frame
        self.char_frame = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.char_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")
        self.char_frame.grid_propagate(False) # Prevent frame from shrinking
        
        self.char_label = ctk.CTkLabel(self.char_frame, text="Character", font=ctk.CTkFont(size=20, weight="bold"))
        self.char_label.pack(pady=10)
        
        self.char_info_text = ctk.CTkTextbox(self.char_frame, wrap="word", font=("Arial", 14), activate_scrollbars=False)
        self.char_info_text.pack(expand=True, fill="both", padx=10, pady=10)
        self.char_info_text.configure(state="disabled")

        # Main Chat Frame
        self.chat_frame = ctk.CTkFrame(self, corner_radius=10)
        self.chat_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        self.textbox = ctk.CTkTextbox(self.chat_frame, state="disabled", wrap="word", font=("Arial", 16))
        self.textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Input Frame
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        # Replaced CTkEntry with CTkTextbox for multiline input
        self.entry = ctk.CTkTextbox(self.input_frame, height=100, font=("Arial", 16))
        self.entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        
        # AI Status Label
        self.status_label = ctk.CTkLabel(self.input_frame, text="AI is thinking...", font=ctk.CTkFont(size=12))
        # Initially hidden, will be shown when waiting for AI
        
        self.game_logic_runner = game_logic_runner
        self.ui_queue = queue.Queue()
        self.after(100, self.process_queue)
        
        self.textbox.tag_config("dm", foreground="#00FF00")
        self.textbox.tag_config("roll", foreground="#FFA500")

    def send_message(self, event=None):
        # Allow Shift+Enter for new lines
        if event and event.state & 1: # 1 is the bitmask for Shift key
            return
        
        # Get text from the textbox
        message = self.entry.get("1.0", "end-1c").strip()
        if message:
            self.display_message(f"You: {message}\n\n", "user")
            # Clear the textbox
            self.entry.delete("1.0", "end")
            self.show_status("AI is thinking...")
            Thread(target=self.game_logic_runner, args=(message, self.ui_queue), daemon=True).start()
        
        return "break" # Prevents default Enter key behavior (like adding a newline)

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
        self.char_info_text.configure(state="normal")
        self.char_info_text.delete("1.0", "end")
        for key, value in info_dict.items():
            self.char_info_text.insert("end", f"{key.capitalize()}: {value}\n")
        self.char_info_text.configure(state="disabled")

    def start_game(self):
        """Displays the initial welcome message."""
        welcome_text = "You find yourself in a dimly lit tavern...\n\nWhat do you do?\n"
        self.display_message(f"DM: {welcome_text}", "dm")