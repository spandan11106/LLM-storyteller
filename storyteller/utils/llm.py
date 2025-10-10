# storyteller/utils/llm.py
"""
🤖 The AI Communication Hub - Where We Chat with Our Smart Storytelling Friend!

This is the bridge between our storytelling system and the incredibly smart AI
that generates all the amazing stories, characters, and plot twists. Think of
it as a translator that helps us have amazing conversations with our AI buddy!
"""

import json
import httpx
from typing import List, Dict, Any, Optional

from ..config import LLM_MODEL, GROQ_API_KEY

# Let's see if we have our AI communication tools ready!
try:
    from groq import Groq, DefaultHttpxClient
    HAS_GROQ = True
    print("🎉 AI communication tools are ready!")
except ImportError:
    HAS_GROQ = False
    print("📝 Note: Install groq package for AI storytelling features")


class LLMClient:
    """🌟 Your Personal AI Storytelling Assistant - Ready to Create Magic!"""
    
    def __init__(self):
        self.model = LLM_MODEL
        self.client = None
        
        if HAS_GROQ and GROQ_API_KEY:
            # Set up a reliable connection to our AI friend
            timeout = httpx.Timeout(30.0, connect=10.0)  # Give it time to think of great stories
            transport = httpx.HTTPTransport(retries=3)    # Try again if connection hiccups
            
            custom_httpx_client = DefaultHttpxClient(
                timeout=timeout,
                transport=transport,
            )
            
            # Connect to our amazing AI storyteller
            self.client = Groq(
                api_key=GROQ_API_KEY,
                http_client=custom_httpx_client,
            )
            print("🚀 Connected to AI storyteller - ready for epic adventures!")
        else:
            print("⚠️ AI storyteller needs a connection key - add your GROQ_API_KEY!")
    
    def generate_text(self, messages: List[Dict[str, str]], **kwargs) -> Optional[str]:
        """💬 Have an amazing conversation with our AI storytelling friend!"""
        if not self.client:
            return "🤖 AI storyteller is taking a nap - please check your connection and API key!"
        
        try:
            # Ask our AI friend to weave some storytelling magic!
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                **kwargs
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"🤖 AI storyteller encountered an issue: {e}"
    
    def generate_story_intro(self, character_info: str) -> str:
        """🌟 Create an amazing opening scene for your hero's first adventure!"""
        prompt = f"""You are the most amazing Dungeon Master ever, starting a brand new adventure! Create an engaging, exciting opening scene for this incredible hero:

{character_info}

Make it immersive, exciting, and full of possibilities! Give the player some really interesting choices to make.
Just tell the story - no technical stuff, just pure storytelling magic!"""
        
        messages = [{"role": "user", "content": prompt}]
        return self.generate_text(messages) or "🏰 Welcome to your amazing adventure! You find yourself at the entrance to a mysterious tavern, with sounds of laughter and adventure calling from within. The wooden sign creaks in the wind, and you can smell fresh bread and hear tales of distant lands. What would you like to do?"
    
    def continue_story(self, character_info: str, memory_context: str, recent_context: str, player_action: str) -> str:
        """📖 Continue the epic story based on what your hero chooses to do!"""
        prompt = f"""You are the best Dungeon Master in the world, continuing an amazing ongoing adventure! 

OUR HERO:
{character_info}

WHAT JUST HAPPENED:
{recent_context}

IMPORTANT THINGS TO REMEMBER:
{memory_context}

WHAT THE HERO DOES NOW: {player_action}

Continue this epic story! Remember everything that happened before, make it exciting and consistent, and give our hero some great choices for what to do next.

Just tell the amazing story - pure narrative magic, no technical stuff!"""
        
        messages = [{"role": "user", "content": prompt}]
        return self.generate_text(messages) or "🌟 The story continues as you take action, with the world responding to your choices in amazing ways..."


# 🌟 Our amazing AI storytelling friend - ready whenever you need epic stories!
llm_client = LLMClient()