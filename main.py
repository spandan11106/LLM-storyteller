# main.py - Your Gateway to Amazing AI Storytelling Adventures!

"""
🧙‍♂️ Welcome to Your Personal AI Storyteller with Amazing Memory!

This is your magical portal to incredible adventures! Whether you prefer
a beautiful graphical interface or a classic text-based experience,
your AI storyteller is ready to create unforgettable journeys.

Ready to embark on the adventure of a lifetime? Let's go! 🚀
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from storyteller.ui.gui import run_gui
from storyteller.core.engine import StorytellingEngine


def run_cli():
    """🖥️ Experience the classic text-based adventure magic!"""
    print("🎭 === Welcome to Your AI Storytelling Adventure! ===")
    print("✨ Get ready for an incredible journey with your personal AI dungeon master!")
    
    engine = StorytellingEngine()
    
    # Check if character exists
    if not engine.has_character():
        print("\n🎪 Time to create your heroic character!")
        print("Let's bring your adventurer to life with some basic details...")
        
        name = input("📝 What's your hero's name? ")
        background = input("📚 What's their background story? ")
        personality = input("🎭 How would you describe their personality? ")
        goals = input("🎯 What drives them? What are their goals? ")
        
        print("\n⚔️ Now let's set your hero's abilities (just press Enter for default 10):")
        try:
            strength = int(input("💪 Strength [10]: ") or "10")
            dexterity = int(input("🏃 Dexterity [10]: ") or "10")
            intelligence = int(input("🧠 Intelligence [10]: ") or "10")
            charisma = int(input("😊 Charisma [10]: ") or "10")
        except ValueError:
            strength = dexterity = intelligence = charisma = 10
            print("✨ Using default abilities for your hero!")
        
        result = engine.create_character(
            name, background, personality, goals,
            strength=strength, dexterity=dexterity,
            intelligence=intelligence, charisma=charisma
        )
        print(f"\n🎉 {result}")
    
    
    # Start adventure
    if not engine.game_started:
        print("\n🚀 Launching your epic adventure...")
        intro = engine.start_adventure()
        print(f"\n🧙‍♂️ Your AI Dungeon Master: {intro}")
    
    # Main game loop
    print("\n" + "🌟"*25)
    print("🎊 Your Adventure Begins! Type 'quit' when you're ready to leave this magical world.")
    print("🌟"*25)

    while True:
        try:
            action = input("\n🎮 What would you like to do? ").strip()
            if action.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thanks for the amazing adventure! See you next time!")
                break
            
            if action:
                response = engine.process_player_action(action)
                print(f"\n🧙‍♂️ DM: {response}")
            else:
                print("💭 Take your time! What would you like to do?")
        
        except KeyboardInterrupt:
            print("\n\n✨ Adventure paused! Thanks for playing!")
            break
        except Exception as e:
            print(f"⚠️ Oops, something unexpected happened: {e}")
            print("💡 Don't worry, your adventure continues!")
    
    print("\n🎉 What an incredible journey! Your story will be remembered!")


def main():
    """🎪 The main show begins here!"""
    print("🌟 Welcome to Your Personal AI Storyteller! 🌟")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        print("📺 Starting classic text-based adventure mode...")
        run_cli()
    else:
        print("🖼️ Launching beautiful graphical interface...")
        run_gui()


if __name__ == "__main__":
    main()