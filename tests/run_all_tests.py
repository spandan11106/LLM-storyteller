# 🎪 Grand Test Conductor - The Ultimate Testing Adventure! ✨
"""
🎭 Your magical test orchestrator that runs ALL the amazing tests and creates beautiful reports!

This is the grand finale of our testing suite - it conducts the entire symphony of tests:
- 🧠 Memory palace challenges (including the famous needle-in-haystack!)
- 💝 NPC heart and emotion tests
- 📖 Epic story consistency verification  
- ⚡ Lightning-fast performance benchmarks

Watch as it creates detailed reports showing exactly how legendary your AI storyteller is! 🌟
"""

import json
import time
from datetime import datetime
from typing import Dict, Any

from .test_memory import run_memory_tests
from .test_npc_emotions import run_npc_emotion_tests
from .test_story_consistency import run_story_consistency_tests
from .test_performance import run_performance_tests


class TestReportGenerator:
    """📊 Your magical report wizard that creates beautiful test summaries!"""
    
    @staticmethod
    def generate_summary_report(all_results: Dict[str, Any]) -> Dict[str, Any]:
        """✨ Generate a magnificent overview of all your test adventures!"""
        summary = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_suites': {},
            'overall_score': 0.0,
            'timestamp': datetime.now().isoformat()
        }
        
        for suite_name, suite_results in all_results.items():
            suite_summary = {
                'total': len(suite_results),
                'passed': sum(1 for result in suite_results.values() if result['success']),
                'failed': sum(1 for result in suite_results.values() if not result['success']),
                'success_rate': 0.0
            }
            
            if suite_summary['total'] > 0:
                suite_summary['success_rate'] = suite_summary['passed'] / suite_summary['total']
            
            summary['test_suites'][suite_name] = suite_summary
            summary['total_tests'] += suite_summary['total']
            summary['passed_tests'] += suite_summary['passed']
            summary['failed_tests'] += suite_summary['failed']
        
        if summary['total_tests'] > 0:
            summary['overall_score'] = summary['passed_tests'] / summary['total_tests']
        
        return summary
    
    @staticmethod
    def generate_detailed_report(all_results: Dict[str, Any]) -> str:
        """Generate detailed text report"""
        report_lines = []
        report_lines.append("="*80)
        report_lines.append("STORYTELLING ENGINE - COMPREHENSIVE TEST REPORT")
        report_lines.append("="*80)
        report_lines.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Summary section
        summary = TestReportGenerator.generate_summary_report(all_results)
        report_lines.append("EXECUTIVE SUMMARY")
        report_lines.append("-" * 40)
        report_lines.append(f"Overall Score: {summary['overall_score']:.1%}")
        report_lines.append(f"Total Tests: {summary['total_tests']}")
        report_lines.append(f"Passed: {summary['passed_tests']} | Failed: {summary['failed_tests']}")
        report_lines.append("")
        
        # Per-suite breakdown
        for suite_name, suite_summary in summary['test_suites'].items():
            status = "✅ EXCELLENT" if suite_summary['success_rate'] >= 0.9 else \
                    "🟡 GOOD" if suite_summary['success_rate'] >= 0.7 else \
                    "⚠️ NEEDS IMPROVEMENT" if suite_summary['success_rate'] >= 0.5 else \
                    "❌ CRITICAL ISSUES"
            
            report_lines.append(f"{suite_name.upper()}: {suite_summary['success_rate']:.1%} {status}")
        
        report_lines.append("")
        report_lines.append("="*80)
        
        # Detailed results per suite
        for suite_name, suite_results in all_results.items():
            report_lines.append(f"\n{suite_name.upper()} DETAILED RESULTS")
            report_lines.append("-" * 60)
            
            for test_name, result in suite_results.items():
                status_icon = "✅" if result['success'] else "❌"
                report_lines.append(f"{status_icon} {test_name}")
                
                if result['success'] and result['result']:
                    # Add key metrics for successful tests
                    test_result = result['result']
                    
                    if suite_name == 'memory_tests':
                        if test_name == 'needle_haystack':
                            success = test_result.get('memory_retrieval_success', False)
                            position = test_result.get('needle_position', 0)
                            haystack_size = test_result.get('haystack_size', 0)
                            report_lines.append(f"    📍 Needle at position {position}/{haystack_size}: {'FOUND' if success else 'NOT FOUND'}")
                        
                        elif test_name == 'fact_extraction':
                            facts_extracted = test_result.get('facts_extracted', 0)
                            working = test_result.get('extraction_working', False)
                            report_lines.append(f"    📊 Facts extracted: {facts_extracted} (Working: {working})")
                        
                        elif test_name == 'search_accuracy':
                            accuracy = test_result.get('overall_accuracy', 0)
                            report_lines.append(f"    🎯 Search accuracy: {accuracy:.1%}")
                    
                    elif suite_name == 'npc_emotion_tests':
                        if test_name == 'npc_emotion_detection':
                            detection_rate = test_result.get('detection_success_rate', 0)
                            npcs_created = test_result.get('total_npcs_created', 0)
                            report_lines.append(f"    🎭 Detection rate: {detection_rate:.1%} ({npcs_created} NPCs)")
                        
                        elif test_name == 'npc_relationship_progression':
                            accuracy = test_result.get('relationship_logic_accuracy', 0)
                            report_lines.append(f"    💝 Relationship logic: {accuracy:.1%}")
                        
                        elif test_name == 'npc_emotion_consistency':
                            consistency = test_result.get('emotion_consistency_rate', 0)
                            alignment = test_result.get('score_alignment_rate', 0)
                            report_lines.append(f"    🎯 Emotion consistency: {consistency:.1%}, Alignment: {alignment:.1%}")
                    
                    elif suite_name == 'story_consistency_tests':
                        if test_name == 'character_trait_consistency':
                            consistency = test_result.get('overall_consistency', 0)
                            report_lines.append(f"    🎭 Trait consistency: {consistency:.1%}")
                        
                        elif test_name == 'narrative_continuity':
                            continuity = test_result.get('continuity_score', 0)
                            report_lines.append(f"    📜 Narrative continuity: {continuity:.1%}")
                        
                        elif test_name == 'world_state_consistency':
                            world_consistency = test_result.get('consistency_rate', 0)
                            report_lines.append(f"    🌍 World state consistency: {world_consistency:.1%}")
                    
                    elif suite_name == 'performance_tests':
                        if test_name == 'response_time_consistency':
                            avg_time = test_result.get('overall_average', 0)
                            acceptable = test_result.get('acceptable_performance', False)
                            report_lines.append(f"    ⏱️ Average response: {avg_time:.2f}s (Acceptable: {acceptable})")
                        
                        elif test_name == 'scalability':
                            scales_well = test_result.get('scales_well', False)
                            report_lines.append(f"    📈 Scales well: {scales_well}")
                        
                        elif test_name == 'memory_usage_growth':
                            per_conv = test_result.get('memory_per_conversation_mb', 0)
                            reasonable = test_result.get('reasonable_memory_usage', False)
                            report_lines.append(f"    📊 Memory/conversation: {per_conv:.3f}MB (Reasonable: {reasonable})")
                
                elif not result['success']:
                    report_lines.append(f"    ❌ Error: {result['error']}")
                
                report_lines.append("")
        
        # Recommendations section
        report_lines.append("\nRECOMMendATIONS")
        report_lines.append("-" * 40)
        
        recommendations = TestReportGenerator._generate_recommendations(summary, all_results)
        for recommendation in recommendations:
            report_lines.append(f"• {recommendation}")
        
        return "\n".join(report_lines)
    
    @staticmethod
    def _generate_recommendations(summary: Dict[str, Any], all_results: Dict[str, Any]) -> list:
        """Generate actionable recommendations based on test results"""
        recommendations = []
        
        # Overall performance recommendations
        if summary['overall_score'] < 0.7:
            recommendations.append("Overall test score is below 70%. Consider reviewing failed tests and implementing fixes.")
        
        # Memory-specific recommendations
        memory_results = all_results.get('memory_tests', {})
        if 'needle_haystack' in memory_results and memory_results['needle_haystack']['success']:
            needle_result = memory_results['needle_haystack']['result']
            if not needle_result.get('memory_retrieval_success', False):
                recommendations.append("Long-term memory retrieval failed. Consider improving search algorithms or fact extraction.")
        
        # NPC emotion recommendations
        npc_results = all_results.get('npc_emotion_tests', {})
        if 'npc_emotion_detection' in npc_results and npc_results['npc_emotion_detection']['success']:
            detection_result = npc_results['npc_emotion_detection']['result']
            if detection_result.get('detection_success_rate', 0) < 0.8:
                recommendations.append("NPC detection rate is low. Review NPC identification logic in text processing.")
        
        # Performance recommendations
        perf_results = all_results.get('performance_tests', {})
        if 'response_time_consistency' in perf_results and perf_results['response_time_consistency']['success']:
            timing_result = perf_results['response_time_consistency']['result']
            if not timing_result.get('acceptable_performance', True):
                recommendations.append("Response times are too slow. Consider optimizing LLM calls or memory operations.")
        
        # Story consistency recommendations
        story_results = all_results.get('story_consistency_tests', {})
        if 'character_trait_consistency' in story_results and story_results['character_trait_consistency']['success']:
            trait_result = story_results['character_trait_consistency']['result']
            if trait_result.get('overall_consistency', 0) < 0.7:
                recommendations.append("Character trait consistency is low. Improve character context in prompts.")
        
        if not recommendations:
            recommendations.append("All tests performing well! Consider adding more edge cases to test suite.")
        
        return recommendations


