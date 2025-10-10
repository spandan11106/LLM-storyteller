# storyteller/config.py
"""
🎛️ The Control Center for Your Amazing Storytelling Adventure!

This is where all the magic settings live - think of it as the backstage
area where we fine-tune your storytelling experience to be absolutely perfect!
"""

import os
from typing import Dict, Any

# Let's get our environment ready for adventure!
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Great! Loaded all your secret settings from .env file")
except ImportError:
    print("📝 Note: Using system environment (that's totally fine too!)")

# 🤖 AI Brain Configuration - This is where we talk to our smart AI friend
LLM_MODEL = "llama-3.1-8b-instant"  # Our storytelling AI's brain model
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if GROQ_API_KEY:
    print("🔑 Perfect! Your AI connection key is ready to go")
else:
    print("⚠️  Heads up: Don't forget to add your GROQ_API_KEY to get started!")

# 🧠 Memory Magic Configuration - How your AI remembers everything
MEMORY_SAVE_PATH = "memory_docs"  # Where all the epic memories are stored
MAX_CONVERSATION_HISTORY = 50     # Keeps the last 50 chats fresh in memory
MAX_RETRIEVAL_RESULTS = 5         # How many old memories to dig up for context

# 🔍 Smart Memory Search Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"      # The brain that understands memories
VECTOR_DB_COLLECTION = "story_memory"      # Our memory treasure vault

# ⚔️ Character Power Stats - Default abilities for new heroes
DEFAULT_ATTRIBUTES = {
    'strength': 10,      # How strong your hero is
    'dexterity': 10,     # How quick and agile they are
    'intelligence': 10,  # How smart and wise they are
    'charisma': 10       # How charming and persuasive they are
}

# 🔍 Smart Pattern Recognition - How we spot important stuff in your story
ENTITY_PATTERNS = [
    r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Cool names (like Sir Galahad)
    r'\b(?:sword|shield|armor|weapon|potion|key|treasure|gold|silver)\b',  # Epic loot!
    r'\b(?:castle|tavern|forest|mountain|village|city|tower|dungeon)\b',  # Amazing places
]

RELATIONSHIP_PATTERNS = [
    r'(\w+)\s+(?:gives?|gave|handed?|offered?)\s+(\w+)',         # Who gave what to whom
    r'(\w+)\s+(?:tells?|told|said?|mentioned?)\s+(?:to\s+)?(\w+)',  # Who talked to whom
    r'(\w+)\s+(?:attacks?|attacked?|fights?|fought?)\s+(\w+)',   # Epic battles!
    r'(\w+)\s+(?:helps?|helped?|assists?|assisted?)\s+(\w+)',    # Helpful friendships
]

# 🌟 Keywords That Make Stories EPIC - We pay extra attention to these!
IMPORTANCE_KEYWORDS = [
    'quest', 'mission', 'treasure', 'secret', 'magic', 'prophecy',
    'death', 'betrayal', 'discovery', 'revelation', 'ancient',
    'powerful', 'dangerous', 'legendary', 'cursed', 'blessed'
]

# 🖼️ User Interface Magic - Making everything look awesome
GUI_WINDOW_SIZE = "1000x700"
GUI_TITLE = "🧙‍♂️ Your Personal AI Storyteller with Amazing Memory!"