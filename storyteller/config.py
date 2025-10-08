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

# --- Plot Point Configuration ---
PLOT_POINTS = [
    "MEET_MYSTERIOUS_STRANGER",
    "GET_THE_QUEST",
    "FIND_THE_HIDDEN_CAVE",
    "CONFRONT_THE_GOBLIN_LEADER"
]

# --- D&D System Prompt & Rules ---
GAME_SYSTEM_PROMPT = (
    "You are a skilled D&D Dungeon Master. Your primary goal is to guide the player through the story. "
    "1. **Follow the Active Plot Point:** You will be given an 'Active Plot Point'. Your main job is to create a response that moves the story toward completing this goal. If the player does something unexpected, connect it back to the plot. "
    "2. **Be Concise & Interactive:** Keep descriptions to 2-5 sentences and ALWAYS end by asking 'What do you do?' often with 2-3 numbered choices. "
    "3. **Adhere to Facts:** You MUST treat all provided facts about the world and player as absolute truth."
)

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