def run_all_tests(save_results: bool = True) -> Dict[str, Any]:
    """Run all test suites and return comprehensive results"""
    print("🚀 Starting Comprehensive Test Suite")
    print("="*50)
    
    start_time = time.time()
    all_results = {}
    
    # Run each test suite
    test_suites = [
        ('memory_tests', run_memory_tests),
        ('npc_emotion_tests', run_npc_emotion_tests),
        ('story_consistency_tests', run_story_consistency_tests),
        ('performance_tests', run_performance_tests)
    ]
    
    for suite_name, test_function in test_suites:
        print(f"\n🔧 Running {suite_name}...")
        suite_start = time.time()
        
        try:
            results = test_function()
            all_results[suite_name] = results
            suite_time = time.time() - suite_start
            print(f"✅ {suite_name} completed in {suite_time:.2f}s")
        except Exception as e:
            print(f"❌ {suite_name} failed: {e}")
            all_results[suite_name] = {'error': str(e)}
    
    total_time = time.time() - start_time
    print(f"\n🏁 All tests completed in {total_time:.2f}s")
    
    # Generate reports
    summary = TestReportGenerator.generate_summary_report(all_results)
    detailed_report = TestReportGenerator.generate_detailed_report(all_results)
    
    # Save results if requested
    if save_results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        json_filename = f"test_results_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump({
                'summary': summary,
                'detailed_results': all_results,
                'execution_time_seconds': total_time
            }, f, indent=2)
        
        # Save text report
        report_filename = f"test_report_{timestamp}.txt"
        with open(report_filename, 'w') as f:
            f.write(detailed_report)
        
        print(f"\n📄 Results saved to {json_filename} and {report_filename}")
    
    # Print summary
    print("\n" + "="*50)
    print("FINAL SUMMARY")
    print("="*50)
    print(f"Overall Score: {summary['overall_score']:.1%}")
    print(f"Tests: {summary['passed_tests']}/{summary['total_tests']} passed")
    
    for suite_name, suite_summary in summary['test_suites'].items():
        status = "✅" if suite_summary['success_rate'] >= 0.8 else "⚠️" if suite_summary['success_rate'] >= 0.6 else "❌"
        print(f"{status} {suite_name}: {suite_summary['success_rate']:.1%}")
    
    return {
        'summary': summary,
        'detailed_results': all_results,
        'report': detailed_report
    }


if __name__ == "__main__":
    # Install required package for performance monitoring
    try:
        import psutil
    except ImportError:
        print("Installing psutil for performance monitoring...")
        import subprocess
        subprocess.check_call(["pip", "install", "psutil"])
        import psutil
    
    # Run all tests
    results = run_all_tests(save_results=True)
    
    print("\n" + "="*50)
    print("Test suite execution completed!")
    print("Check the generated files for detailed results.")
    print("="*50)