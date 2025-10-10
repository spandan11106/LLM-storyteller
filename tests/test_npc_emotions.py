# tests/test_npc_emotions.py
"""
Test NPC emotion tracking, consistency, and relationship dynamics
"""

import time
from typing import Dict, List, Any

from .test_utils import TestSetup, NPCEmotionTester, run_test_safely


class NPCEmotionTests:
    """Comprehensive NPC emotion and relationship tests"""
    
    def __init__(self):
        self.setup = TestSetup()
        self.results = {}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all NPC emotion tests"""
        print("😊 Starting NPC Emotion Tests...")
        
        # Setup test environment
        engine = self.setup.setup_test_environment()
        
        try:
            # Create test character
            self.setup.create_test_character()
            
            # Run individual tests
            self.test_npc_emotion_detection(engine)
            self.test_npc_relationship_progression(engine)
            self.test_npc_emotion_consistency(engine)
            self.test_multiple_npc_interactions(engine)
            self.test_npc_memory_integration(engine)
            
        finally:
            # Cleanup
            self.setup.teardown_test_environment()
        
        return self.results
    
    def test_npc_emotion_detection(self, engine):
        """Test if NPCs are properly detected and emotions tracked"""
        print("  🎭 Testing NPC emotion detection...")
        
        def emotion_detection_test():
            # Start adventure
            engine.start_adventure()
            
            # Interactions that should create and track NPCs
            npc_interactions = [
                {
                    'action': "I greet the friendly tavern keeper warmly and ask about rooms.",
                    'expected_npc': "tavern keeper",
                    'expected_tone': "positive"
                },
                {
                    'action': "I rudely demand information from the village guard without saying please.",
                    'expected_npc': "guard",
                    'expected_tone': "negative"
                },
                {
                    'action': "I politely ask the wise old sage for advice about my quest.",
                    'expected_npc': "sage",
                    'expected_tone': "positive"
                }
            ]
            
            npc_detection_results = []
            
            for interaction in npc_interactions:
                initial_npcs = engine.get_npc_states()
                response = engine.process_player_action(interaction['action'])
                final_npcs = engine.get_npc_states()
                
                # Check for new NPCs
                new_npcs = {k: v for k, v in final_npcs.items() if k not in initial_npcs}
                
                npc_detection_results.append({
                    'action': interaction['action'],
                    'expected_npc': interaction['expected_npc'],
                    'expected_tone': interaction['expected_tone'],
                    'response': response,
                    'initial_npc_count': len(initial_npcs),
                    'final_npc_count': len(final_npcs),
                    'new_npcs': new_npcs,
                    'npc_detected': len(new_npcs) > 0
                })
                
                time.sleep(0.1)
            
            return {
                'interactions': npc_detection_results,
                'total_npcs_created': len(engine.get_npc_states()),
                'detection_success_rate': sum(1 for r in npc_detection_results if r['npc_detected']) / len(npc_detection_results)
            }
        
        self.results['npc_emotion_detection'] = run_test_safely(emotion_detection_test)
    
    def test_npc_relationship_progression(self, engine):
        """Test NPC relationship score progression over multiple interactions"""
        print("  💝 Testing NPC relationship progression...")
        
        def relationship_progression_test():
            # Start adventure
            engine.start_adventure()
            
            # Create an NPC through interaction
            engine.process_player_action("I meet a blacksmith named Thorin in his forge.")
            time.sleep(0.1)
            
            # Series of interactions with different tones
            progression_interactions = [
                {
                    'action': "I compliment Thorin on his excellent craftsmanship.",
                    'expected_change': 'positive'
                },
                {
                    'action': "I offer to help Thorin organize his workshop.",
                    'expected_change': 'positive'
                },
                {
                    'action': "I accidentally knock over some of Thorin's tools.",
                    'expected_change': 'negative'
                },
                {
                    'action': "I apologize sincerely and help clean up the mess.",
                    'expected_change': 'positive'
                },
                {
                    'action': "I buy an expensive sword from Thorin and tip generously.",
                    'expected_change': 'positive'
                }
            ]
            
            relationship_tracking = []
            previous_score = None
            
            for interaction in progression_interactions:
                pre_npcs = engine.get_npc_states()
                response = engine.process_player_action(interaction['action'])
                post_npcs = engine.get_npc_states()
                
                # Find Thorin's data
                thorin_data = None
                for npc_name, data in post_npcs.items():
                    if 'thorin' in npc_name.lower() or 'blacksmith' in npc_name.lower():
                        thorin_data = data
                        break
                
                current_score = thorin_data['score'] if thorin_data else 0
                score_change = current_score - (previous_score or 0)
                
                relationship_tracking.append({
                    'action': interaction['action'],
                    'expected_change': interaction['expected_change'],
                    'previous_score': previous_score,
                    'current_score': current_score,
                    'score_change': score_change,
                    'emotion': thorin_data['emotion'] if thorin_data else 'unknown',
                    'change_matches_expectation': (
                        (interaction['expected_change'] == 'positive' and score_change >= 0) or
                        (interaction['expected_change'] == 'negative' and score_change < 0)
                    )
                })
                
                previous_score = current_score
                time.sleep(0.1)
            
            return {
                'interactions': relationship_tracking,
                'final_thorin_data': thorin_data,
                'relationship_logic_accuracy': sum(1 for r in relationship_tracking if r['change_matches_expectation']) / len(relationship_tracking)
            }
        
        self.results['npc_relationship_progression'] = run_test_safely(relationship_progression_test)
    
    def test_npc_emotion_consistency(self, engine):
        """Test if NPC emotions remain consistent with their relationship scores"""
        print("  🎯 Testing NPC emotion consistency...")
        
        def emotion_consistency_test():
            # Start adventure
            engine.start_adventure()
            
            # Create NPCs with different relationship trajectories
            consistency_scenarios = [
                {
                    'npc_setup': "I meet Captain Marcus, a stern but fair city guard.",
                    'positive_interactions': [
                        "I respectfully report a crime to Captain Marcus.",
                        "I offer to help Captain Marcus with his duties.",
                        "I thank Captain Marcus for keeping the city safe."
                    ],
                    'expected_final_emotion': ['friendly', 'pleased', 'happy', 'positive']
                },
                {
                    'npc_setup': "I encounter Sneaky Pete, a suspicious-looking rogue in an alley.",
                    'negative_interactions': [
                        "I threaten to report Sneaky Pete to the authorities.",
                        "I refuse to pay Sneaky Pete's extortion demands.",
                        "I insult Sneaky Pete's thieving ways."
                    ],
                    'expected_final_emotion': ['angry', 'hostile', 'upset', 'negative']
                }
            ]
            
            consistency_results = []
            
            for scenario in consistency_scenarios:
                # Setup NPC
                engine.process_player_action(scenario['npc_setup'])
                time.sleep(0.1)
                
                # Run interactions
                interactions = scenario.get('positive_interactions', []) or scenario.get('negative_interactions', [])
                for interaction in interactions:
                    engine.process_player_action(interaction)
                    time.sleep(0.1)
                
                # Check final state
                final_npcs = engine.get_npc_states()
                
                # Find the relevant NPC
                relevant_npc = None
                for npc_name, data in final_npcs.items():
                    setup_lower = scenario['npc_setup'].lower()
                    if any(word in npc_name.lower() for word in ['marcus', 'captain', 'pete', 'rogue']):
                        relevant_npc = data
                        break
                
                if relevant_npc:
                    emotion_consistent = any(
                        expected.lower() in relevant_npc['emotion'].lower() 
                        for expected in scenario['expected_final_emotion']
                    )
                    
                    # Check score-emotion alignment
                    score = relevant_npc['score']
                    emotion = relevant_npc['emotion'].lower()
                    
                    score_emotion_aligned = (
                        (score > 0 and any(pos in emotion for pos in ['happy', 'friendly', 'pleased', 'positive'])) or
                        (score < 0 and any(neg in emotion for neg in ['angry', 'hostile', 'upset', 'negative'])) or
                        (score == 0 and any(neu in emotion for neu in ['neutral', 'indifferent']))
                    )
                else:
                    emotion_consistent = False
                    score_emotion_aligned = False
                
                consistency_results.append({
                    'scenario': scenario['npc_setup'],
                    'interactions': interactions,
                    'expected_emotions': scenario['expected_final_emotion'],
                    'final_npc_data': relevant_npc,
                    'emotion_consistent': emotion_consistent,
                    'score_emotion_aligned': score_emotion_aligned,
                    'npc_found': relevant_npc is not None
                })
            
            return {
                'scenarios': consistency_results,
                'emotion_consistency_rate': sum(1 for r in consistency_results if r['emotion_consistent']) / len(consistency_results),
                'score_alignment_rate': sum(1 for r in consistency_results if r['score_emotion_aligned']) / len(consistency_results)
            }
        
        self.results['npc_emotion_consistency'] = run_test_safely(emotion_consistency_test)
    
    def test_multiple_npc_interactions(self, engine):
        """Test handling multiple NPCs simultaneously"""
        print("  👥 Testing multiple NPC interactions...")
        
        def multiple_npc_test():
            # Start adventure
            engine.start_adventure()
            
            # Create multiple NPCs in one scene
            setup_action = "I enter a busy tavern with a bartender, a bard, and several patrons drinking and talking."
            engine.process_player_action(setup_action)
            time.sleep(0.1)
            
            # Interact with different NPCs
            multi_npc_actions = [
                "I order a drink from the bartender and tip well.",
                "I request a song from the bard and applaud enthusiastically.",
                "I join a conversation with the patrons about local news.",
                "I accidentally spill a drink on one of the patrons.",
                "I buy a round of drinks for everyone in the tavern."
            ]
            
            npc_tracking = []
            for action in multi_npc_actions:
                pre_npcs = engine.get_npc_states()
                response = engine.process_player_action(action)
                post_npcs = engine.get_npc_states()
                
                npc_tracking.append({
                    'action': action,
                    'pre_npc_count': len(pre_npcs),
                    'post_npc_count': len(post_npcs),
                    'npc_states': post_npcs.copy(),
                    'response': response
                })
                
                time.sleep(0.1)
            
            final_npcs = engine.get_npc_states()
            
            return {
                'setup_action': setup_action,
                'interactions': npc_tracking,
                'final_npc_count': len(final_npcs),
                'final_npc_states': final_npcs,
                'multiple_npcs_tracked': len(final_npcs) >= 2
            }
        
        self.results['multiple_npc_interactions'] = run_test_safely(multiple_npc_test)
    
    def test_npc_memory_integration(self, engine):
        """Test if NPC states are properly integrated with memory system"""
        print("  🧠 Testing NPC memory integration...")
        
        def npc_memory_test():
            # Start adventure
            engine.start_adventure()
            
            # Create an NPC and build relationship
            engine.process_player_action("I meet Elena, a wise librarian who knows many secrets.")
            time.sleep(0.1)
            
            engine.process_player_action("I help Elena organize ancient books and she shares valuable information.")
            time.sleep(0.1)
            
            # Get current NPC state
            current_npcs = engine.get_npc_states()
            
            # Later, reference the NPC in conversation
            memory_test_action = "I need to find Elena the librarian again for more help."
            response = engine.process_player_action(memory_test_action)
            
            # Check if the system remembers Elena and her current relationship status
            elena_mentioned = 'elena' in response.lower() or 'librarian' in response.lower()
            
            # Test if NPC data influences future interactions
            follow_up_action = "I approach Elena and ask for her assistance with my quest."
            follow_up_response = engine.process_player_action(follow_up_action)
            
            final_npcs = engine.get_npc_states()
            
            return {
                'initial_npc_creation': len(current_npcs) > 0,
                'memory_test_action': memory_test_action,
                'memory_response': response,
                'elena_mentioned_in_memory': elena_mentioned,
                'follow_up_response': follow_up_response,
                'npc_state_maintained': len(final_npcs) > 0,
                'memory_integration_working': elena_mentioned and len(final_npcs) > 0
            }
        
        self.results['npc_memory_integration'] = run_test_safely(npc_memory_test)


def run_npc_emotion_tests():
    """Run all NPC emotion tests and return results"""
    tester = NPCEmotionTests()
    return tester.run_all_tests()


if __name__ == "__main__":
    results = run_npc_emotion_tests()
    
    print("\n" + "="*50)
    print("NPC EMOTION TEST RESULTS")
    print("="*50)
    
    for test_name, result in results.items():
        print(f"\n{test_name.upper()}:")
        if result['success']:
            print(f"  ✅ PASSED")
            test_result = result['result']
            
            if test_name == 'npc_emotion_detection':
                print(f"  🎭 NPCs created: {test_result['total_npcs_created']}")
                print(f"  📊 Detection rate: {test_result['detection_success_rate']:.2%}")
            
            elif test_name == 'npc_relationship_progression':
                print(f"  📈 Relationship logic accuracy: {test_result['relationship_logic_accuracy']:.2%}")
                if test_result['final_thorin_data']:
                    print(f"  💝 Final relationship score: {test_result['final_thorin_data']['score']}")
            
            elif test_name == 'npc_emotion_consistency':
                print(f"  🎯 Emotion consistency: {test_result['emotion_consistency_rate']:.2%}")
                print(f"  📊 Score-emotion alignment: {test_result['score_alignment_rate']:.2%}")
            
            elif test_name == 'multiple_npc_interactions':
                print(f"  👥 Multiple NPCs tracked: {test_result['multiple_npcs_tracked']}")
                print(f"  🔢 Final NPC count: {test_result['final_npc_count']}")
            
            elif test_name == 'npc_memory_integration':
                print(f"  🧠 Memory integration: {'WORKING' if test_result['memory_integration_working'] else 'FAILED'}")
                print(f"  📝 NPC mentioned in memory: {test_result['elena_mentioned_in_memory']}")
        
        else:
            print(f"  ❌ FAILED: {result['error']}")