"""Run entrypoint for the storyteller app."""
from storyteller import MemoryManager, client, config
from storyteller.memory_manager import MemoryManager

def main():
    # Keep the previous behavior: import the package and run the main loop from top-level main.py
    import main as app_main
    app_main.main()

if __name__ == "__main__":
    main()
