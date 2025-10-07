# main.py
import json
from storyteller import client, MemoryManager, config

def main():
    """Main function to run the AI Dungeon Master."""
    memory = MemoryManager()
    
    # Add the initial quest to the knowledge graph at the start of the game
    memory.knowledge_graph["Quests"] = {config.INITIAL_QUEST_ID: "active"}

    print("\n✨ AI Dungeon Master v3 (with Quest Log) Initialized ✨")
    print("You find yourself in a dimly lit tavern. What do you do? (Type 'quit' to exit or '/questlog' to see quests)")

    system_prompt = {
        "role": "system",
        "content": (
            "You are a Dungeon Master. Your primary goal is to maintain a consistent and logical world state. "
            "You have been provided with KNOWN WORLD FACTS. You MUST treat these facts as the absolute source of truth. "
            "If a player's action contradicts a known fact, your response must reflect this contradiction. "
            "Narrate the story, but ensure all descriptions and character dialogues strictly adhere to the provided facts."
        )
    }
    
    conversation_history = [system_prompt]

    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == 'quit':
                print("Ending adventure. Goodbye!")
                break

            # Handle the /questlog command
            if user_input.lower() == '/questlog':
                print("\n--- QUEST LOG ---")
                active_quests = memory.knowledge_graph.get("Quests", {})
                if not active_quests:
                    print("No active quests.")
                for quest, status in active_quests.items():
                    print(f"- {quest} [{status.upper()}]")
                print("-----------------\n")
                continue # Skip the rest of the loop and ask for new input

            # 1. Retrieve Episodic Memories (narrative context)
            relevant_memories = memory.retrieve_memories(user_input)
            memory_context = "\n".join(relevant_memories)
            
            # 2. Retrieve Factual Memories (knowledge graph)
            known_facts = []
            # Find entities from our graph that are mentioned in the user's input
            for entity in memory.knowledge_graph.keys():
                if entity.lower() in user_input.lower():
                    facts = memory.get_facts_about(entity)
                    if facts:
                        known_facts.append(f"Facts about {entity}: {json.dumps(facts)}")
            
            fact_context = "\n".join(known_facts)

            # 3. Construct the prompt
            prompt_context = f"Relevant Narrative Memories:\n{memory_context}\n\nKnown World Facts:\n{fact_context}\n\nContinue the story."
            
            # 4. Trim working memory
            if len(conversation_history) > config.WORKING_MEMORY_SIZE + 1:
                del conversation_history[1:3]

            # 5. Prepare messages for API
            messages_for_api = [
                system_prompt,
                {"role": "system", "content": prompt_context},
                *conversation_history[1:],
                {"role": "user", "content": user_input}
            ]

            # 6. Call LLM
            chat_completion = client.chat.completions.create(
                messages=messages_for_api,
                model=config.LLM_MODEL,
            )
            ai_response = chat_completion.choices[0].message.content
            # Sanitize response to avoid surrogate encoding errors when printing
            try:
                safe_ai = ai_response.encode('utf-8', errors='replace').decode('utf-8')
            except Exception:
                safe_ai = ai_response
            print(f"\nDM: {safe_ai}")

            # 7. Update history and save all memory types
            turn_text = f"Player: {user_input}\nDM: {safe_ai}"
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": safe_ai})
            memory.save_memory(turn_text, user_input)

        except Exception as e:
            import traceback
            print("An error occurred:")
            traceback.print_exc()
            break

if __name__ == "__main__":
    main()