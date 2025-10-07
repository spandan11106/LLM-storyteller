import json
import random

# Import from your storyteller package
from storyteller.llm_client import client
from storyteller.memory_manager import MemoryManager
from storyteller import config

def main():
    """Main function to run the command-line AI Dungeon Master."""
    memory = MemoryManager()
    
    memory.knowledge_graph["Quests"] = {config.INITIAL_QUEST_ID: "active"}

    print("\n✨ AI Dungeon Master v4 (Interactive) Initialized ✨")
    print("You find yourself in a dimly lit tavern. What do you do?")
    
    # Use the same interactive system prompt as the GUI version
    system_prompt = {"role": "system", "content": config.GAME_SYSTEM_PROMPT}
    
    conversation_history = [system_prompt]
    turn_counter = 0

    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == 'quit':
                print("Ending adventure. Goodbye!")
                break

            if user_input.lower() == '/questlog':
                print("\n--- QUEST LOG ---")
                active_quests = memory.knowledge_graph.get("Quests", {})
                if not active_quests:
                    print("No active quests.")
                for quest, status in active_quests.items():
                    print(f"- {quest} [{status.upper()}]")
                print("-----------------\n")
                continue

            if "try to" in user_input.lower() or "attempt to" in user_input.lower():
                roll = random.randint(1, 20)
                print(f"🎲 You attempt the action and roll a {roll}!")
                user_input += f" (Dice roll result: {roll})"
            
            relevant_memories = memory.retrieve_memories(user_input)
            memory_context = "\n".join(relevant_memories)
            
            known_facts = []
            for entity in memory.knowledge_graph.keys():
                if entity.lower() in user_input.lower():
                    facts = memory.get_facts_about(entity)
                    if facts:
                        known_facts.append(f"Facts about {entity}: {json.dumps(facts)}")
            fact_context = "\n".join(known_facts)

            prompt_context = f"Relevant Narrative Memories:\n{memory_context}\n\nKnown World Facts:\n{fact_context}\n\nContinue the story."
            
            if len(conversation_history) > config.WORKING_MEMORY_SIZE + 1:
                del conversation_history[1:3]

            messages_for_api = [
                system_prompt,
                {"role": "system", "content": prompt_context},
                *conversation_history[1:],
                {"role": "user", "content": user_input}
            ]

            chat_completion = client.chat.completions.create(
                messages=messages_for_api,
                model=config.LLM_MODEL,
            )
            ai_response = chat_completion.choices[0].message.content
            print(f"\nDM: {ai_response}")

            turn_text = f"Player: {user_input}\nDM: {ai_response}"
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": ai_response})
            memory.save_memory(turn_text, user_input)

            turn_counter += 1
            if turn_counter >= 3:
                print("\n[EVENT] The tavern door creaks open as a hooded stranger steps in, silencing the room for a moment before conversations resume.")
                turn_counter = 0

        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()