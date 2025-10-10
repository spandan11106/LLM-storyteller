# storyteller/core/npc.py
"""
🎭 The Character Workshop - Where Amazing NPCs Come to Life!

This is where all the fascinating characters in your story live and grow!
Each character has their own personality, emotions, and memories. They react
to how you treat them and remember your interactions, making every conversation
feel real and meaningful. It's like having a whole world of living characters!
"""

import re
from typing import Dict, Any, List, Set
from ..config import LLM_MODEL
from ..utils.llm import llm_client


class NPCManager:
    """🎪 Your Amazing Character Director - Bringing NPCs to Life with Personality!"""
    
    def __init__(self):
        self.npcs: Dict[str, Dict[str, Any]] = {}  # Our collection of amazing characters
        self.current_npcs: Set[str] = set()         # Who's in the current scene
        
        # How different ways of talking affect character relationships
        self.tone_effects = {
            "Polite": 5,        # People love good manners!
            "Friendly": 3,      # Friendliness goes a long way
            "Neutral": 0,       # Just normal conversation
            "Rude": -10,        # Nobody likes being treated badly
            "Threatening": -20, # This really upsets people
            "Aggressive": -15   # Aggression pushes people away
        }
        
        # Words we ignore when looking for character names
        self.excluded_words = {
            'you', 'your', 'yours', 'yourself', 'we', 'us', 'our', 'ours', 'ourselves',
            'they', 'them', 'their', 'theirs', 'themselves', 'he', 'him', 'his', 'himself',
            'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'i', 'me', 'my',
            'mine', 'myself', 'the', 'a', 'an', 'and', 'or', 'but', 'so', 'yet', 'for',
            'nor', 'to', 'in', 'on', 'at', 'by', 'up', 'of', 'as', 'is', 'am', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
            'this', 'that', 'these', 'those', 'here', 'there', 'where', 'when', 'why',
            'how', 'what', 'which', 'who', 'whom', 'whose', 'if', 'then', 'else',
            'while', 'until', 'since', 'because', 'although', 'though', 'unless',
            'before', 'after', 'during', 'within', 'without', 'between', 'among',
            'through', 'across', 'over', 'under', 'above', 'below', 'beside', 'behind',
            'front', 'back', 'left', 'right', 'north', 'south', 'east', 'west',
            'yes', 'no', 'not', 'never', 'always', 'sometimes', 'often', 'rarely',
            'much', 'many', 'few', 'little', 'more', 'most', 'less', 'least',
            'all', 'some', 'any', 'each', 'every', 'both', 'either', 'neither',
            'first', 'second', 'third', 'last', 'next', 'previous', 'new', 'old',
            'good', 'bad', 'big', 'small', 'long', 'short', 'high', 'low', 'hot', 'cold'
        }
    
    def initialize_npc(self, name: str, occupation: str = "unknown", **attributes):
        """🌟 Welcome a new character to our amazing story world!"""
        self.npcs[name] = {
            "name": name,
            "occupation": occupation,
            "relationship_score": 0,      # How much they like you (-100 to +100)
            "emotional_state": "Neutral", # How they're feeling right now
            "last_interaction": None,     # What you last said to them
            "times_mentioned": 0,         # How often they appear in your story
            **attributes                  # Any other cool traits they have
        }
        print(f"🎭 {name} the {occupation} has joined your story!")
    
    def analyze_player_tone(self, player_input: str) -> str:
        """🎯 Figure out how you're talking to the characters - are you being nice?"""
        input_lower = player_input.lower()
        
        # Words that show you're being polite and respectful
        polite_words = ["please", "thank you", "excuse me", "sorry", "may i", "could you"]
        # Words that might hurt someone's feelings
        rude_words = ["shut up", "stupid", "idiot", "get out", "go away"]
        # Words that would definitely scare someone
        threatening_words = ["kill", "hurt", "attack", "threaten", "fight", "die"]
        # Words that show you're being friendly and kind
        friendly_words = ["hello", "hi", "friend", "help", "kind", "nice"]
        
        if any(word in input_lower for word in threatening_words):
            return "Threatening"  # Yikes! That's scary talk!
        elif any(word in input_lower for word in rude_words):
            return "Rude"         # Not very nice...
        elif any(word in input_lower for word in polite_words):
            return "Polite"       # Such good manners!
        elif any(word in input_lower for word in friendly_words):
            return "Friendly"     # How nice and welcoming!
        else:
            return "Neutral"      # Just normal conversation
    
    def update_npc_emotion(self, npc_name: str, tone: str, interaction_text: str = ""):
        """💭 Update how a character feels about you based on your interaction!"""
        if npc_name not in self.npcs:
            self.initialize_npc(npc_name)  # Welcome the new character!
        
        npc = self.npcs[npc_name]
        
        # Characters remember how you treat them
        score_change = self.tone_effects.get(tone, 0)
        npc["relationship_score"] += score_change
        npc["last_interaction"] = interaction_text
        
        # Determine emotional state based on relationship score
        score = npc["relationship_score"]
        if score > 50:
            emotion = "Adoring"
        elif score > 20:
            emotion = "Friendly"
        elif score > 10:
            emotion = "Pleased"
        elif score > -10:
            emotion = "Neutral"
        elif score > -30:
            emotion = "Annoyed"
        elif score > -50:
            emotion = "Angry"
        else:
            emotion = "Hostile"
        
        npc["emotional_state"] = emotion
        
        return npc
    
    def get_mentioned_npcs(self, text: str) -> List[str]:
        """Find NPCs mentioned in text"""
        mentioned = []
        for npc_name in self.npcs.keys():
            if re.search(r'\b' + re.escape(npc_name) + r'\b', text, re.IGNORECASE):
                mentioned.append(npc_name)
                # Track that this NPC was mentioned
                self.npcs[npc_name]["times_mentioned"] += 1
        return mentioned
    
    def update_current_npcs(self, text: str):
        """Update which NPCs are currently present in the conversation with enhanced detection"""
        # Clear current NPCs
        self.current_npcs.clear()
        
        # Add NPCs that are mentioned in the current text
        mentioned = self.get_mentioned_npcs(text)
        self.current_npcs.update(mentioned)
        
        # Enhanced presence indicators with more comprehensive patterns
        presence_indicators = [
            # Direct presence/arrival
            r'(\w+)\s+(?:approaches?|walks?\s+(?:up|over|toward)|comes?\s+(?:forward|closer|over))',
            r'(\w+)\s+(?:enters?|arrives?|appears?|emerges?|steps?\s+(?:forward|out))',
            r'(\w+)\s+(?:stands?|sits?|waits?|remains?|stays?)\s+(?:nearby|here|there|close)',
            
            # Visual/perceptual presence
            r'(?:you\s+(?:see|notice|spot|observe|watch))\s+(\w+)',
            r'(?:there\s+(?:is|stands?|sits?))\s+(\w+)',
            r'(\w+)\s+(?:is|was)\s+(?:standing|sitting|waiting|here|there|nearby)',
            
            # Communication/interaction
            r'(\w+)\s+(?:says?|tells?|asks?|responds?|replies?|whispers?|shouts?|calls?)',
            r'(?:talk|speak|chat|converse)\s+(?:to|with)\s+(\w+)',
            r'(\w+)\s+(?:nods?|smiles?|frowns?|laughs?|sighs?|gestures?)',
            
            # Actions indicating presence
            r'(\w+)\s+(?:gives?|hands?|offers?|shows?|presents?)',
            r'(\w+)\s+(?:takes?|grabs?|picks?|accepts?|receives?)',
            r'(\w+)\s+(?:looks?|stares?|glances?|gazes?)\s+(?:at|toward)',
            r'(\w+)\s+(?:points?|gestures?|waves?|beckons?)',
            
            # Movement while present
            r'(\w+)\s+(?:moves?|shifts?|turns?|leans?|steps?)',
            r'(\w+)\s+(?:follows?|leads?|accompanies?)',
            
            # Departure indicators (remove from current)
            r'(\w+)\s+(?:leaves?|departs?|goes?\s+away|walks?\s+away|disappears?)',
            r'(\w+)\s+(?:exits?|retreats?|flees?|runs?\s+away)',
        ]
        
        departure_patterns = [
            r'(\w+)\s+(?:leaves?|departs?|goes?\s+away|walks?\s+away|disappears?)',
            r'(\w+)\s+(?:exits?|retreats?|flees?|runs?\s+away)',
            r'(\w+)\s+(?:is\s+gone|has\s+left|vanishes?)',
        ]
        
        # Check for departing NPCs first (to remove them)
        departing_npcs = set()
        for pattern in departure_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                name = match if isinstance(match, str) else match[0] if match else ""
                if name and name.capitalize() in self.npcs:
                    departing_npcs.add(name.capitalize())
        
        # Check for present NPCs
        for pattern in presence_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                name = match if isinstance(match, str) else match[0] if match else ""
                
                if name and len(name) > 2:
                    name = name.capitalize()
                    # Only add if it's a known NPC and not departing
                    if name in self.npcs and name not in departing_npcs:
                        self.current_npcs.add(name)
        
        # Remove departing NPCs from current set
        self.current_npcs -= departing_npcs
        
        # Also check for NPCs being referenced in dialogue or actions
        dialogue_patterns = [
            r'\"[^\"]*(\w+)[^\"]*\"',  # NPCs mentioned in quoted dialogue
            r'(?:about|regarding|concerning)\s+(\w+)',  # "talking about Marcus"
            r'(?:with|alongside|beside)\s+(\w+)',  # "standing with Elena"
        ]
        
        for pattern in dialogue_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                name = match if isinstance(match, str) else match[0] if match else ""
                if name and name.capitalize() in self.npcs:
                    self.current_npcs.add(name.capitalize())
    
    def get_current_npc_states(self) -> Dict[str, Dict[str, Any]]:
        """Get states of only currently present NPCs for UI display"""
        return {
            name: {
                "score": self.npcs[name]["relationship_score"],
                "emotion": self.npcs[name]["emotional_state"],
                "occupation": self.npcs[name].get("occupation", "Unknown")
            }
            for name in self.current_npcs if name in self.npcs
        }
    
    def get_npc_context(self) -> str:
        """Get formatted context of currently present NPCs"""
        if not self.current_npcs:
            return "No NPCs currently present."
        
        contexts = []
        for name in self.current_npcs:
            if name in self.npcs:
                data = self.npcs[name]
                contexts.append(f"{name} ({data['occupation']}): {data['emotional_state']} (Relationship: {data['relationship_score']})")
        
        return "\n".join(contexts)
    
    def get_npc_states(self) -> Dict[str, Dict[str, Any]]:
        """Get all NPC states for reference (backward compatibility)"""
        return {
            name: {
                "score": data["relationship_score"],
                "emotion": data["emotional_state"],
                "occupation": data.get("occupation", "Unknown")
            }
            for name, data in self.npcs.items()
        }
    
    def is_valid_npc_name(self, name: str) -> bool:
        """Check if a name is valid for an NPC (not a common word)"""
        if not name or len(name) < 2:
            return False
            
        name_lower = name.lower()
        
        # Enhanced exclusion list
        excluded_words = {
            # Common words that aren't names
            'the', 'and', 'you', 'your', 'they', 'them', 'their', 'this', 'that', 'these', 'those',
            'here', 'there', 'where', 'when', 'what', 'who', 'why', 'how', 'which',
            'with', 'from', 'into', 'unto', 'upon', 'over', 'under', 'above', 'below',
            'before', 'after', 'during', 'while', 'since', 'until', 'through', 'across',
            'around', 'between', 'among', 'within', 'without', 'inside', 'outside',
            
            # Common verbs that might be mistaken for names
            'says', 'said', 'tells', 'told', 'asks', 'asked', 'calls', 'called',
            'walks', 'walked', 'runs', 'ran', 'comes', 'came', 'goes', 'went',
            'takes', 'took', 'gives', 'gave', 'makes', 'made', 'does', 'did',
            'looks', 'looked', 'sees', 'saw', 'hears', 'heard', 'feels', 'felt',
            
            # Common adjectives
            'old', 'young', 'new', 'big', 'small', 'large', 'little', 'good', 'bad',
            'great', 'long', 'short', 'high', 'low', 'right', 'left', 'first', 'last',
            'next', 'few', 'many', 'much', 'more', 'most', 'other', 'another', 'same',
            
            # Common nouns that aren't names
            'man', 'woman', 'person', 'people', 'child', 'boy', 'girl', 'friend', 'enemy',
            'stranger', 'traveler', 'visitor', 'guest', 'host', 'owner', 'master', 'servant',
            'lord', 'lady', 'king', 'queen', 'prince', 'princess', 'duke', 'baron',
            
            # RPG-specific common words
            'player', 'character', 'hero', 'villain', 'monster', 'creature', 'beast',
            'dragon', 'goblin', 'orc', 'elf', 'dwarf', 'human', 'halfling',
            'warrior', 'fighter', 'mage', 'wizard', 'priest', 'cleric', 'rogue', 'thief',
            'archer', 'ranger', 'paladin', 'barbarian', 'monk', 'sorcerer', 'warlock',
            
            # Common titles and occupations (general)
            'sir', 'lord', 'lady', 'master', 'mister', 'miss', 'mrs', 'doctor', 'captain',
            
            # Location words
            'town', 'city', 'village', 'castle', 'tower', 'dungeon', 'cave', 'forest',
            'mountain', 'river', 'lake', 'sea', 'ocean', 'desert', 'plain', 'hill',
            'road', 'path', 'bridge', 'gate', 'door', 'window', 'wall', 'floor', 'roof',
            
            # Time words
            'day', 'night', 'morning', 'evening', 'noon', 'midnight', 'dawn', 'dusk',
            'today', 'tomorrow', 'yesterday', 'week', 'month', 'year', 'hour', 'minute',
            
            # Game mechanics
            'level', 'experience', 'skill', 'ability', 'spell', 'magic', 'item', 'weapon',
            'armor', 'shield', 'sword', 'bow', 'staff', 'potion', 'scroll', 'book',
            'gold', 'silver', 'copper', 'coin', 'treasure', 'loot', 'quest', 'mission',
        }
        
        return (
            name.replace("'", "").replace("-", "").isalpha() and  # Allow apostrophes and hyphens in names
            len(name) >= 2 and 
            name_lower not in excluded_words and
            name[0].isupper() and  # Should be capitalized like a proper name
            not name.isupper()     # Avoid all-caps words
        )
    
    def process_dm_response_for_npcs(self, dm_response: str):
        """Extract and initialize NPCs from DM response with enhanced filtering"""
        # Enhanced patterns for better NPC detection
        npc_patterns = [
            # Direct introduction patterns
            r'(?:meet|encounter|see|find|approach)\s+(\w+),?\s+(?:the|a|an)\s+(\w+)',  # "meet Boric, the blacksmith"
            r'(\w+)\s+the\s+(\w+)(?:\s+(?:approaches?|says?|tells?|greets?|nods?))',    # "Elara the merchant approaches"
            r'(?:a|an)\s+(\w+)\s+named\s+(\w+)',                         # "a blacksmith named Boric"
            r'(\w+)\s+named\s+(\w+)(?:\s+(?:approaches?|says?|tells?))?',  # "merchant named Gareth"
            
            # Conversation patterns
            r'(?:talk|speak)\s+(?:to|with)\s+(\w+)(?:\s+the\s+(\w+))?',  # "talk to Marcus the guard"
            r'(\w+)(?:\s+the\s+(\w+))?\s+(?:says?|tells?|asks?|responds?|replies?)', # "Marcus says" or "Marcus the guard says"
            r'(\w+)\s+(?:whispers?|shouts?|calls?|announces?)',           # "Marcus whispers"
            
            # Action patterns
            r'(\w+)(?:\s+the\s+(\w+))?\s+(?:walks?|runs?|moves?|steps?)',  # "Marcus walks"
            r'(\w+)(?:\s+the\s+(\w+))?\s+(?:gives?|hands?|offers?)',       # "Elena gives"
            r'(\w+)(?:\s+the\s+(\w+))?\s+(?:takes?|grabs?|picks?)',        # "Thorin takes"
            
            # Descriptive patterns
            r'(?:you\s+(?:see|notice|spot|observe))\s+(\w+)(?:\s+the\s+(\w+))?',  # "you see Marcus"
            r'(?:there\s+(?:is|stands?|sits?))\s+(\w+)(?:\s+the\s+(\w+))?',        # "there is Elena"
        ]
        
        # Additional occupation-specific patterns
        occupation_patterns = [
            r'(?:the\s+)?(\w+)\s+(blacksmith|merchant|guard|innkeeper|wizard|priest|bard|farmer|hunter|knight|captain|librarian|cook|stable\w*|shop\w*)',
            r'(blacksmith|merchant|guard|innkeeper|wizard|priest|bard|farmer|hunter|knight|captain|librarian|cook)\s+(\w+)',
        ]
        
        detected_npcs = {}
        
        # Process main NPC patterns
        for pattern in npc_patterns:
            matches = re.findall(pattern, dm_response, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 1:
                    name = match[0] if match[0] else None
                    occupation = match[1] if len(match) > 1 and match[1] else "person"
                    
                    if name and self.is_valid_npc_name(name):
                        name = name.capitalize()
                        occupation = occupation.lower() if occupation else "person"
                        detected_npcs[name] = occupation
        
        # Process occupation-specific patterns
        for pattern in occupation_patterns:
            matches = re.findall(pattern, dm_response, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 2:
                    # Handle both "Name occupation" and "occupation Name" patterns
                    if match[0] and self.is_valid_npc_name(match[0]):
                        name, occupation = match[0].capitalize(), match[1].lower()
                    elif match[1] and self.is_valid_npc_name(match[1]):
                        name, occupation = match[1].capitalize(), match[0].lower()
                    else:
                        continue
                    
                    detected_npcs[name] = occupation
        
        # Initialize new NPCs
        for name, occupation in detected_npcs.items():
            if name not in self.npcs:
                self.initialize_npc(name, occupation)
                print(f"🆕 Detected new NPC: {name} the {occupation}")
        
        # Update current NPCs based on the DM response
        self.update_current_npcs(dm_response)