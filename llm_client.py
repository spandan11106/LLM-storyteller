# llm_client.py
from groq import Groq
import config

# Initialize the Groq client with the API key from the config file
# This creates a single instance that can be imported and used by other files.
client = Groq(api_key=config.GROQ_API_KEY)