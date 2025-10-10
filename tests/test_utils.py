# tests/test_utils.py
"""
Utility functions and fixtures for testing
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
    """Setup and teardown utilities for tests"""
    
    def __init__(self):
        self.temp_dir = None
        self.original_memory_path = None
        self.engine = None
    
    def setup_test_environment(self):
        """Setup isolated test environment"""
        # Create temporary directory for test memory
        self.temp_dir = tempfile.mkdtemp(prefix="storyteller_test_")
        
        # Store original memory path
        from storyteller import config
        self.original_memory_path = config.MEMORY_SAVE_PATH
        config.MEMORY_SAVE_PATH = self.temp_dir
        
        # Create fresh engine
        self.engine = StorytellingEngine()
        
        return self.engine
    
    def teardown_test_environment(self):
        """Clean up test environment"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        
        if self.original_memory_path:
            from storyteller import config
            config.MEMORY_SAVE_PATH = self.original_memory_path
    
    def create_test_character(self, name="TestHero", **kwargs) -> Character:
        """Create a standard test character"""
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
    """Helper for memory-related testing"""
    
    @staticmethod
    def create_haystack_conversations(engine: StorytellingEngine, 
                                    needle_info: str, 
                                    haystack_size: int = 50) -> int:
        """
        Create a haystack of conversations with a needle of important information
        Returns the conversation number where the needle was inserted
        """
        # Start adventure first
        engine.start_adventure()
        
        # Insert needle conversation at a random position (not too early or late)
        needle_position = haystack_size // 3 + (haystack_size // 6)
        
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
                # Insert the needle - important information
                response = engine.process_player_action(needle_info)
            else:
                # Insert filler conversation
                action = filler_actions[i % len(filler_actions)]
                response = engine.process_player_action(action)
            
            # Add small delay to ensure different timestamps
            time.sleep(0.01)
        
        return needle_position
    
    @staticmethod
    def extract_needle_from_memory(engine: StorytellingEngine, 
                                 needle_keywords: List[str]) -> List[str]:
        """
        Try to extract the needle information from memory using various retrieval methods
        """
        found_memories = []
        
        # Method 1: Direct keyword search
        for keyword in needle_keywords:
            memories = engine.memory.retrieve_relevant_memories(keyword, max_results=5)
            for memory in memories:
                if any(kw.lower() in memory.lower() for kw in needle_keywords):
                    found_memories.append(memory)
        
        # Method 2: Semantic search if available
        try:
            semantic_query = ' '.join(needle_keywords)
            semantic_memories = engine.memory.retrieve_relevant_memories(semantic_query, max_results=10)
            for memory in semantic_memories:
                if any(kw.lower() in memory.lower() for kw in needle_keywords):
                    found_memories.append(memory)
        except Exception:
            pass
        
        return list(set(found_memories))  # Remove duplicates


class StoryConsistencyTester:
    """Test story consistency and coherence"""
    
    @staticmethod
    def test_character_consistency(engine: StorytellingEngine, 
                                 interactions: List[str]) -> Dict[str, Any]:
        """Test if character traits remain consistent across interactions"""
        character_info = engine.get_character_info()
        responses = []
        
        for interaction in interactions:
            response = engine.process_player_action(interaction)
            responses.append(response)
            time.sleep(0.01)
        
        # Analyze responses for character consistency
        character_mentions = []
        for response in responses:
            response_lower = response.lower()
            # Check for mentions of character traits
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
    """Test NPC emotion tracking and consistency"""
    
    @staticmethod
    def test_npc_emotion_progression(engine: StorytellingEngine, 
                                   npc_interactions: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Test NPC emotion progression through various interactions
        npc_interactions: [{'action': '...', 'expected_tone': 'positive/negative/neutral'}]
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
            
            time.sleep(0.01)
        
        return {
            'initial_npcs': initial_npcs,
            'progression': emotion_progression,
            'final_npcs': engine.get_npc_states()
        }


class PerformanceTester:
    """Test performance and timing"""
    
    @staticmethod
    def measure_response_time(engine: StorytellingEngine, 
                            action: str, 
                            iterations: int = 5) -> Dict[str, float]:
        """Measure response time for actions"""
        times = []
        
        for _ in range(iterations):
            start_time = time.time()
            response = engine.process_player_action(action)
            end_time = time.time()
            
            times.append(end_time - start_time)
            time.sleep(0.1)  # Small delay between iterations
        
        return {
            'times': times,
            'average': sum(times) / len(times),
            'min': min(times),
            'max': max(times)
        }
    
    @staticmethod
    def measure_memory_operations(engine: StorytellingEngine) -> Dict[str, float]:
        """Measure memory operation performance"""
        # Test memory save
        start_time = time.time()
        engine.memory.add_conversation_turn("Test action", "Test response")
        save_time = time.time() - start_time
        
        # Test memory search
        start_time = time.time()
        results = engine.memory.retrieve_relevant_memories("test", max_results=5)
        search_time = time.time() - start_time
        
        # Test fact extraction
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
    """Run a test function safely with error handling"""
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