# storyteller/__init__.py
"""
🧙‍♂️ Your Personal AI Storyteller with Amazing Memory!

Hey there, adventurer! Welcome to the most incredible storytelling system
you've ever encountered. This isn't just any ordinary AI - it actually 
remembers everything that happens in your adventures, creating truly 
immersive experiences that continue to grow and evolve!

Think of it as having your own personal dungeon master who never forgets
a single detail of your epic journey. Pretty cool, right?
"""

__version__ = "1.0.0"
__author__ = "Spandan - The Memory Magic Creator"

from .core.engine import StorytellingEngine
from .core.character import Character
from .core.memory import DocumentMemorySystem

# Quick and easy way to get started with your adventure!
def create_engine():
    """Fire up a brand new storytelling adventure - let the magic begin!"""
    return StorytellingEngine()

__all__ = [
    'StorytellingEngine',
    'Character', 
    'DocumentMemorySystem',
    'create_engine'
]