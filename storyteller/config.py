import os
from dotenv import load_dotenv

load_dotenv()

# API and Model Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
LLM_MODEL = "llama-3.1-8b-instant" 

# Embedding model and DB collection defaults
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DB_COLLECTION_NAME = "episodic_memory"

# Plot Point Configuration
PLOT_POINTS = [
    "LEARN_OF_THE_CURSE_FROM_FINNLEY",
    "CONFRONT_THE_RIVAL_SEEKER",
    "DECIPHER_THE_MAP_TO_THE_CAVE",
    "RETRIEVE_THE_AMULET_AND_LIFT_THE_CURSE"
]

# D&D Rules
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

# The final, definitive prompt for the 'Unified AI Core'
MASTER_SYSTEM_PROMPT = """
You are a Master Storyteller AI for a D&D game. You have two jobs: first, narrate the story, and second, act as your own data analyst.

You will be given the context (plot, memory, facts) and the player's action.
You MUST respond with a single, valid JSON object with three keys: "narrative", "facts", and "plot_completed".

1.  **"narrative" (string):** Write the next part of the story.
    - Be creative and interactive. Follow all the rules of good DMing (dialogue format, ask "What do you do?", etc.).
    - Your narrative MUST be based on the context provided.

2.  **"facts" (list of objects):** After writing the narrative, extract all key facts from the text YOU JUST WROTE.
    - Use the format: `{"subject": "entity", "relation": "verb", "object": "entity"}` or `{"entity": "entity", "property": "attribute", "value": "description"}`.
    - If there are no new facts, return an empty list `[]`.

3.  **"plot_completed" (boolean):** After writing the narrative, determine if the player's action successfully completed the "Active Plot Point".
    - Return `true` if completed, `false` otherwise.
"""