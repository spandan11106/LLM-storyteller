# tests/test_story_consistency.py
"""
Test story consistency, narrative coherence, and character behavior
"""

import time
from typing import Dict, List, Any

from .test_utils import TestSetup, StoryConsistencyTester, run_test_safely


class StoryConsistencyTests:
    """Comprehensive story consistency and narrative coherence tests"""
    
    def __init__(self):
        self.setup = TestSetup()
        self.results = {}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all story consistency tests"""
        print("📖 Starting Story Consistency Tests...")
        
        # Setup test environment
        engine = self.setup.setup_test_environment()
        
        try:
            # Create test character with specific traits
            self.setup.create_test_character(
                name="Sir Galahad",
                background="A noble knight from the Kingdom of Valor, trained in chivalry and honor.",
                personality="Honorable, brave, compassionate, and always helps those in need.",
                goals="To uphold justice, protect the innocent, and find the legendary Holy Grail."
            )
            
            # Run individual tests
            self.test_character_trait_consistency(engine)
            self.test_narrative_continuity(engine)
            self.test_world_state_consistency(engine)
            self.test_dialogue_consistency(engine)
            self.test_consequence_tracking(engine)
            
        finally:
            # Cleanup
            self.setup.teardown_test_environment()
        
        return self.results
    
    def test_character_trait_consistency(self, engine):
        """Test if character traits remain consistent throughout the story"""
        print("  🎭 Testing character trait consistency...")
        
        def trait_consistency_test():
            # Start adventure
            engine.start_adventure()
            
            # Actions that should reflect character traits
            trait_testing_actions = [
                {
                    'action': "I see a group of bandits attacking innocent travelers on the road.",
                    'expected_traits': ['brave', 'protect', 'help', 'justice'],
                    'unexpected_traits': ['flee', 'ignore', 'coward']
                },
                {
                    'action': "A poor beggar asks me for gold to feed his family.",
                    'expected_traits': ['compassionate', 'help', 'give', 'kind'],
                    'unexpected_traits': ['refuse', 'ignore', 'selfish']
                },
                {
                    'action': "I find a valuable treasure that belongs to someone else.",
                    'expected_traits': ['honor', 'return', 'honest', 'right'],
                    'unexpected_traits': ['steal', 'keep', 'dishonest']
                },
                {
                    'action': "An evil lord offers me great wealth to betray my principles.",
                    'expected_traits': ['refuse', 'honor', 'principle', 'noble'],
                    'unexpected_traits': ['accept', 'betray', 'greedy']
                }
            ]
            
            trait_consistency_results = []
            
            for scenario in trait_testing_actions:
                response = engine.process_player_action(scenario['action'])
                
                # Analyze response for trait consistency
                response_lower = response.lower()
                
                expected_found = sum(1 for trait in scenario['expected_traits'] if trait in response_lower)
                unexpected_found = sum(1 for trait in scenario['unexpected_traits'] if trait in response_lower)
                
                trait_score = expected_found - unexpected_found
                is_consistent = trait_score > 0
                
                trait_consistency_results.append({
                    'action': scenario['action'],
                    'response': response,
                    'expected_traits': scenario['expected_traits'],
                    'unexpected_traits': scenario['unexpected_traits'],
                    'expected_found': expected_found,
                    'unexpected_found': unexpected_found,
                    'trait_score': trait_score,
                    'is_consistent': is_consistent
                })
                
                time.sleep(0.1)
            
            overall_consistency = sum(1 for r in trait_consistency_results if r['is_consistent']) / len(trait_consistency_results)
            
            return {
                'scenarios': trait_consistency_results,
                'overall_consistency': overall_consistency,
                'consistency_threshold_met': overall_consistency >= 0.7
            }
        
        self.results['character_trait_consistency'] = run_test_safely(trait_consistency_test)
    
    def test_narrative_continuity(self, engine):
        """Test if the narrative maintains continuity across interactions"""
        print("  📜 Testing narrative continuity...")
        
        def narrative_continuity_test():
            # Start adventure
            engine.start_adventure()
            
            # Create a sequence of connected events
            story_sequence = [
                "I enter a dark forest looking for the lost village of Millhaven.",
                "I find strange glowing mushrooms that light my way through the forest.",
                "I discover an old map carved into a tree trunk showing the path to Millhaven.",
                "I follow the map and reach the outskirts of the village as night falls.",
                "I approach the village and notice all the houses are mysteriously dark and silent."
            ]
            
            narrative_elements = {
                'forest': 0,
                'millhaven': 0,
                'mushrooms': 0,
                'map': 0,
                'village': 0,
                'dark': 0,
                'night': 0
            }
            
            responses = []
            for action in story_sequence:
                response = engine.process_player_action(action)
                responses.append({
                    'action': action,
                    'response': response
                })
                
                # Track narrative elements
                response_lower = response.lower()
                for element in narrative_elements:
                    if element in response_lower:
                        narrative_elements[element] += 1
                
                time.sleep(0.1)
            
            # Test continuity by asking about previous events
            continuity_questions = [
                "What do I remember about the glowing mushrooms I found?",
                "Can I recall the map I discovered in the forest?",
                "What was my goal when I entered this forest?"
            ]
            
            continuity_responses = []
            for question in continuity_questions:
                response = engine.process_player_action(question)
                
                # Check if response references previous events
                response_lower = response.lower()
                references_found = sum(1 for element in ['mushroom', 'map', 'millhaven', 'forest'] if element in response_lower)
                
                continuity_responses.append({
                    'question': question,
                    'response': response,
                    'references_found': references_found,
                    'has_continuity': references_found > 0
                })
                
                time.sleep(0.1)
            
            continuity_score = sum(1 for r in continuity_responses if r['has_continuity']) / len(continuity_responses)
            
            return {
                'story_sequence': responses,
                'narrative_elements_tracked': narrative_elements,
                'continuity_questions': continuity_responses,
                'continuity_score': continuity_score,
                'strong_continuity': continuity_score >= 0.6
            }
        
        self.results['narrative_continuity'] = run_test_safely(narrative_continuity_test)
    
    def test_world_state_consistency(self, engine):
        """Test if the world state remains consistent (no contradictions)"""
        print("  🌍 Testing world state consistency...")
        
        def world_state_test():
            # Start adventure
            engine.start_adventure()
            
            # Establish world state facts
            world_building_actions = [
                "I am in the kingdom of Aethermoor, ruled by King Aldric the Wise.",
                "The capital city is called Goldenheart, famous for its golden spires.",
                "I carry my family's ancestral sword, Dawnbreaker, which glows at sunrise.",
                "My horse is a white stallion named Thunder who is very loyal.",
                "The current season is autumn, with leaves turning golden and red."
            ]
            
            established_facts = []
            for action in world_building_actions:
                response = engine.process_player_action(action)
                established_facts.append({
                    'action': action,
                    'response': response
                })
                time.sleep(0.1)
            
            # Later, test for consistency
            consistency_test_actions = [
                "I think about my homeland and its ruler.",  # Should mention King Aldric/Aethermoor
                "I look at my sword in the morning light.",   # Should mention Dawnbreaker/glowing
                "I check on my faithful steed.",             # Should mention Thunder/white stallion
                "I notice the changing leaves around me.",   # Should mention autumn
                "I remember the golden spires of my capital." # Should mention Goldenheart
            ]
            
            consistency_results = []
            key_elements = [
                ['aldric', 'king', 'aethermoor'],
                ['dawnbreaker', 'sword', 'glow'],
                ['thunder', 'horse', 'stallion'],
                ['autumn', 'leaves', 'golden'],
                ['goldenheart', 'spires', 'capital']
            ]
            
            for i, action in enumerate(consistency_test_actions):
                response = engine.process_player_action(action)
                response_lower = response.lower()
                
                # Check if response contains relevant established facts
                relevant_elements = key_elements[i]
                elements_found = sum(1 for element in relevant_elements if element in response_lower)
                
                consistency_results.append({
                    'action': action,
                    'response': response,
                    'expected_elements': relevant_elements,
                    'elements_found': elements_found,
                    'is_consistent': elements_found > 0
                })
                
                time.sleep(0.1)
            
            consistency_rate = sum(1 for r in consistency_results if r['is_consistent']) / len(consistency_results)
            
            return {
                'established_facts': established_facts,
                'consistency_tests': consistency_results,
                'consistency_rate': consistency_rate,
                'world_state_maintained': consistency_rate >= 0.6
            }
        
        self.results['world_state_consistency'] = run_test_safely(world_state_test)
    
    def test_dialogue_consistency(self, engine):
        """Test consistency in NPC dialogue and personality"""
        print("  💬 Testing dialogue consistency...")
        
        def dialogue_consistency_test():
            # Start adventure
            engine.start_adventure()
            
            # Introduce NPCs with specific personalities
            npc_introductions = [
                {
                    'action': "I meet Gruff the dwarf, a grumpy but skilled blacksmith who speaks in short, direct sentences.",
                    'npc_name': 'gruff',
                    'traits': ['grumpy', 'direct', 'short', 'skilled'],
                    'speech_style': 'short_sentences'
                },
                {
                    'action': "I encounter Lady Seraphina, an eloquent and verbose noble who speaks in flowery, elaborate language.",
                    'npc_name': 'seraphina',
                    'traits': ['eloquent', 'verbose', 'flowery', 'elaborate'],
                    'speech_style': 'elaborate_speech'
                }
            ]
            
            dialogue_tests = []
            
            for npc_intro in npc_introductions:
                # Introduce the NPC
                engine.process_player_action(npc_intro['action'])
                time.sleep(0.1)
                
                # Have multiple conversations with the NPC
                conversations = [
                    f"I ask {npc_intro['npc_name']} about their work and craftsmanship.",
                    f"I inquire about {npc_intro['npc_name']}'s opinion on current events.",
                    f"I seek advice from {npc_intro['npc_name']} about my quest."
                ]
                
                npc_responses = []
                for conversation in conversations:
                    response = engine.process_player_action(conversation)
                    
                    # Analyze response for consistency with established personality
                    response_lower = response.lower()
                    trait_mentions = sum(1 for trait in npc_intro['traits'] if trait in response_lower)
                    
                    # Check for name consistency
                    name_mentioned = npc_intro['npc_name'].lower() in response_lower
                    
                    npc_responses.append({
                        'conversation': conversation,
                        'response': response,
                        'trait_mentions': trait_mentions,
                        'name_mentioned': name_mentioned,
                        'personality_consistent': trait_mentions > 0 or name_mentioned
                    })
                    
                    time.sleep(0.1)
                
                consistency_rate = sum(1 for r in npc_responses if r['personality_consistent']) / len(npc_responses)
                
                dialogue_tests.append({
                    'npc': npc_intro,
                    'conversations': npc_responses,
                    'consistency_rate': consistency_rate
                })
            
            overall_dialogue_consistency = sum(test['consistency_rate'] for test in dialogue_tests) / len(dialogue_tests)
            
            return {
                'dialogue_tests': dialogue_tests,
                'overall_consistency': overall_dialogue_consistency,
                'dialogue_consistency_good': overall_dialogue_consistency >= 0.5
            }
        
        self.results['dialogue_consistency'] = run_test_safely(dialogue_consistency_test)
    
    def test_consequence_tracking(self, engine):
        """Test if actions have appropriate consequences that are remembered"""
        print("  ⚡ Testing consequence tracking...")
        
        def consequence_test():
            # Start adventure
            engine.start_adventure()
            
            # Actions with clear consequences
            consequential_actions = [
                {
                    'action': "I break down the locked door to the armory instead of finding the key.",
                    'consequence_keywords': ['broken', 'door', 'damage', 'loud', 'alarm'],
                    'test_action': "I try to leave the armory quietly."
                },
                {
                    'action': "I save a merchant from bandits and he gives me a magical amulet as reward.",
                    'consequence_keywords': ['amulet', 'magical', 'reward', 'merchant', 'grateful'],
                    'test_action': "I check my magical items and equipment."
                },
                {
                    'action': "I accidentally insult the local lord during our conversation.",
                    'consequence_keywords': ['insult', 'lord', 'angry', 'offended', 'upset'],
                    'test_action': "I think about my relationship with the local nobility."
                }
            ]
            
            consequence_results = []
            
            for scenario in consequential_actions:
                # Perform the consequential action
                initial_response = engine.process_player_action(scenario['action'])
                time.sleep(0.1)
                
                # Perform several unrelated actions to create distance
                filler_actions = [
                    "I walk around and explore the area.",
                    "I check my equipment and supplies.",
                    "I think about my quest objectives."
                ]
                
                for filler in filler_actions:
                    engine.process_player_action(filler)
                    time.sleep(0.05)
                
                # Test if consequences are remembered
                test_response = engine.process_player_action(scenario['test_action'])
                
                # Check if consequence keywords appear in test response
                test_response_lower = test_response.lower()
                consequences_remembered = sum(
                    1 for keyword in scenario['consequence_keywords'] 
                    if keyword in test_response_lower
                )
                
                consequence_results.append({
                    'action': scenario['action'],
                    'initial_response': initial_response,
                    'test_action': scenario['test_action'],
                    'test_response': test_response,
                    'expected_consequences': scenario['consequence_keywords'],
                    'consequences_found': consequences_remembered,
                    'consequences_remembered': consequences_remembered > 0
                })
            
            consequence_tracking_rate = sum(1 for r in consequence_results if r['consequences_remembered']) / len(consequence_results)
            
            return {
                'consequence_scenarios': consequence_results,
                'tracking_rate': consequence_tracking_rate,
                'good_consequence_tracking': consequence_tracking_rate >= 0.6
            }
        
        self.results['consequence_tracking'] = run_test_safely(consequence_test)


def run_story_consistency_tests():
    """Run all story consistency tests and return results"""
    tester = StoryConsistencyTests()
    return tester.run_all_tests()


if __name__ == "__main__":
    results = run_story_consistency_tests()
    
    print("\n" + "="*50)
    print("STORY CONSISTENCY TEST RESULTS")
    print("="*50)
    
    for test_name, result in results.items():
        print(f"\n{test_name.upper()}:")
        if result['success']:
            print(f"  ✅ PASSED")
            test_result = result['result']
            
            if test_name == 'character_trait_consistency':
                print(f"  🎭 Trait consistency: {test_result['overall_consistency']:.2%}")
                print(f"  ✅ Threshold met: {test_result['consistency_threshold_met']}")
            
            elif test_name == 'narrative_continuity':
                print(f"  📜 Continuity score: {test_result['continuity_score']:.2%}")
                print(f"  🔗 Strong continuity: {test_result['strong_continuity']}")
            
            elif test_name == 'world_state_consistency':
                print(f"  🌍 World state consistency: {test_result['consistency_rate']:.2%}")
                print(f"  ✅ State maintained: {test_result['world_state_maintained']}")
            
            elif test_name == 'dialogue_consistency':
                print(f"  💬 Dialogue consistency: {test_result['overall_consistency']:.2%}")
                print(f"  🎯 Good consistency: {test_result['dialogue_consistency_good']}")
            
            elif test_name == 'consequence_tracking':
                print(f"  ⚡ Consequence tracking: {test_result['tracking_rate']:.2%}")
                print(f"  🎯 Good tracking: {test_result['good_consequence_tracking']}")
        
        else:
            print(f"  ❌ FAILED: {result['error']}")