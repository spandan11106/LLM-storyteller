# storyteller/core/__init__.py
"""
🎪 The Heart of the Magic - Core Storytelling Components!

This is where all the essential ingredients for amazing adventures live!
Think of this as the engine room of your storytelling experience, containing
all the fundamental pieces that make the magic happen.
"""

from .character import Character
from .memory import DocumentMemorySystem, MemoryEntry  
from .engine import StorytellingEngine

__all__ = [
    'Character',              # Your amazing hero character
    'DocumentMemorySystem',   # The incredible memory palace
    'MemoryEntry',           # Individual precious memories
    'StorytellingEngine'     # The master orchestrator of adventures
]