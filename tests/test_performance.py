# tests/test_performance.py
"""
Performance, timing, and scalability tests for the storytelling engine
"""

import time
import psutil
import os
from typing import Dict, List, Any

from .test_utils import TestSetup, PerformanceTester, run_test_safely


class PerformanceTests:
    """Comprehensive performance and timing tests"""
    
    def __init__(self):
        self.setup = TestSetup()
        self.results = {}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all performance tests"""
        print("⚡ Starting Performance Tests...")
        
        # Setup test environment
        engine = self.setup.setup_test_environment()
        
        try:
            # Create test character
            self.setup.create_test_character()
            
            # Run individual tests
            self.test_response_time_consistency(engine)
            self.test_memory_operation_performance(engine)
            self.test_scalability_with_conversation_count(engine)
            self.test_npc_processing_overhead(engine)
            self.test_memory_usage_growth(engine)
            
        finally:
            # Cleanup
            self.setup.teardown_test_environment()
        
        return self.results
    
    def test_response_time_consistency(self, engine):
        """Test if response times remain consistent"""
        print("  ⏱️ Testing response time consistency...")
        
        def response_time_test():
            # Start adventure
            engine.start_adventure()
            
            # Test different types of actions
            action_types = [
                {
                    'type': 'simple_action',
                    'actions': [
                        "I look around.",
                        "I check my inventory.",
                        "I listen carefully."
                    ]
                },
                {
                    'type': 'complex_action',
                    'actions': [
                        "I engage in detailed combat with the dragon, using my sword and shield while dodging its fire attacks.",
                        "I attempt to negotiate a complex trade agreement with the merchant guild involving multiple rare items.",
                        "I investigate the mysterious crime scene, examining clues and interviewing witnesses."
                    ]
                },
                {
                    'type': 'memory_intensive',
                    'actions': [
                        "I try to remember all the important people I've met on my journey.",
                        "I think about all the magical items I've discovered during my adventures.",
                        "I recall the various quests and missions I've completed so far."
                    ]
                }
            ]
            
            timing_results = {}
            
            for action_category in action_types:
                category_times = []
                
                for action in action_category['actions']:
                    timing_data = PerformanceTester.measure_response_time(engine, action, iterations=3)
                    category_times.extend(timing_data['times'])
                
                timing_results[action_category['type']] = {
                    'times': category_times,
                    'average': sum(category_times) / len(category_times),
                    'min': min(category_times),
                    'max': max(category_times),
                    'variance': self._calculate_variance(category_times)
                }
            
            return {
                'timing_by_category': timing_results,
                'overall_average': sum(sum(data['times']) for data in timing_results.values()) / sum(len(data['times']) for data in timing_results.values()),
                'acceptable_performance': all(data['average'] < 10.0 for data in timing_results.values())  # Under 10 seconds
            }
        
        self.results['response_time_consistency'] = run_test_safely(response_time_test)
    
    def test_memory_operation_performance(self, engine):
        """Test performance of memory operations"""
        print("  🧠 Testing memory operation performance...")
        
        def memory_performance_test():
            # Start adventure
            engine.start_adventure()
            
            # Create some initial conversations for context
            for i in range(10):
                engine.process_player_action(f"I perform action number {i} in my adventure.")
                time.sleep(0.01)
            
            # Test memory operations
            memory_metrics = PerformanceTester.measure_memory_operations(engine)
            
            # Test search performance with different query sizes
            search_performance = []
            test_queries = [
                "action",  # Short query
                "adventure journey quest",  # Medium query
                "I am looking for information about my previous adventures and the people I have met along the way"  # Long query
            ]
            
            for query in test_queries:
                start_time = time.time()
                results = engine.memory.retrieve_relevant_memories(query, max_results=5)
                search_time = time.time() - start_time
                
                search_performance.append({
                    'query': query,
                    'query_length': len(query),
                    'search_time': search_time,
                    'results_count': len(results)
                })
            
            # Test fact extraction performance
            fact_test_texts = [
                "I meet the wizard Gandalf who gives me a magic ring.",
                "The dragon Smaug guards a vast treasure in the Lonely Mountain.",
                "Princess Zelda asks me to rescue her from the evil Ganondorf in Hyrule Castle."
            ]
            
            fact_extraction_times = []
            for text in fact_test_texts:
                start_time = time.time()
                facts = engine.memory.extract_facts(text)
                extraction_time = time.time() - start_time
                fact_extraction_times.append(extraction_time)
            
            return {
                'basic_operations': memory_metrics,
                'search_performance': search_performance,
                'fact_extraction_times': fact_extraction_times,
                'average_search_time': sum(s['search_time'] for s in search_performance) / len(search_performance),
                'average_extraction_time': sum(fact_extraction_times) / len(fact_extraction_times),
                'memory_performance_good': memory_metrics['search_time'] < 1.0 and memory_metrics['save_time'] < 0.5
            }
        
        self.results['memory_operation_performance'] = run_test_safely(memory_performance_test)
    
    def test_scalability_with_conversation_count(self, engine):
        """Test how performance scales with number of conversations"""
        print("  📈 Testing scalability with conversation count...")
        
        def scalability_test():
            # Start adventure
            engine.start_adventure()
            
            # Test performance at different conversation counts
            conversation_thresholds = [10, 25, 50, 75, 100]
            scalability_data = []
            
            for threshold in conversation_thresholds:
                # Add conversations to reach threshold
                current_count = engine.memory.get_summary()['total_conversations']
                conversations_to_add = max(0, threshold - current_count)
                
                for i in range(conversations_to_add):
                    engine.process_player_action(f"I perform scalability test action {current_count + i}.")
                    time.sleep(0.001)  # Minimal delay
                
                # Measure performance at this threshold
                test_action = "I check my current situation and think about my next move."
                timing_data = PerformanceTester.measure_response_time(engine, test_action, iterations=3)
                
                # Measure memory search performance
                start_time = time.time()
                search_results = engine.memory.retrieve_relevant_memories("test action", max_results=5)
                search_time = time.time() - start_time
                
                scalability_data.append({
                    'conversation_count': engine.memory.get_summary()['total_conversations'],
                    'response_time': timing_data['average'],
                    'search_time': search_time,
                    'memory_usage_mb': self._get_memory_usage()
                })
            
            # Analyze scaling trends
            response_time_trend = self._calculate_trend([d['response_time'] for d in scalability_data])
            search_time_trend = self._calculate_trend([d['search_time'] for d in scalability_data])
            memory_usage_trend = self._calculate_trend([d['memory_usage_mb'] for d in scalability_data])
            
            return {
                'scalability_data': scalability_data,
                'response_time_trend': response_time_trend,
                'search_time_trend': search_time_trend,
                'memory_usage_trend': memory_usage_trend,
                'scales_well': response_time_trend < 0.1 and search_time_trend < 0.01  # Reasonable scaling
            }
        
        self.results['scalability'] = run_test_safely(scalability_test)
    
    def test_npc_processing_overhead(self, engine):
        """Test overhead of NPC emotion processing"""
        print("  👥 Testing NPC processing overhead...")
        
        def npc_overhead_test():
            # Start adventure
            engine.start_adventure()
            
            # Baseline: Actions without NPCs
            baseline_action = "I examine my equipment and check my supplies."
            baseline_timing = PerformanceTester.measure_response_time(engine, baseline_action, iterations=5)
            
            # Create NPCs through interactions
            npc_creation_actions = [
                "I meet Bob the baker who is cheerful and friendly.",
                "I encounter Alice the warrior who is stern and disciplined.",
                "I find Charlie the merchant who is greedy but useful."
            ]
            
            for action in npc_creation_actions:
                engine.process_player_action(action)
                time.sleep(0.1)
            
            # Actions that interact with NPCs
            npc_interaction_actions = [
                "I greet Bob warmly and ask about his bread.",
                "I challenge Alice to a friendly sparring match.",
                "I negotiate with Charlie for better prices."
            ]
            
            npc_timing_results = []
            for action in npc_interaction_actions:
                timing_data = PerformanceTester.measure_response_time(engine, action, iterations=3)
                npc_timing_results.append(timing_data['average'])
            
            average_npc_time = sum(npc_timing_results) / len(npc_timing_results)
            npc_overhead = average_npc_time - baseline_timing['average']
            
            return {
                'baseline_time': baseline_timing['average'],
                'npc_interaction_times': npc_timing_results,
                'average_npc_time': average_npc_time,
                'npc_overhead': npc_overhead,
                'overhead_percentage': (npc_overhead / baseline_timing['average']) * 100,
                'acceptable_overhead': npc_overhead < 2.0  # Less than 2 seconds overhead
            }
        
        self.results['npc_processing_overhead'] = run_test_safely(npc_overhead_test)
    
    def test_memory_usage_growth(self, engine):
        """Test memory usage growth over time"""
        print("  📊 Testing memory usage growth...")
        
        def memory_usage_test():
            # Start adventure
            engine.start_adventure()
            
            initial_memory = self._get_memory_usage()
            memory_snapshots = [{'conversations': 0, 'memory_mb': initial_memory}]
            
            # Add conversations in batches and measure memory
            batch_sizes = [10, 20, 30, 40, 50]
            
            for batch_size in batch_sizes:
                # Add batch of conversations
                for i in range(batch_size):
                    action = f"I perform memory test action {engine.memory.get_summary()['total_conversations'] + 1} involving various characters and situations."
                    engine.process_player_action(action)
                    time.sleep(0.001)
                
                current_memory = self._get_memory_usage()
                memory_snapshots.append({
                    'conversations': engine.memory.get_summary()['total_conversations'],
                    'memory_mb': current_memory
                })
                
                # Force garbage collection to get accurate readings
                import gc
                gc.collect()
                time.sleep(0.1)
            
            # Calculate memory growth rate
            memory_growth = memory_snapshots[-1]['memory_mb'] - memory_snapshots[0]['memory_mb']
            conversations_added = memory_snapshots[-1]['conversations']
            memory_per_conversation = memory_growth / conversations_added if conversations_added > 0 else 0
            
            return {
                'memory_snapshots': memory_snapshots,
                'initial_memory_mb': initial_memory,
                'final_memory_mb': memory_snapshots[-1]['memory_mb'],
                'total_memory_growth_mb': memory_growth,
                'conversations_added': conversations_added,
                'memory_per_conversation_mb': memory_per_conversation,
                'reasonable_memory_usage': memory_per_conversation < 1.0  # Less than 1MB per conversation
            }
        
        self.results['memory_usage_growth'] = run_test_safely(memory_usage_test)
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values"""
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate simple linear trend (slope) of values"""
        if len(values) < 2:
            return 0.0
        n = len(values)
        x_values = list(range(n))
        x_mean = sum(x_values) / n
        y_mean = sum(values) / n
        
        numerator = sum((x_values[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        return numerator / denominator if denominator != 0 else 0.0
    
    def _get_memory_usage(self) -> float:
        """Get current process memory usage in MB"""
        try:
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            return memory_info.rss / 1024 / 1024  # Convert to MB
        except:
            return 0.0


def run_performance_tests():
    """Run all performance tests and return results"""
    tester = PerformanceTests()
    return tester.run_all_tests()


if __name__ == "__main__":
    results = run_performance_tests()
    
    print("\n" + "="*50)
    print("PERFORMANCE TEST RESULTS")
    print("="*50)
    
    for test_name, result in results.items():
        print(f"\n{test_name.upper()}:")
        if result['success']:
            print(f"  ✅ PASSED")
            test_result = result['result']
            
            if test_name == 'response_time_consistency':
                print(f"  ⏱️ Overall average: {test_result['overall_average']:.2f}s")
                print(f"  ✅ Acceptable performance: {test_result['acceptable_performance']}")
            
            elif test_name == 'memory_operation_performance':
                print(f"  🔍 Average search time: {test_result['average_search_time']:.3f}s")
                print(f"  🧠 Average extraction time: {test_result['average_extraction_time']:.3f}s")
                print(f"  ✅ Good performance: {test_result['memory_performance_good']}")
            
            elif test_name == 'scalability':
                print(f"  📈 Response time trend: {test_result['response_time_trend']:.4f}")
                print(f"  🔍 Search time trend: {test_result['search_time_trend']:.4f}")
                print(f"  ✅ Scales well: {test_result['scales_well']}")
            
            elif test_name == 'npc_processing_overhead':
                print(f"  👥 NPC overhead: {test_result['npc_overhead']:.2f}s ({test_result['overhead_percentage']:.1f}%)")
                print(f"  ✅ Acceptable overhead: {test_result['acceptable_overhead']}")
            
            elif test_name == 'memory_usage_growth':
                print(f"  📊 Memory per conversation: {test_result['memory_per_conversation_mb']:.3f}MB")
                print(f"  💾 Total growth: {test_result['total_memory_growth_mb']:.1f}MB")
                print(f"  ✅ Reasonable usage: {test_result['reasonable_memory_usage']}")
        
        else:
            print(f"  ❌ FAILED: {result['error']}")