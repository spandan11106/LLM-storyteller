import os
from dotenv import load_dotenv

load_dotenv()

# --- API and Model Configuration ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
LLM_MODEL = "llama-3.1-8b-instant" 

# --- Memory Configuration ---
WORKING_MEMORY_SIZE = 10
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DB_COLLECTION_NAME = "episodic_memory"

# --- Quest Configuration ---
INITIAL_QUEST_ID = "The Lord's Summons"

# --- D&D System Prompt & Rules ---
GAME_SYSTEM_PROMPT = (
    "You are a skilled Dungeon Master for a Dungeons & Dragons (D&D) fantasy game. "
    "Your tone is descriptive and immersive. "
    "1. **Describe the Scene:** Use sensory details. What does the player see, hear, and smell? "
    "2. **Be Concise:** Keep descriptions to 2-5 sentences. "
    "3. **Drive the Action:** ALWAYS end by asking 'What do you do?' and often present 2-3 clear, numbered choices. "
    "4. **Use D&D Language:** Refer to actions as 'skill checks' and use D&D terminology. "
    "5. **Adhere to Facts:** You will be given facts about the world and the player character. You MUST treat these as absolute truth."
)

# Simplified D&D rules for character creation and skill checks
DND_RULES = {
    "classes": {
        "Fighter": {"modifier": "strength", "value": 3},
        "Rogue": {"modifier": "dexterity", "value": 3},
        "Wizard": {"modifier": "intelligence", "value": 3}
    },
    "skills": {
        "strength": ["intimidate", "smash", "break", "force"],
        "dexterity": ["sneak", "pickpocket", "pick lock", "acrobatics", "dodge"],
        "intelligence": ["investigate", "recall history", "decipher", "examine"]
    }
}