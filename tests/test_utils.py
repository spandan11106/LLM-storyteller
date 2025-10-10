# 🛠️ Magical Testing Toolkit! ✨
"""
🎪 Your friendly collection of testing helpers and magical utilities!

This toolkit provides everything you need to create amazing tests:
- 🏗️ Test environment setup and cleanup magic
- 🎭 Helper functions for creating test characters
- 🧠 Memory testing utilities (including the famous needle-in-haystack!)
- 🔍 Result analysis and reporting spells

Think of this as your trusty sidekick for all testing adventures! 🌟
"""

import os
import json
import time
import tempfile
import shutil
from typing import Dict, List, Any
from dataclasses import asdict

from storyteller.core.engine import StorytellingEngine
from storyteller.core.character import Character


class TestSetup:
    """🏗️ Your magical test environment constructor and cleaner-upper!"""
    
    def __init__(self):
        self.temp_dir = None
        self.original_memory_path = None
        self.engine = None
    
    def setup_test_environment(self):
        """🎪 Set up a completely isolated test playground!"""
        # Create a cozy temporary directory for test memories
        self.temp_dir = tempfile.mkdtemp(prefix="storyteller_test_")
        
        # Safely store the original memory path so we can restore it later
        from storyteller import config
        self.original_memory_path = config.MEMORY_SAVE_PATH
        config.MEMORY_SAVE_PATH = self.temp_dir
        
        # Create a fresh, pristine storytelling engine just for testing!
        self.engine = StorytellingEngine()
        
        return self.engine
    
    def teardown_test_environment(self):
        """🧹 Clean up our test playground and restore everything perfectly!"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        
        if self.original_memory_path:
            from storyteller import config
            config.MEMORY_SAVE_PATH = self.original_memory_path
    
    def create_test_character(self, name="TestHero", **kwargs) -> Character:
        """🎭 Create a perfectly heroic test character for our adventures!"""
        defaults = {
            'background': 'A brave adventurer seeking glory and treasure.',
            'personality': 'Courageous, curious, and kind-hearted.',
            'goals': 'To become a legendary hero and protect the innocent.',
            'strength': 15,
            'dexterity': 12,
            'intelligence': 14,
            'charisma': 13
        }
        defaults.update(kwargs)
        
        self.engine.create_character(name, **defaults)
        return self.engine.character


class MemoryTestHelper:
    """🧠 Your specialist helper for testing the legendary memory palace!"""
    
    @staticmethod
    def create_haystack_conversations(engine: StorytellingEngine, 
                                    needle_info: str, 
                                    haystack_size: int = 50) -> int:
        """
        🔍 Create the famous needle-in-haystack test! 
        Builds a mountain of conversations and hides important info somewhere inside.
        Returns the conversation number where the needle was secretly inserted.
        """
        # Start the adventure magic first!
        engine.start_adventure()
        
        # Hide the needle somewhere in the middle (not too obvious!)
        needle_position = haystack_size // 3 + (haystack_size // 6)
        
        # Collection of typical adventurer actions for building our haystack
        filler_actions = [
            "I look around the room carefully.",
            "I check my equipment and inventory.",
            "I listen for any sounds nearby.",
            "I examine the walls for secret passages.",
            "I search for anything useful on the floor.",
            "I try to remember how I got here.",
            "I take a deep breath and steel my nerves.",
            "I adjust my grip on my weapon.",
            "I peek around the corner cautiously.",
            "I study the architecture of this place.",
            "I clean my sword and check its sharpness.",
            "I count my remaining supplies.",
            "I practice a few sword movements.",
            "I think about my quest and goals.",
            "I examine my clothing for damage.",
        ]
        
        for i in range(haystack_size):
            if i == needle_position:
                # 💎 Insert the precious needle - this is our important information!
                response = engine.process_player_action(needle_info)
            else:
                # 🌾 Insert regular haystack conversation
                action = filler_actions[i % len(filler_actions)]
                response = engine.process_player_action(action)
            
            # Add a tiny pause to ensure each conversation has a unique timestamp
            time.sleep(0.01)
        
        return needle_position
    
    @staticmethod
    def extract_needle_from_memory(engine: StorytellingEngine, 
                                 needle_keywords: List[str]) -> List[str]:
        """
        🔍 Try to find our hidden needle using every trick in the book!
        Tests multiple search strategies to see if the memory palace is truly legendary.
        """
        found_memories = []
        
        # 🎯 Method 1: Direct keyword hunting (the obvious approach)
        for keyword in needle_keywords:
            memories = engine.memory.retrieve_relevant_memories(keyword, max_results=5)
            for memory in memories:
                if any(kw.lower() in memory.lower() for kw in needle_keywords):
                    found_memories.append(memory)
        
        # 🧠 Method 2: Smart semantic search (understanding meaning, not just words)
        try:
            semantic_query = ' '.join(needle_keywords)
            semantic_memories = engine.memory.retrieve_relevant_memories(semantic_query, max_results=10)
            for memory in semantic_memories:
                if any(kw.lower() in memory.lower() for kw in needle_keywords):
                    found_memories.append(memory)
        except Exception:
            # No worries if semantic search isn't available
            pass
        
        return list(set(found_memories))  # Remove duplicates and return our treasure hunt results!


class StoryConsistencyTester:
    """📖 Your specialist for testing epic story consistency and flow!"""
    
    @staticmethod
    def test_character_consistency(engine: StorytellingEngine, 
                                 interactions: List[str]) -> Dict[str, Any]:
        """🎭 Test if character traits stay true across the entire adventure!"""
        character_info = engine.get_character_info()
        responses = []
        
        for interaction in interactions:
            response = engine.process_player_action(interaction)
            responses.append(response)
            time.sleep(0.01)  # Give the AI a moment to think
        
        # 🔍 Analyze responses to see if character personality shines through consistently
        character_mentions = []
        for response in responses:
            response_lower = response.lower()
            # Check if the character's personality comes through in the responses
            if character_info['personality'].lower() in response_lower:
                character_mentions.append('personality')
            if any(goal.lower() in response_lower for goal in character_info['goals'].split()):
                character_mentions.append('goals')
        
        return {
            'responses': responses,
            'character_mentions': character_mentions,
            'consistency_score': len(character_mentions) / len(interactions)
        }


class NPCEmotionTester:
    """💝 Your specialist for testing NPC hearts, emotions, and relationship magic!"""
    
    @staticmethod
    def test_npc_emotion_progression(engine: StorytellingEngine, 
                                   npc_interactions: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        💕 Test how NPC emotions grow and change through various interactions!
        npc_interactions: [{'action': '...', 'expected_tone': 'positive/negative/neutral'}]
        This tests if NPCs actually remember how you treat them and respond accordingly!
        """
        initial_npcs = engine.get_npc_states()
        emotion_progression = []
        
        for interaction in npc_interactions:
            response = engine.process_player_action(interaction['action'])
            current_npcs = engine.get_npc_states()
            
            emotion_progression.append({
                'action': interaction['action'],
                'expected_tone': interaction['expected_tone'],
                'response': response,
                'npc_states': current_npcs.copy()
            })
            
            time.sleep(0.01)  # Let emotions process naturally
        
        return {
            'initial_npcs': initial_npcs,
            'progression': emotion_progression,
            'final_npcs': engine.get_npc_states()
        }


