# storyteller/npc_manager.py

import json
from .llm_client import client
from . import config

def analyze_player_tone(player_input: str) -> str:
    """
    Uses an LLM to analyze the tone of the player's input.
    Returns a string like 'Polite', 'Rude', 'Threatening', or 'Neutral'.
    """
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": config.TONE_ANALYSIS_PROMPT},
                {"role": "user", "content": player_input}
            ],
            model=config.LLM_MODEL,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return data.get("tone", "Neutral")
    except Exception:
        return "Neutral" # Default to neutral if analysis fails

def update_npc_state(graph, npc_name: str, tone: str):
    """
    Updates the NPC's relationship score and emotional state in the knowledge graph.
    """
    if not graph.has_node(npc_name):
        return # Don't act on NPCs not in the graph

    # Define how tone affects relationship score
    tone_effects = {
        "Polite": 5,
        "Neutral": 0,
        "Rude": -10,
        "Threatening": -20,
    }
    
    # Get current score or default to 0
    current_score = graph.nodes[npc_name].get('relationship_score', 0)
    new_score = current_score + tone_effects.get(tone, 0)
    
    # Determine new emotional state based on score
    if new_score > 50:
        emotion = "Friendly"
    elif new_score > 10:
        emotion = "Pleased"
    elif new_score < -50:
        emotion = "Hostile"
    elif new_score < -10:
        emotion = "Annoyed"
    else:
        emotion = "Neutral"

    # Update the graph with the new values
    graph.nodes[npc_name]['relationship_score'] = new_score
    graph.nodes[npc_name]['emotional_state'] = emotion
    
    print(f"[Social AI] {npc_name}'s state updated. Score: {new_score}, Emotion: {emotion}")

def get_npc_context(graph) -> str:
    """
    Generates a context string describing the emotional state of all NPCs.
    """
    npc_contexts = []
    for node, data in graph.nodes(data=True):
        if data.get('type') == 'npc':
            score = data.get('relationship_score', 0)
            emotion = data.get('emotional_state', 'Neutral')
            npc_contexts.append(f"- {node} (Relationship: {score}, Emotion: {emotion})")
    
    if not npc_contexts:
        return "No notable NPC relationships have been established."
    return "\n".join(npc_contexts)

# storyteller/npc_manager.py

# ... (add this new function at the end of the file) ...

def get_npc_context_dict(graph) -> dict:
    """
    Generates a dictionary of all NPCs and their emotional states.
    """
    npc_data = {}
    for node, data in graph.nodes(data=True):
        if data.get('type') == 'npc':
            npc_data[node] = {
                "score": data.get('relationship_score', 0),
                "emotion": data.get('emotional_state', 'Neutral')
            }
    return npc_data