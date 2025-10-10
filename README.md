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

## Testing

The project includes a comprehensive test suite that validates:
- 🧠 **Memory System**: Including "needle in haystack" long-term memory tests
- 😊 **NPC Emotions**: Relationship tracking and emotion consistency
- 📖 **Story Consistency**: Character traits and narrative continuity  
- ⚡ **Performance**: Response times and scalability

### Run All Tests
```bash
source venv/bin/activate
python run_tests.py all
```

### Run Specific Test Suites
```bash
python run_tests.py memory      # Memory tests only
python run_tests.py npc         # NPC emotion tests
python run_tests.py story       # Story consistency tests
python run_tests.py performance # Performance tests
```

See `tests/README.md` for detailed testing documentation.

## Project Structure

* `main.py`: The main entry point to launch the graphical application.
* `storyteller/`: The core package containing all backend logic:
    * `core/`: Core engine components
        * `engine.py`: Main storytelling orchestration
        * `character.py`: Character data management
        * `memory.py`: Long-term memory system with fact extraction
        * `npc.py`: NPC emotion tracking and relationships
    * `ui/`: User interface components
        * `gui.py`: CustomTkinter-based GUI with sidebar design
    * `utils/`: Utility modules
        * `llm.py`: Groq LLM client wrapper
    * `config.py`: Configuration and settings
* `tests/`: Comprehensive test suite
    * `test_memory.py`: Memory system tests including needle-in-haystack
    * `test_npc_emotions.py`: NPC emotion and relationship tests
    * `test_story_consistency.py`: Narrative coherence tests
    * `test_performance.py`: Performance and scalability tests
    * `run_all_tests.py`: Main test orchestrator
* `run_tests.py`: Convenient test runner script

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.