# storyteller/engine.py

import json
import random
import re
from threading import Thread

from .llm_client import client
from . import config
from . import npc_manager
from .utils import sanitize_data_for_graph

def game_logic_thread(user_input, ui_queue, memory_manager):
    """The game logic loop, now without inventory management."""
    try:
        player_node = memory_manager.rag.graph.nodes.get("Player", {})
        player_state = player_node.get("state", "Healthy")
        
        npc_context = npc_manager.get_npc_context(memory_manager.rag.graph)
        retrieved_context = memory_manager.retrieve_context(user_input)
        memory_context = "\n".join(retrieved_context)
        active_plot_point = memory_manager.get_active_plot_point()

        # --- UPDATED: Removed Inventory from the prompt context ---
        prompt_context = (
            f"--- Player Status ---\nState: {player_state}\n\n"
            f"--- Active Plot Point ---\n{active_plot_point}\n\n"
            f"--- NPC Relationships & Emotions ---\n{npc_context}\n\n"
            f"--- Relevant Memories ---\n{memory_context}\n\n"
            f"--- Player Action ---\n{user_input}"
        )

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": config.MASTER_SYSTEM_PROMPT},
                {"role": "user", "content": prompt_context}
            ],
            model=config.LLM_MODEL,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        sanitized_data = sanitize_data_for_graph(data)

        narrative = sanitized_data.get("narrative", "The DM seems lost in thought...")
        ui_queue.put(("dm_response", narrative))

        player_updates = sanitized_data.get("player_updates", {})
        plot_completed = sanitized_data.get("plot_completed", False)

        Thread(
            target=background_processing_thread,
            args=(memory_manager, user_input, narrative, player_updates, plot_completed, active_plot_point, ui_queue),
            daemon=True
        ).start()
        
    except Exception as e:
        ui_queue.put(("dm_response", f"An error occurred: {e}"))


def background_processing_thread(memory_manager, user_input, narrative, player_updates, plot_completed, active_plot_point, ui_queue):
    """Background thread for social, memory, and player state updates."""
    try:
        player_node = memory_manager.rag.graph.nodes.get("Player", {})
        if player_updates:
            # --- UPDATED: Only process 'state' updates ---
            if "state" in player_updates:
                player_node["state"] = player_updates["state"]
            
            ui_queue.put(("update_char_info", player_node))

        # (Social AI and Memory processing logic remains the same)
        tone = npc_manager.analyze_player_tone(user_input)
        all_npcs_in_graph = [node for node, data in memory_manager.rag.graph.nodes(data=True) if data.get('type') == 'npc']
        mentioned_npcs = [npc for npc in all_npcs_in_graph if re.search(r'\b' + npc + r'\b', user_input, re.IGNORECASE)]
        
        if mentioned_npcs:
            target_npc = mentioned_npcs[0]
            npc_manager.update_npc_state(memory_manager.rag.graph, target_npc, tone)

        turn_text = f"Player: {user_input}\nDM: {narrative}"
        memory_manager.add_turn_to_log(turn_text)
        
        if plot_completed and active_plot_point:
            memory_manager.update_plot_point(active_plot_point)

        npc_data = npc_manager.get_npc_context_dict(memory_manager.rag.graph)
        ui_queue.put(("update_npc_info", npc_data))
        
    except Exception as e:
        print(f"Error in background processing: {e}")

# (determine_skill function remains unchanged)
def determine_skill(user_input):
    action_phrases = ["i try to", "i attempt to", "i want to"]
    if any(user_input.lower().startswith(phrase) for phrase in action_phrases):
        for skill, keywords in config.DND_RULES['skills'].items():
            if any(keyword in user_input.lower() for keyword in keywords):
                return skill
    return None