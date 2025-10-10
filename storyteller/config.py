# storyteller/config.py
"""
Configuration settings for the storytelling engine
"""

import os
from typing import Dict, Any

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env file")
except ImportError:
    print("Warning: python-dotenv not available, using system environment only")

# LLM Configuration
LLM_MODEL = "llama-3.1-8b-instant"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if GROQ_API_KEY:
    print("GROQ API key loaded successfully")
else:
    print("Warning: GROQ_API_KEY not found in environment")

# Memory Configuration
MEMORY_SAVE_PATH = "memory_docs"
MAX_CONVERSATION_HISTORY = 50  # Keep last 50 conversations in memory
MAX_RETRIEVAL_RESULTS = 5      # Max memories to retrieve for context

# Embedding Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
VECTOR_DB_COLLECTION = "story_memory"

# Character Attributes
DEFAULT_ATTRIBUTES = {
    'strength': 10,
    'dexterity': 10, 
    'intelligence': 10,
    'charisma': 10
}

# Fact Extraction Patterns
ENTITY_PATTERNS = [
    r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Proper nouns
    r'\b(?:sword|shield|armor|weapon|potion|key|treasure|gold|silver)\b',  # Items
    r'\b(?:castle|tavern|forest|mountain|village|city|tower|dungeon)\b',  # Places
]

RELATIONSHIP_PATTERNS = [
    r'(\w+)\s+(?:gives?|gave|handed?|offered?)\s+(\w+)',
    r'(\w+)\s+(?:tells?|told|said?|mentioned?)\s+(?:to\s+)?(\w+)',
    r'(\w+)\s+(?:attacks?|attacked?|fights?|fought?)\s+(\w+)',
    r'(\w+)\s+(?:helps?|helped?|assists?|assisted?)\s+(\w+)',
]

# Importance Keywords
IMPORTANCE_KEYWORDS = [
    'quest', 'mission', 'treasure', 'secret', 'magic', 'prophecy',
    'death', 'betrayal', 'discovery', 'revelation', 'ancient',
    'powerful', 'dangerous', 'legendary', 'cursed', 'blessed'
]

# UI Configuration
GUI_WINDOW_SIZE = "1000x700"
GUI_TITLE = "AI Storyteller with Long-Term Memory"