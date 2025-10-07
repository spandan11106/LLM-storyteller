# config.py
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# --- API and Model Configuration ---

# Load the Groq API key from the environment
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# IMPORTANT: Set the model ID you confirmed is working for you
LLM_MODEL = "openai/gpt-oss-20b" 

# --- Memory Configuration ---

# Defines the number of recent turns to keep in short-term memory
# (5 user turns + 5 assistant turns = 10 messages)
WORKING_MEMORY_SIZE = 10

# The embedding model for vectorizing text
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# The name for our vector database collection
DB_COLLECTION_NAME = "episodic_memory"

# In config.py, add this at the end

# --- Quest Configuration ---
INITIAL_QUEST_ID = "The Lord's Summons"