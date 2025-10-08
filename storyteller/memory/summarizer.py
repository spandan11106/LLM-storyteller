# storyteller/memory/summarizer.py

from ..llm_client import client
from .. import config
import json

def summarize_scene(turn_texts: list[str]) -> str:
    """
    Uses an LLM to create a concise summary of a scene from a list of turns.
    """
    if not turn_texts:
        return ""

    full_scene_text = "\n".join(turn_texts)
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": config.SCENE_SUMMARY_PROMPT},
                {"role": "user", "content": full_scene_text}
            ],
            model=config.LLM_MODEL,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return data.get("summary", "")
    except Exception as e:
        print(f"Error during scene summarization: {e}")
        # Fallback to a simple concatenation if LLM fails
        return " ".join(turn_texts)[:500]