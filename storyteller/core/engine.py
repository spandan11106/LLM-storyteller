# storyteller/core/engine.py
"""
🎭 The Heart of Adventure - Your Personal Story Master!

This is where all the magic comes together! Think of this as your personal
dungeon master who never gets tired, always remembers every detail, and 
creates amazing adventures tailored just for you.

This engine combines character creation, memory management, and AI storytelling
to create truly immersive experiences that grow and evolve with every session!
"""

import json
from typing import Dict, Any, Optional

from .character import Character
from .memory import DocumentMemorySystem
from .npc import NPCManager
from ..utils.llm import llm_client


class StorytellingEngine:
    """🎪 Your Amazing Adventure Engine - Where Stories Come to Life!"""
    
    def get_plot(self):
        """🗺️ Get the epic quest structure: 15 amazing adventures that get progressively more challenging!"""
        quests = []
        for i in range(1, 16):
            theme = "Ancient Mysteries" if i <= 5 else "Future Worlds" if i >= 11 else "Medieval Legends"
            quest_type = "dragon" if i == 3 or i == 10 else "artifact" if i % 4 == 0 else "battle"
            quests.append({
                "number": i,
                "title": f"Quest {i}: {'Epic Dragon Battle' if quest_type == 'dragon' else 'Hunt for Lost Artifacts' if quest_type == 'artifact' else 'Legendary Battle'}",
                "theme": theme,
                "difficulty": i,
                "art": "dragon" if quest_type == "dragon" else "artifact" if quest_type == "artifact" else "battle"
            })
        return quests

    def get_possible_endings(self):
        """🏆 Discover the possible ways your epic story could conclude!"""
        return [
            "You become a legend that inspires generations to come!",
            "You become lost in time, your story becoming a mysterious tale!",
            "You rule the future with wisdom and compassion!",
            "You make the ultimate sacrifice to save the world you love!",
            "You retire peacefully, having changed history forever!"
        ]
    
    def __init__(self, memory_path: str = None):
        self.memory = DocumentMemorySystem(memory_path)  # Our amazing memory palace
        self.npc_manager = NPCManager()                   # All the characters you'll meet
        self.character: Optional[Character] = None        # Your heroic character
        self.game_started = False                         # Adventure status
        
        # Welcome back any returning heroes!
        self._load_character()
    
    def _load_character(self):
        """🔍 Look for any returning heroes who want to continue their adventure!"""
        try:
            memory_summary = self.memory.get_summary()
            # Check if we have a saved hero waiting to return
            import os
            char_file = os.path.join(self.memory.save_path, "character.json")
            if os.path.exists(char_file):
                with open(char_file, 'r') as f:
                    char_data = json.load(f)
                    self.character = Character.from_dict(char_data)
                    print(f"🎉 Welcome back, {self.character.name}! Ready for more adventures?")
        except Exception as e:
            print(f"📝 No returning hero found (that's fine - let's create a new one!): {e}")
    
    def _save_character(self):
        """💾 Carefully save your hero so they can return for future adventures!"""
        if not self.character:
            return
        
        try:
            import os
            char_file = os.path.join(self.memory.save_path, "character.json")
            with open(char_file, 'w') as f:
                json.dump(self.character.to_dict(), f, indent=2)
            print(f"✅ {self.character.name} is safely saved for future adventures!")
        except Exception as e:
            print(f"⚠️ Couldn't save character (but they're still active): {e}")
    
    def create_character(self, name: str, background: str, personality: str, goals: str, **attributes) -> str:
        """⚔️ Bring your amazing hero to life and prepare them for epic adventures!"""
        self.character = Character(name, background, personality, goals, attributes)
        self._save_character()
        self.game_started = False  # Fresh start for new adventures
        return f"🎉 Hero {name} is ready for adventure! Let the stories begin!"
    
    def has_character(self) -> bool:
        """🧙‍♂️ Check if we have a hero ready for adventures"""
        return self.character is not None
    
    def start_adventure(self) -> str:
        """🚀 Begin an epic adventure with your hero!"""
        if not self.character:
            return "Please create a character first!"
        
        character_info = self.character.get_description()
        intro = llm_client.generate_story_intro(character_info)
        
        # Add to memory
        self.memory.add_conversation_turn(
            f"[Character Created: {self.character.name}]", 
            intro
        )
        
        self.game_started = True
        return intro
    
    def process_player_action(self, action: str) -> str:
        """Process player action and generate DM response"""
        if not self.game_started:
            return "Please start an adventure first!"
        
        if not action.strip():
            return "Please tell me what you want to do."
        
        # Retrieve relevant memories
        relevant_memories = self.memory.retrieve_relevant_memories(action)
        memory_context = "\n".join(relevant_memories) if relevant_memories else "No relevant past events."
        
        # Get recent conversation context (last 3 turns)
        recent_context = ""
        if len(self.memory.conversation_history) > 0:
            recent_turns = self.memory.conversation_history[-3:]
            recent_context = "\n".join([
                f"Player: {turn.player_action}\nDM: {turn.dm_response}"
                for turn in recent_turns
            ])
        
        # Get NPC context
        npc_context = self.npc_manager.get_npc_context()
        
        character_info = self.character.get_description()
        
        # Generate DM response
        full_context = f"{character_info}\n\nNPC States:\n{npc_context}\n\nRecent Context:\n{recent_context}\n\nRelevant Memories:\n{memory_context}"
        dm_response = llm_client.continue_story(
            character_info, memory_context, recent_context, action
        )
        
        # Process NPCs mentioned in player action and update current NPCs
        self.npc_manager.update_current_npcs(action)
        mentioned_npcs = self.npc_manager.get_mentioned_npcs(action)
        if mentioned_npcs:
            tone = self.npc_manager.analyze_player_tone(action)
            for npc_name in mentioned_npcs:
                self.npc_manager.update_npc_emotion(npc_name, tone, action)
        
        # Extract new NPCs from DM response and update current NPCs
        self.npc_manager.process_dm_response_for_npcs(dm_response)
        
        # Add to memory
        self.memory.add_conversation_turn(action, dm_response)
        
        return dm_response
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of current memory state"""
        summary = self.memory.get_summary()
        summary['character'] = self.character.to_dict() if self.character else None
        summary['npcs'] = self.npc_manager.get_npc_states()
        summary['current_npcs'] = self.npc_manager.get_current_npc_states()
        return summary
    
    def get_character_info(self) -> Optional[Dict[str, Any]]:
        """Get current character information"""
        return self.character.to_dict() if self.character else None
    
    def get_npc_states(self) -> Dict[str, Dict[str, Any]]:
        """Get current NPC states (all NPCs for backward compatibility)"""
        return self.npc_manager.get_npc_states()
    
    def get_current_npc_states(self) -> Dict[str, Dict[str, Any]]:
        """Get states of NPCs currently present in the conversation"""
        return self.npc_manager.get_current_npc_states()