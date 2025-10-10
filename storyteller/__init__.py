# storyteller/__init__.py
"""
AI Storyteller with Long-Term Memory

A sophisticated storytelling system that creates immersive adventures
with persistent character memory across multiple sessions.
"""

__version__ = "1.0.0"
__author__ = "Spandan"

from .core.engine import StorytellingEngine
from .core.character import Character
from .core.memory import DocumentMemorySystem

# Convenience imports for easy access
def create_engine():
    """Create a new storytelling engine instance"""
    return StorytellingEngine()

__all__ = [
    'StorytellingEngine',
    'Character', 
    'DocumentMemorySystem',
    'create_engine'
]