"""storyteller package

Exports core objects for easy imports from the package root.
"""
from .llm_client import client
from .memory_manager import MemoryManager
from . import config

__all__ = ["client", "MemoryManager", "config"]
