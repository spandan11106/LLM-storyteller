#!/usr/bin/env python3
# 🧪 Magical Test Laboratory 🧪
"""
🎭 Your friendly test conductor! This helpful script runs all our quality assurance spells
to make sure your AI Dungeon Master is working perfectly! ✨

Think of this as your personal testing wizard - just tell it which magic you want to verify,
and it'll make sure everything is working beautifully! 🪄
"""

import sys
import argparse
from tests.run_all_tests import run_all_tests
from tests.test_memory import run_memory_tests
from tests.test_npc_emotions import run_npc_emotion_tests
from tests.test_story_consistency import run_story_consistency_tests
from tests.test_performance import run_performance_tests


def main():
    parser = argparse.ArgumentParser(description="🎪 Test your amazing storytelling engine!")
    parser.add_argument(
        'suite', 
        nargs='?', 
        choices=['all', 'memory', 'npc', 'story', 'performance'],
        default='all',
        help='Which magical tests to run? (default: all the magic!)'
    )
    parser.add_argument(
        '--no-save', 
        action='store_true',
        help='Skip saving results (just show them to me!)'
    )
    
    args = parser.parse_args()
    
    print("🎪 Welcome to the Storytelling Magic Testing Laboratory! 🧪")
    print("="*55)
    
    if args.suite == 'all':
        print("🌟 Running ALL the magical tests! This will be thorough and amazing!")
        results = run_all_tests(save_results=not args.no_save)
    elif args.suite == 'memory':
        print("🧠 Testing the legendary memory palace! Let's see if our AI remembers everything...")
        results = run_memory_tests()
    elif args.suite == 'npc':
        print("💝 Testing NPC hearts and emotions! Making sure every character feels real...")
        results = run_npc_emotion_tests()
    elif args.suite == 'story':
        print("📖 Testing story consistency magic! Ensuring your adventures flow perfectly...")
        results = run_story_consistency_tests()
    elif args.suite == 'performance':
        print("⚡ Testing lightning-fast performance! Making sure the magic never slows down...")
        results = run_performance_tests()
    
    print("\n🎉 All tests completed! Your AI Dungeon Master has been thoroughly checked! ✨")
    
    if args.suite != 'all':
        # Show a beautiful summary for individual test adventures
        print("\n📊 MAGICAL TEST RESULTS SUMMARY:")
        for test_name, result in results.items():
            if result['success']:
                status = "✅ MAGNIFICENT! Everything works perfectly!"
            else:
                status = f"❌ Oops! We found something: {result['error']}"
            print(f"  🔮 {test_name}: {status}")


if __name__ == "__main__":
    main()