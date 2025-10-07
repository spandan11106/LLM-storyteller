import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("Attempting to connect to Groq API to fetch models...")

try:
    # Initialize the Groq client
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    # Fetch the list of available models
    models = client.models.list()

    print("\n\u2705 Success! Here are the models available to your API key:")
    print("---------------------------------------------------------")
    
    # Iterate through the models and print their IDs
    for model in models.data:
        print(model.id)
        
    print("---------------------------------------------------------")
    print("\nPlease copy one of these model IDs and paste it into your main.py file.")

except Exception as e:
    print(f"\n\u274c An error occurred: {e}")
    print("Please double-check that your GROQ_API_KEY in the .env file is correct.")
