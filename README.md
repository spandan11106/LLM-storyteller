# LLM Storyteller 🐉

A graphical, AI-powered Dungeon Master and interactive story engine. This application uses the Groq LLM API to generate dynamic, narrative-driven adventures. It features an advanced memory system to ensure story coherence and a dynamic social AI that allows NPCs to react to the player's behavior.

*(You can add a screenshot of your application here!)*

## Features

* **Graphical User Interface**: A clean, modern UI built with `customtkinter` that includes a chat window and a dynamic sidebar for character and NPC status.
* **Dynamic Storytelling**: Powered by the Groq LLM API (`llama-3.1-8b-instant`) to generate creative and responsive narratives.
* **Advanced Three-Tier Memory**:
    * **L1 (Turn Memory)**: Remembers the most recent turns for immediate context.
    * **L2 (Scene Memory)**: Intelligently detects scene changes and creates summaries for medium-term recall.
    * **L3 (Core Memory)**: Maintains a constantly updated summary of the entire story, ensuring the AI never forgets key events.
* **Dynamic Social AI**: NPCs have emotional states and relationship scores that change based on the player's tone. The system dynamically detects new NPCs introduced in the story and begins tracking them.
* **Simple Gameplay Mechanics**: A narrative-driven system for player state ('Healthy' or 'Wounded') and a linear plot-point quest system.

## Requirements

* Python 3.10+
* Dependencies listed in `requirements.txt`, including:
    * `groq`
    * `python-dotenv`
    * `customtkinter`
    * `networkx`
    * `sentence-transformers`

## Quickstart

1.  **Set up a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file** in the project's root directory and add your Groq API key:
    ```text
    GROQ_API_KEY=your_groq_api_key_here
    ```

4.  **Run the application**:
    ```bash
    python main.py
    ```

## How to Run Tests

The project includes a comprehensive test suite to validate all core features. To run all tests and generate a detailed report, use the `run_tests.py` script:

```bash
python run_tests.py
```

## Project Structure

* `main.py`: The main entry point to launch the graphical application.
* `frontend/`: Contains the customtkinter UI code.
* `storyteller/`: The core package containing all backend logic:
    * `engine.py`: The main game loop and logic.
    * `memory_manager.py`: Manages the overall memory state.
    * `rag_manager.py`: Handles the three-tier memory database and knowledge graph.
    * `npc_manager.py`: Contains the social AI logic for NPCs.
    * `config.py`: Stores all prompts, plot points, and configurations.
* `tests/`: Contains all the unit and integration tests.
* `run_tests.py`: A convenient script to run the entire test suite.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.