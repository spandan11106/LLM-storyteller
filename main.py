# main.py - Main entry point for the storytelling application

"""
AI Storyteller with Long-Term Memory

This is the main entry point for the storytelling application.
You can run either the GUI or command-line version.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from storyteller.ui.gui import run_gui
from storyteller.core.engine import StorytellingEngine


def run_cli():
    """Run a simple command-line version"""
    print("=== AI Storyteller CLI ===")
    
    engine = StorytellingEngine()
    
    # Check if character exists
    if not engine.has_character():
        print("\nNo character found. Let's create one!")
        name = input("Character name: ")
        background = input("Background: ")
        personality = input("Personality: ")
        goals = input("Goals: ")
        
        print("\nAttributes (press enter for default 10):")
        try:
            strength = int(input("Strength [10]: ") or "10")
            dexterity = int(input("Dexterity [10]: ") or "10")
            intelligence = int(input("Intelligence [10]: ") or "10")
            charisma = int(input("Charisma [10]: ") or "10")
        except ValueError:
            strength = dexterity = intelligence = charisma = 10
        
        result = engine.create_character(
            name, background, personality, goals,
            strength=strength, dexterity=dexterity,
            intelligence=intelligence, charisma=charisma
        )
        print(f"\n{result}")
    
    # Start adventure
    if not engine.game_started:
        print("\nStarting adventure...")
        intro = engine.start_adventure()
        print(f"\nDM: {intro}")
    
    # Main game loop
    print("\n" + "="*50)
    print("Adventure begins! Type 'quit' to exit.")
    print("="*50)
    
    while True:
        try:
            action = input("\nWhat do you do? ").strip()
            if action.lower() in ['quit', 'exit', 'q']:
                break
            
            if action:
                response = engine.process_player_action(action)
                print(f"\nDM: {response}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nThanks for playing!")


def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        run_cli()
    else:
        run_gui()


if __name__ == "__main__":
    main()