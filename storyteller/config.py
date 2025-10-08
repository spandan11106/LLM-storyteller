import os
from dotenv import load_dotenv

load_dotenv()

# API and Model Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
LLM_MODEL = "llama-3.1-8b-instant" 

# Embedding model and DB collection defaults
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DB_COLLECTION_NAME = "episodic_memory"
SCENE_COLLECTION_NAME = "scene_memory"

# --- UPDATED: A simple, linear quest chain ---
PLOT_POINTS = [
    "Investigate Boric's stolen hammer",
    "Track the goblins in the Whispering Woods",
    "Defeat the Goblin Leader",
    "Return the hammer to Boric"
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

# Initial NPC states
INITIAL_NPC_STATES = {
    "Boric": {
        "type": "npc",
        "occupation": "blacksmith",
        "relationship_score": 0,
        "emotional_state": "Neutral"
    },
    "Elara": {
        "type": "npc",
        "occupation": "mysterious old woman",
        "relationship_score": 0,
        "emotional_state": "Neutral"
    }
}

# --- Prompts ---

TONE_ANALYSIS_PROMPT = """
You are a social intelligence AI. Analyze the user's input and classify its tone.
The tone can be: Polite, Rude, Threatening, or Neutral.
Respond with a single, valid JSON object with a single key "tone".
"""

FACT_EXTRACTION_PROMPT = """
You are a data analyst AI. Your job is to extract key facts from a narrative text.
Analyze the text and identify all entities, their type, and their relationships or properties.
The entity_type MUST be one of: 'person', 'item', 'location', or 'other'.
Return a single, valid JSON object with a single key "facts".
"""

SCENE_SUMMARY_PROMPT = """
You are a story archivist. Your job is to read a transcript of a scene from a story and write a very concise summary.
Focus on the key outcomes, decisions, and discoveries.
Respond with a single, valid JSON object with a single key "summary".
"""

SCENE_DETECTOR_PROMPT = """
You are an AI story editor. Your job is to determine if a new turn in a story marks the end of the current scene.
Respond with a single, valid JSON object with a single boolean key "is_scene_break".
"""

CORE_MEMORY_UPDATE_PROMPT = """
You are an AI historian. You will be given a "Current Core Memory" and a "Latest Scene Summary".
Your job is to seamlessly integrate the new summary into the core memory.
Respond with a single, valid JSON object with a single key "updated_core_memory".
"""

MASTER_SYSTEM_PROMPT = """
You are a Master Storyteller AI for a D&D game. Your task is to respond to the player's action with a narrative and structured data.
You MUST respond with a single, valid JSON object and nothing else.

You will be given the Player's current state ('Healthy' or 'Wounded').
- If the Player is 'Wounded', describe their actions as being more difficult or painful.
- Your response can change the player's state.

Strictly follow this structure:
{
  "narrative": "Your creative story narration. If the player is wounded, reflect this in the text.",
  "player_updates": {
    "state": "Healthy"
  },
  "plot_completed": false
}

- "narrative": The story content.
- "player_updates": An object to update the player's status. Include only the 'state' key if it needs to change. If nothing changes, return an empty object {}.
- "plot_completed": A boolean (true or false).
"""