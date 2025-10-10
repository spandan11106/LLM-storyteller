# tests/test_memory.py
"""
Memory system tests including needle in haystack for long-term memory
"""

import time
import json
from typing import Dict, List, Any

from .test_utils import TestSetup, MemoryTestHelper, run_test_safely


class MemoryTests:
    """Comprehensive memory system tests"""
    
    def __init__(self):
        self.setup = TestSetup()
        self.results = {}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all memory tests"""
        print("🧠 Starting Memory Tests...")
        
        # Setup test environment
        engine = self.setup.setup_test_environment()
        
        try:
            # Create test character
            self.setup.create_test_character()
            
            # Run individual tests
            self.test_short_term_memory(engine)
            self.test_long_term_memory_needle_haystack(engine)
            self.test_fact_extraction(engine)
            self.test_memory_persistence(engine)
            self.test_memory_search_accuracy(engine)
            
        finally:
            # Cleanup
            self.setup.teardown_test_environment()
        
        return self.results
    
    def test_short_term_memory(self, engine):
        """Test short-term memory (recent conversations)"""
        print("  📝 Testing short-term memory...")
        
        def short_term_test():
            # Start adventure
            engine.start_adventure()
            
            # Have a few recent conversations
            recent_actions = [
                "I draw my sword and prepare for battle.",
                "I cast a healing spell on myself.",
                "I search the fallen enemy for loot."
            ]
            
            responses = []
            for action in recent_actions:
                response = engine.process_player_action(action)
                responses.append(response)
                time.sleep(0.01)
            
            # Test if recent context is available
            memory_summary = engine.get_memory_summary()
            recent_conversations = memory_summary.get('recent_conversations', [])
            
            return {
                'actions': recent_actions,
                'responses': responses,
                'recent_count': len(recent_conversations),
                'has_recent_context': len(recent_conversations) >= len(recent_actions)
            }
        
        self.results['short_term_memory'] = run_test_safely(short_term_test)
    
    def test_long_term_memory_needle_haystack(self, engine):
        """Test long-term memory using needle in haystack method"""
        print("  🔍 Testing long-term memory (needle in haystack)...")
        
        def needle_haystack_test():
            # Define our "needle" - important information to hide
            needle_action = "I discover the ancient Crystal of Eternal Flame hidden behind the altar, glowing with mystical blue fire."
            needle_keywords = ["Crystal", "Eternal", "Flame", "altar", "blue fire"]
            
            # Create haystack of conversations
            print("    Creating haystack of conversations...")
            haystack_size = 75  # Large number of conversations
            needle_position = MemoryTestHelper.create_haystack_conversations(
                engine, needle_action, haystack_size
            )
            
            print(f"    Needle inserted at position {needle_position}/{haystack_size}")
            
            # Add more conversations after the needle
            post_needle_actions = [
                "I continue exploring the dungeon.",
                "I check my map for the next location.",
                "I rest and eat some provisions.",
                "I sharpen my weapons and prepare for the next challenge.",
                "I think about my journey so far."
            ]
            
            for action in post_needle_actions:
                engine.process_player_action(action)
                time.sleep(0.01)
            
            print("    Searching for needle in memory...")
            
            # Try to retrieve the needle information
            found_memories = MemoryTestHelper.extract_needle_from_memory(
                engine, needle_keywords
            )
            
            # Test semantic search with related query
            semantic_query = "What magical items have I found?"
            semantic_response = engine.process_player_action(semantic_query)
            
            # Check if needle information is mentioned in semantic response
            needle_found_in_response = any(
                keyword.lower() in semantic_response.lower() 
                for keyword in needle_keywords
            )
            
            return {
                'needle_action': needle_action,
                'needle_position': needle_position,
                'haystack_size': haystack_size + len(post_needle_actions),
                'found_memories': found_memories,
                'needle_found_count': len(found_memories),
                'semantic_query': semantic_query,
                'semantic_response': semantic_response,
                'needle_in_semantic_response': needle_found_in_response,
                'memory_retrieval_success': len(found_memories) > 0 or needle_found_in_response
            }
        
        self.results['needle_haystack'] = run_test_safely(needle_haystack_test)
    
    def test_fact_extraction(self, engine):
        """Test fact extraction from conversations"""
        print("  🔬 Testing fact extraction...")
        
        def fact_extraction_test():
            # Start adventure
            engine.start_adventure()
            
            # Actions that should generate extractable facts
            fact_generating_actions = [
                "I meet a merchant named Gareth who sells magical potions.",
                "I learn that the Dragon of Mount Doom has been terrorizing nearby villages.",
                "I discover that my sword is actually the legendary Blade of Heroes.",
                "I find out the evil wizard Malachar lives in the Dark Tower."
            ]
            
            # Track initial state
            initial_memories = engine.memory.get_summary()['total_conversations']
            extracted_facts_list = []
            
            for action in fact_generating_actions:
                response = engine.process_player_action(action)
                # Extract facts from this response
                facts = engine.memory.extract_facts(response)
                extracted_facts_list.extend(facts)
                time.sleep(0.01)
            
            final_memories = engine.memory.get_summary()['total_conversations']
            
            return {
                'initial_memory_count': initial_memories,
                'final_memory_count': final_memories,
                'facts_extracted': len(extracted_facts_list),
                'fact_generating_actions': fact_generating_actions,
                'recent_facts': extracted_facts_list[-10:],
                'extraction_working': len(extracted_facts_list) > 0
            }
        
        self.results['fact_extraction'] = run_test_safely(fact_extraction_test)
    
    def test_memory_persistence(self, engine):
        """Test if memory persists across sessions"""
        print("  💾 Testing memory persistence...")
        
        def persistence_test():
            # Start adventure and create some memories
            engine.start_adventure()
            
            test_action = "I discover a secret passage behind the bookshelf."
            response = engine.process_player_action(test_action)
            
            # Get current memory state
            pre_save_summary = engine.get_memory_summary()
            conversation_count = pre_save_summary['total_conversations']
            
            # Force save memory
            engine.memory.add_conversation_turn(test_action, response)
            
            # Create new engine instance (simulate restart)
            new_engine = type(engine)()
            new_engine.character = engine.character  # Use same character
            
            # Check if memory was loaded
            post_load_summary = new_engine.get_memory_summary()
            
            return {
                'pre_save_conversations': conversation_count,
                'post_load_conversations': post_load_summary['total_conversations'],
                'memory_persisted': post_load_summary['total_conversations'] >= conversation_count,
                'test_action': test_action
            }
        
        self.results['memory_persistence'] = run_test_safely(persistence_test)
    
    def test_memory_search_accuracy(self, engine):
        """Test accuracy of memory search functionality"""
        print("  🎯 Testing memory search accuracy...")
        
        def search_accuracy_test():
            # Start adventure
            engine.start_adventure()
            
            # Create conversations with specific searchable content
            search_scenarios = [
                {
                    'action': "I fight a fearsome red dragon in the mountain cave.",
                    'keywords': ["dragon", "red", "mountain"],
                    'irrelevant_keywords': ["ocean", "fish", "library"]
                },
                {
                    'action': "I brew a powerful healing potion using rare herbs.",
                    'keywords': ["potion", "healing", "herbs"],
                    'irrelevant_keywords': ["sword", "armor", "castle"]
                },
                {
                    'action': "I negotiate with the goblin king for safe passage.",
                    'keywords': ["goblin", "king", "negotiate"],
                    'irrelevant_keywords': ["dragon", "potion", "mountain"]
                }
            ]
            
            # Create the conversations
            for scenario in search_scenarios:
                engine.process_player_action(scenario['action'])
                time.sleep(0.01)
            
            # Test search accuracy
            search_results = []
            for scenario in search_scenarios:
                # Test relevant keyword search
                relevant_results = []
                for keyword in scenario['keywords']:
                    results = engine.memory.retrieve_relevant_memories(keyword, max_results=5)
                    relevant_results.extend(results)
                
                # Test irrelevant keyword search
                irrelevant_results = []
                for keyword in scenario['irrelevant_keywords']:
                    results = engine.memory.retrieve_relevant_memories(keyword, max_results=5)
                    irrelevant_results.extend(results)
                
                search_results.append({
                    'action': scenario['action'],
                    'relevant_keywords': scenario['keywords'],
                    'irrelevant_keywords': scenario['irrelevant_keywords'],
                    'relevant_results_count': len(relevant_results),
                    'irrelevant_results_count': len(irrelevant_results),
                    'search_accuracy': len(relevant_results) > len(irrelevant_results)
                })
            
            overall_accuracy = sum(1 for r in search_results if r['search_accuracy']) / len(search_results)
            
            return {
                'search_scenarios': search_results,
                'overall_accuracy': overall_accuracy,
                'accuracy_threshold_met': overall_accuracy >= 0.7  # 70% accuracy threshold
            }
        
        self.results['search_accuracy'] = run_test_safely(search_accuracy_test)


def run_memory_tests():
    """Run all memory tests and return results"""
    tester = MemoryTests()
    return tester.run_all_tests()


if __name__ == "__main__":
    results = run_memory_tests()
    
    print("\n" + "="*50)
    print("MEMORY TEST RESULTS")
    print("="*50)
    
    for test_name, result in results.items():
        print(f"\n{test_name.upper()}:")
        if result['success']:
            print(f"  ✅ PASSED")
            # Print key metrics
            test_result = result['result']
            if test_name == 'needle_haystack':
                print(f"  📍 Needle position: {test_result['needle_position']}/{test_result['haystack_size']}")
                print(f"  🔍 Memory retrieval: {'SUCCESS' if test_result['memory_retrieval_success'] else 'FAILED'}")
                print(f"  🧠 Found memories: {test_result['needle_found_count']}")
            elif test_name == 'fact_extraction':
                print(f"  📊 Facts extracted: {test_result['facts_extracted']}")
                print(f"  ✅ Extraction working: {test_result['extraction_working']}")
            elif test_name == 'search_accuracy':
                print(f"  🎯 Search accuracy: {test_result['overall_accuracy']:.2%}")
                print(f"  ✅ Threshold met: {test_result['accuracy_threshold_met']}")
        else:
            print(f"  ❌ FAILED: {result['error']}")