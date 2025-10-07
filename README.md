<<<<<<< HEAD
# LLM-storyteller
=======
# LLM-storyteller

A lightweight AI-powered Dungeon Master / story engine that uses the Groq LLM API to generate narrative responses, and a small memory system (episodic memories + a simple knowledge graph) powered by Chroma and SentenceTransformers.

This repository provides a minimal interactive loop (`main.py`) where a player types actions, the LLM responds as a Dungeon Master, and memories & facts are stored and retrieved to keep the world state consistent.

## Features
- Interactive CLI story loop (see `main.py`).
- Episodic memory: summarizes turns and stores vector embeddings in a Chroma collection (`memory_manager.py`).
- Knowledge graph: extracts structured facts from turns and keeps a small in-memory graph for factual consistency.
- Uses Groq LLM client via `llm_client.py`; model configured in `config.py`.

## Requirements
- Python 3.10+ (tested with 3.12 in this workspace)
- See `requirements.txt` for Python packages. Key dependencies:
	- groq
	- python-dotenv
	- chromadb
	- sentence-transformers

## Quickstart
1. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Groq API key:

```text
GROQ_API_KEY=your_groq_api_key_here
```

4. (Optional) Confirm a working model ID with `check_models.py`:

# LLM-storyteller

A lightweight AI-powered Dungeon Master / story engine that uses the Groq LLM API to generate narrative responses, and a small memory system (episodic memories + a simple knowledge graph) powered by Chroma and SentenceTransformers.

This repository provides a minimal interactive loop (`main.py`) where a player types actions, the LLM responds as a Dungeon Master, and memories & facts are stored and retrieved to keep the world state consistent.

## Features
- Interactive CLI story loop (see `main.py`).
- Episodic memory: summarizes turns and stores vector embeddings in a Chroma collection (`memory_manager.py`).
- Knowledge graph: extracts structured facts from turns and keeps a small in-memory graph for factual consistency.
- Uses Groq LLM client via `llm_client.py`; model configured in `config.py`.

## Requirements
- Python 3.10+ (tested with 3.12 in this workspace)
- See `requirements.txt` for Python packages. Key dependencies:
  - groq
  - python-dotenv
  - chromadb
  - sentence-transformers

## Quickstart
1. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Groq API key:

```text
GROQ_API_KEY=your_groq_api_key_here
```

4. (Optional) Confirm a working model ID with `check_models.py`:

# LLM-storyteller

A lightweight AI-powered Dungeon Master / story engine that uses the Groq LLM API to generate narrative responses, and a small memory system (episodic memories + a simple knowledge graph) powered by Chroma and SentenceTransformers.

This repository provides a minimal interactive loop (`main.py`) where a player types actions, the LLM responds as a Dungeon Master, and memories & facts are stored and retrieved to keep the world state consistent.

## Features
- Interactive CLI story loop (see `main.py`).
- Episodic memory: summarizes turns and stores vector embeddings in a Chroma collection (`memory_manager.py`).
- Knowledge graph: extracts structured facts from turns and keeps a small in-memory graph for factual consistency.
- Uses Groq LLM client via `llm_client.py`; model configured in `config.py`.

## Requirements
- Python 3.10+ (tested with 3.12 in this workspace)
- See `requirements.txt` for Python packages. Key dependencies:
  - groq
  - python-dotenv
  - chromadb
  - sentence-transformers

## Quickstart
1. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Groq API key:

```text
GROQ_API_KEY=your_groq_api_key_here
```

4. (Optional) Confirm a working model ID with `scripts/check_models.py`:

```bash
python scripts/check_models.py
```

5. Adjust `storyteller/config.py` if you want to change the model (`LLM_MODEL`), the embedding model, or memory settings.

6. Run the interactive DM loop:

```bash
python main.py
```

Controls:
- Type normal text to take actions in the story.
- Type `/questlog` to print the active quests stored in the knowledge graph.
- Type `quit` to exit.

## Important configuration
- `GROQ_API_KEY` (from your `.env`) — required.
- `storyteller.config.LLM_MODEL` — model id used for chat calls. The default in `storyteller/config.py` is a placeholder; use `scripts/check_models.py` to list available models for your key.
- `storyteller.config.EMBEDDING_MODEL` — SentenceTransformers model used for embeddings (default: `all-MiniLM-L6-v2`).

## Project layout
- `storyteller/` - package containing core modules (`config.py`, `llm_client.py`, `memory_manager.py`).
- `main.py` - interactive CLI using `storyteller` package.
- `scripts/` - helpful scripts such as `check_models.py`.
- `requirements.txt` - Python dependencies.
- `run.py` - optional entrypoint that calls `main.py`.

## Notes & troubleshooting
- If model calls fail, verify `GROQ_API_KEY` and that `storyteller.config.LLM_MODEL` is set to a valid model id for that key.
- The first time the sentence-transformers model downloads it may take some time and network bandwidth.
- Chroma creates local storage for vectors by default; ensure you have write permission in the project directory.

## Contributing
Feel free to open issues or PRs. Small improvements that help reproducibility are welcome (tests, type hints, CI).

## License
This project is licensed under the MIT License — see `LICENSE`.
