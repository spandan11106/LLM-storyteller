# storyteller/memory/core_memory.py

from ..llm_client import client
from .. import config
import json

def update_core_memory(current_core_memory: str, new_scene_summary: str) -> str:
    """
    Updates the core memory by integrating the summary of the latest scene.
    """
    if not new_scene_summary:
        return current_core_memory

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": config.CORE_MEMORY_UPDATE_PROMPT},
                {"role": "user", "content": f"Current Core Memory:\n{current_core_memory}\n\nLatest Scene Summary:\n{new_scene_summary}"}
            ],
            model=config.LLM_MODEL,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return data.get("updated_core_memory", current_core_memory)
    except Exception as e:
        print(f"Error updating core memory: {e}")
        # Fallback: simple append
        return f"{current_core_memory}\n- {new_scene_summary}"