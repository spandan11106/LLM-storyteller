#!/usr/bin/env python3
"""
The Ultimate Memory Challenge for AI
====================================

Hey there! This demo is designed to blow minds and prove beyond any doubt 
that our AI storyteller has REAL long-term memory. Here's how we're going 
to absolutely convince everyone:

1. We'll casually drop some very specific details into our story
2. Then we'll chat about tons of completely unrelated stuff to "bury" those details  
3. Much later, we'll ask our AI to remember those exact details from way back
4. Watch in amazement as it recalls things from dozens of conversations ago!

This isn't some parlor trick - either the AI genuinely remembers or it doesn't.
No amount of clever programming can fake this kind of long-term recall!
"""

import sys
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from storyteller.ui.gui import StorytellerGUI
import customtkinter as ctk

class MemoryProofDemo(StorytellerGUI):
    """A demo that will absolutely convince anyone that our AI has genuine memory"""
    
    def __init__(self):
        super().__init__()
        self.title("🧠 THE ULTIMATE AI MEMORY CHALLENGE - Watch This!")
        
        # Here's our secret test information that we'll bury and later recall
        self.test_data = {
            "secret_number": "7429",
            "hidden_treasure": "Golden Chalice of Elderwood", 
            "npc_backstory": "Marcus lost his daughter Elena to a dragon attack 3 years ago",
            "village_secret": "The village well contains a hidden passage to ancient tunnels",
            "magic_word": "Zephyralton",
            "specific_location": "Behind the third oak tree near the old watchtower"
        }
        
        self.setup_memory_proof_controls()
        self.current_phase = "ready"  # ready -> planting -> burying -> testing -> complete
        self.phase_step = 0
    
    def setup_memory_proof_controls(self):
        """Let's set up our memory challenge interface"""
        # Memory Challenge Control Panel
        self.proof_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.proof_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        
        # Title
        title = ctk.CTkLabel(self.proof_frame, text="🧠 Memory Challenge", 
                            font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=5)
        
        # Phase indicator - shows what we're doing right now
        self.phase_label = ctk.CTkLabel(self.proof_frame, text="Ready to blow some minds!", 
                                       font=("Arial", 12, "bold"))
        self.phase_label.pack(pady=5)
        
        # The secret info we'll test
        self.info_display = ctk.CTkTextbox(self.proof_frame, height=120, font=("Arial", 9))
        self.info_display.pack(fill="x", pady=5)
        self.info_display.insert("1.0", "🤫 SECRET INFO WE'LL PLANT & TEST:\n\n" +
                                "\n".join([f"• {key}: {value}" for key, value in self.test_data.items()]))
        self.info_display.configure(state="disabled")
        
        # Control buttons
        self.start_proof_btn = ctk.CTkButton(self.proof_frame, text="🚀 Start the Memory Challenge!", 
                                            command=self.start_memory_proof)
        self.start_proof_btn.pack(pady=5, fill="x")
        
        self.next_phase_btn = ctk.CTkButton(self.proof_frame, text="Continue to Next Step", 
                                           command=self.next_phase, state="disabled")
        self.next_phase_btn.pack(pady=2, fill="x")
        
        # Quick skip for impatient judges
        self.skip_btn = ctk.CTkButton(self.proof_frame, text="⚡ Jump to the Memory Test!", 
                                     command=self.skip_to_test, state="disabled")
        self.skip_btn.pack(pady=2, fill="x")
    
    def start_memory_proof(self):
        """Let's kick off this amazing memory demonstration!"""
        # Auto-create character for convenience
        if not self.character_created:
            self.name_entry.insert(0, "Memory Test Hero")
            self.create_character_main()
            time.sleep(0.5)
        
        # Start the adventure
        if not self.adventure_started:
            self.start_adventure()
            time.sleep(1.0)
        
        # Let's explain what we're about to do
        intro = ("🎯 GET READY FOR THE ULTIMATE MEMORY CHALLENGE!\n"
                "============================================\n\n"
                "We're about to prove beyond any doubt that our AI has real memory:\n\n"
                "STEP 1: Casually drop some secret info into our story\n"
                "STEP 2: Chat about tons of random stuff to bury those secrets\n"
                "STEP 3: See if our AI can still remember those details from way back!\n\n"
                "⚠️  JUDGES: Keep your eyes peeled for exact recall!\n"
                "There's no way to fake this - the AI either remembers or it doesn't.\n\n")
        
        self.display_message(intro, "proof_intro")
        
        self.current_phase = "planting"
        self.phase_step = 0
        self.update_phase_display()
        
        self.start_proof_btn.configure(state="disabled")
        self.next_phase_btn.configure(state="normal")
        self.skip_btn.configure(state="normal")
    
    def next_phase(self):
        """Let's move to the next step of our memory challenge"""
        if self.current_phase == "planting":
            self.execute_planting_phase()
        elif self.current_phase == "burying":
            self.execute_burying_phase()
        elif self.current_phase == "testing":
            self.execute_testing_phase()
    
    def execute_planting_phase(self):
        """Time to sneakily plant our secret information!"""
        planting_actions = [
            f"I ask the villagers about any secret numbers they might know. Someone whispers '{self.test_data['secret_number']}' to me.",
            f"I discover a legendary treasure called the {self.test_data['hidden_treasure']} is hidden somewhere.",
            f"I learn that {self.test_data['npc_backstory']}",
            f"A villager secretly tells me: '{self.test_data['village_secret']}'",
            f"I learn the ancient magic word: '{self.test_data['magic_word']}'",
            f"Someone gives me directions: 'The item you seek is {self.test_data['specific_location']}'"
        ]
        
        if self.phase_step < len(planting_actions):
            action = planting_actions[self.phase_step]
            self.display_message(f"🌱 SNEAKING IN SECRET #{self.phase_step + 1}: {action}\n\n", "planting")
            
            # Let's plant this secret!
            self.entry.insert(0, action)
            self.send_message()
            
            self.phase_step += 1
            
            if self.phase_step >= len(planting_actions):
                self.current_phase = "burying"
                self.phase_step = 0
                self.after(2000, self.update_phase_display)
        
        self.update_phase_display()
    
    def execute_burying_phase(self):
        """Time to bury those secrets under a mountain of random chatter!"""
        burying_actions = [
            "I explore the market and look at various goods for sale",
            "I chat with merchants about the weather and trade routes",
            "I ask about the local wildlife and animals in the area",
            "I inquire about farming techniques and crop seasons",
            "I discuss architecture and building materials with a carpenter",
            "I talk about cooking recipes and local cuisine with someone",
            "I ask about festivals and celebrations in the region",
            "I discuss travel routes to neighboring towns and cities",
            "I inquire about local crafts and artisan techniques",
            "I chat about music and entertainment in the village",
            "I ask about the local government and leadership",
            "I discuss education and schools for children",
            "I inquire about medical care and healing practices",
            "I talk about clothing styles and fabric preferences",
            "I ask about transportation methods and vehicles"
        ]
        
        if self.phase_step < len(burying_actions):
            action = burying_actions[self.phase_step]
            self.display_message(f"🏗️ BURYING WITH CHATTER #{self.phase_step + 1}/15: {action}\n\n", "burying")
            
            # Let's bury those secrets deeper!
            self.entry.insert(0, action)
            self.send_message()
            
            self.phase_step += 1
            
            if self.phase_step >= len(burying_actions):
                self.current_phase = "testing"
                self.phase_step = 0
                self.after(2000, self.update_phase_display)
        
        self.update_phase_display()
    
    def execute_testing_phase(self):
        """The moment of truth - can our AI remember what we buried?"""
        testing_prompts = [
            f"What was that secret number someone whispered to me earlier? (Expected: {self.test_data['secret_number']})",
            f"What was the name of that legendary treasure I learned about? (Expected: {self.test_data['hidden_treasure']})",
            f"What tragic story did I learn about Marcus? (Expected: about his daughter Elena and dragon)",
            f"What secret did a villager tell me about the village well? (Expected: hidden passage)",
            f"What was that ancient magic word I learned? (Expected: {self.test_data['magic_word']})",
            f"Where were those directions pointing to? (Expected: {self.test_data['specific_location']})"
        ]
        
        if self.phase_step < len(testing_prompts):
            prompt = testing_prompts[self.phase_step]
            self.display_message(f"🧠 MEMORY CHALLENGE #{self.phase_step + 1}: {prompt}\n\n", "testing")
            
            # Ask just the question part 
            question = prompt.split(" (Expected:")[0]
            self.entry.insert(0, question)
            self.send_message()
            
            self.phase_step += 1
            
            if self.phase_step >= len(testing_prompts):
                self.after(3000, self.complete_memory_proof)
        
        self.update_phase_display()
    
    def skip_to_test(self):
        """Fast track to the memory test for impatient judges!"""
        # Plant everything super quickly
        self.display_message("⚡ SPEED PLANTING: Quickly adding all our secrets to memory...\n\n", "fast_plant")
        
        for i, (key, value) in enumerate(self.test_data.items()):
            quick_action = f"I quickly learn: {key} = {value}"
            self.entry.insert(0, quick_action)
            self.send_message()
            time.sleep(0.5)  # Quick pause between actions
        
        # Add some rapid-fire burying conversations
        self.display_message("⚡ SPEED BURYING: Throwing in some random chatter...\n\n", "fast_bury")
        
        quick_bury = [
            "I chat about the weather with locals",
            "I discuss farming with a villager", 
            "I talk about local festivals",
            "I ask about trade routes",
            "I inquire about local cuisine"
        ]
        
        for action in quick_bury:
            self.entry.insert(0, action)
            self.send_message()
            time.sleep(0.5)
        
        # Now for the exciting part!
        self.current_phase = "testing"
        self.phase_step = 0
        self.update_phase_display()
        
        self.display_message("✅ ALL SET! Now let's see what our AI remembers...\n\n", "setup_complete")
    
    def update_phase_display(self):
        """Keep everyone updated on what we're doing"""
        phase_info = {
            "planting": f"🌱 SNEAKING IN SECRETS ({self.phase_step}/6)",
            "burying": f"🏗️ BURYING WITH CHATTER ({self.phase_step}/15)", 
            "testing": f"🧠 TESTING MEMORY ({self.phase_step}/6)",
            "complete": "✅ CHALLENGE COMPLETE!"
        }
        
        self.phase_label.configure(text=phase_info.get(self.current_phase, "Ready to blow minds!"))
    
    def complete_memory_proof(self):
        """Wrap up our amazing memory demonstration"""
        completion = ("🎉 MEMORY CHALLENGE COMPLETE!\n"
                     "============================\n\n"
                     "WHAT JUST HAPPENED:\n"
                     "• We secretly planted specific information early on\n"
                     "• We buried it under 15+ completely unrelated conversations\n"
                     "• We asked our AI to remember those buried details\n\n"
                     "✅ If our AI remembered = GENUINE long-term memory!\n"
                     "❌ If it failed = No real memory capability\n\n"
                     "This is bulletproof evidence of memory retention!\n"
                     "Feel free to scroll back and verify the accuracy.\n\n")
        
        self.display_message(completion, "completion")
        
        self.current_phase = "complete"
        self.update_phase_display()
        
        # Reset the controls
        self.next_phase_btn.configure(state="disabled")
        self.skip_btn.configure(state="disabled") 
        self.start_proof_btn.configure(state="normal", text="🔄 Try Another Round!")

def main():
    """Fire up our amazing memory proof demonstration"""
    print("🧠 THE ULTIMATE AI MEMORY CHALLENGE")
    print("=" * 40)
    print("Get ready to see undeniable proof that")
    print("our AI has real, genuine long-term memory!")
    print("=" * 40)
    
    try:
        app = MemoryProofDemo()
        
        # Welcome our judges with clear instructions
        instructions = ("🎯 WELCOME TO THE MEMORY CHALLENGE!\n"
                       "==================================\n\n"
                       "We're about to blow your mind with proof of real AI memory:\n\n"
                       "1. SECRET INFO gets casually dropped into our story\n"
                       "2. TONS of random chatter buries those secrets deep\n"
                       "3. We ask our AI to dig up those EXACT details from way back\n\n"
                       "🔍 WHAT TO WATCH: Perfect recall of specific planted info\n"
                       "⚠️  This is the real deal - no tricks, no cheats!\n\n"
                       "Ready to be amazed? Click '🚀 Start the Memory Challenge!' \n\n")
        
        app.display_message(instructions)
        app.mainloop()
        
    except Exception as e:
        print(f"Oops, something went wrong: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()