class PerformanceTester:
    """⚡ Your speed demon for testing lightning-fast performance!"""
    
    @staticmethod
    def measure_response_time(engine: StorytellingEngine, 
                            action: str, 
                            iterations: int = 5) -> Dict[str, float]:
        """⏱️ Measure how fast our AI responds to actions (should be snappy!)"""
        times = []
        
        for _ in range(iterations):
            start_time = time.time()
            response = engine.process_player_action(action)
            end_time = time.time()
            
            times.append(end_time - start_time)
            time.sleep(0.1)  # Brief pause between speed tests
        
        return {
            'times': times,
            'average': sum(times) / len(times),
            'min': min(times),
            'max': max(times)
        }
    
    @staticmethod
    def measure_memory_operations(engine: StorytellingEngine) -> Dict[str, float]:
        """💾 Test how efficiently our memory palace operates!"""
        start_time = time.time()
        engine.memory.add_conversation_turn("Test action", "Test response")
        save_time = time.time() - start_time
        
        # Test memory search speed
        start_time = time.time()
        results = engine.memory.retrieve_relevant_memories("test", max_results=5)
        search_time = time.time() - start_time
        
        # Test fact extraction speed 
        start_time = time.time()
        facts = engine.memory.extract_facts("The brave knight fought the dragon.")
        extraction_time = time.time() - start_time
        
        return {
            'save_time': save_time,
            'search_time': search_time,
            'extraction_time': extraction_time,
            'total_conversations': engine.memory.get_summary()['total_conversations']
        }


def run_test_safely(test_func, *args, **kwargs):
    """🛡️ Run a test function with magical error protection and helpful reporting!"""
    try:
        return {
            'success': True,
            'result': test_func(*args, **kwargs),
            'error': None
        }
    except Exception as e:
        return {
            'success': False,
            'result': None,
            'error': str(e)
        }