#!/usr/bin/env python3
# run_tests.py
"""
Simple script to run individual test suites or all tests
"""

import sys
import argparse
from tests.run_all_tests import run_all_tests
from tests.test_memory import run_memory_tests
from tests.test_npc_emotions import run_npc_emotion_tests
from tests.test_story_consistency import run_story_consistency_tests
from tests.test_performance import run_performance_tests


def main():
    parser = argparse.ArgumentParser(description="Run storytelling engine tests")
    parser.add_argument(
        'suite', 
        nargs='?', 
        choices=['all', 'memory', 'npc', 'story', 'performance'],
        default='all',
        help='Test suite to run (default: all)'
    )
    parser.add_argument(
        '--no-save', 
        action='store_true',
        help='Do not save results to files'
    )
    
    args = parser.parse_args()
    
    print("🧪 Storytelling Engine Test Runner")
    print("="*40)
    
    if args.suite == 'all':
        print("Running all test suites...")
        results = run_all_tests(save_results=not args.no_save)
    elif args.suite == 'memory':
        print("Running memory tests...")
        results = run_memory_tests()
    elif args.suite == 'npc':
        print("Running NPC emotion tests...")
        results = run_npc_emotion_tests()
    elif args.suite == 'story':
        print("Running story consistency tests...")
        results = run_story_consistency_tests()
    elif args.suite == 'performance':
        print("Running performance tests...")
        results = run_performance_tests()
    
    print("\n✅ Test execution completed!")
    
    if args.suite != 'all':
        # Print summary for individual test suites
        print("\nSUMMARY:")
        for test_name, result in results.items():
            status = "✅ PASSED" if result['success'] else f"❌ FAILED: {result['error']}"
            print(f"  {test_name}: {status}")


if __name__ == "__main__":
    main()