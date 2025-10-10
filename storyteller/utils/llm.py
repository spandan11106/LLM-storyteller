# storyteller/utils/llm.py
"""
LLM client wrapper for API calls
"""

import json
import httpx
from typing import List, Dict, Any, Optional

from ..config import LLM_MODEL, GROQ_API_KEY

# Try to import groq
try:
    from groq import Groq, DefaultHttpxClient
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False


class LLMClient:
    """Wrapper for LLM API calls with error handling"""
    
    def __init__(self):
        self.model = LLM_MODEL
        self.client = None
        
        if HAS_GROQ and GROQ_API_KEY:
            # Create a custom httpx client with sensible timeouts and retries
            timeout = httpx.Timeout(30.0, connect=10.0)
            transport = httpx.HTTPTransport(retries=3)
            
            custom_httpx_client = DefaultHttpxClient(
                timeout=timeout,
                transport=transport,
            )
            
            # Initialize the Groq client
            self.client = Groq(
                api_key=GROQ_API_KEY,
                http_client=custom_httpx_client,
            )
            print("Initialized LLM client successfully")
        else:
            print("Warning: Groq client not available (missing groq package or API key)")
    
    def generate_text(self, messages: List[Dict[str, str]], **kwargs) -> Optional[str]:
        """Generate text using the LLM"""
        if not self.client:
            return "LLM client not available - please check your Groq API key and dependencies"
        
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                **kwargs
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating text: {e}"
    
    def generate_story_intro(self, character_info: str) -> str:
        """Generate an opening story based on character"""
        prompt = f"""You are a Dungeon Master starting a new adventure. Create an engaging opening scene for:

{character_info}

Provide a rich, immersive opening that sets up the adventure and gives the player meaningful choices.
Respond with only the narrative text - no JSON, just the story."""
        
        messages = [{"role": "user", "content": prompt}]
        return self.generate_text(messages) or "Welcome to your adventure! You find yourself at the entrance to a mysterious tavern, with sounds of laughter and adventure calling from within."
    
    def continue_story(self, character_info: str, memory_context: str, recent_context: str, player_action: str) -> str:
        """Continue the story based on player action and context"""
        prompt = f"""You are an expert Dungeon Master continuing an ongoing adventure. 

CHARACTER:
{character_info}

RECENT CONVERSATION:
{recent_context}

RELEVANT PAST EVENTS:
{memory_context}

CURRENT PLAYER ACTION: {player_action}

Continue the story based on the player's action. Consider their character, the recent context, and relevant past events. Make the story engaging, consistent, and give the player meaningful choices.

Respond with only the narrative text - no JSON, just the story continuation."""
        
        messages = [{"role": "user", "content": prompt}]
        return self.generate_text(messages) or "The story continues as you take action, the world responding to your choices..."


# Global client instance
llm_client = LLMClient()