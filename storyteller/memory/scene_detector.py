# storyteller/memory/scene_detector.py

from ..llm_client import client
from .. import config
import json

def is_scene_break(turn_text: str, current_scene_turns: list[str]) -> bool:
    """
    Uses an LLM to intelligently determine if a scene has ended.
    """
    if len(current_scene_turns) < 2: # A scene needs at least some context
        return False

    context = "\n".join(current_scene_turns)
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": config.SCENE_DETECTOR_PROMPT},
                {"role": "user", "content": f"Scene Context:\n{context}\n\nLatest Turn:\n{turn_text}"}
            ],
            model=config.LLM_MODEL,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return data.get("is_scene_break", False)
    except Exception as e:
        print(f"Error in scene detection: {e}")
        # Fallback to the old keyword logic if the LLM fails
        return any(keyword in turn_text.lower() for keyword in ["leave", "go to", "travel to"])