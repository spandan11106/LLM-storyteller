# storyteller/core/memory.py
"""
🧠 The Amazing Memory Palace - Where Every Adventure Lives Forever!

This is the incredible memory system that makes our AI storyteller truly special.
Think of it as a magical library that never forgets a single detail from your
adventures, allowing for truly persistent and evolving stories!

Every conversation, every character interaction, every epic moment gets carefully
stored and can be recalled instantly. It's like having a perfect memory that 
grows more interesting with every adventure you embark upon!
"""

import json
import re
import os
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass

from ..config import (
    MEMORY_SAVE_PATH, MAX_CONVERSATION_HISTORY, MAX_RETRIEVAL_RESULTS,
    ENTITY_PATTERNS, RELATIONSHIP_PATTERNS, IMPORTANCE_KEYWORDS,
    EMBEDDING_MODEL, VECTOR_DB_COLLECTION
)

# Let's see what magical memory tools we have available!
try:
    from sentence_transformers import SentenceTransformer
    HAS_EMBEDDINGS = True
    print("🎉 Great! Smart memory search is ready to go!")
except ImportError:
    HAS_EMBEDDINGS = False
    print("📝 Note: Using basic memory (still awesome, just not as fancy!)")
    
try:
    import chromadb
    HAS_CHROMADB = True
    print("🗄️ Excellent! Advanced memory database is available!")
except ImportError:
    HAS_CHROMADB = False
    print("📚 Using simple file-based memory (perfectly fine for most adventures!)")


@dataclass
class MemoryEntry:
    """A precious memory from your adventure - every moment matters!"""
    
    turn_id: int            # Which turn of the conversation was this?
    timestamp: str          # When did this epic moment happen?
    player_action: str      # What did you do?
    dm_response: str        # How did the story unfold?
    extracted_facts: List[str]  # Important things we learned
    importance_score: float     # How epic was this moment?


class DocumentMemorySystem:
    """🏰 Your Personal Memory Palace - Where Stories Come to Life!"""
    
    def __init__(self, save_path: str = None):
        self.save_path = save_path or MEMORY_SAVE_PATH
        os.makedirs(self.save_path, exist_ok=True)  # Make sure our memory palace exists!
        
        # Let's set up our smart memory search tools (if available)
        if HAS_EMBEDDINGS:
            self.embedder = SentenceTransformer(EMBEDDING_MODEL)
            print("🔍 Smart memory search is ready - we can find anything!")
        else:
            self.embedder = None
            print("📝 Using keyword-based memory search (still works great!)")
        
        # Initialize our fancy memory database (if available)
        if HAS_CHROMADB:
            self.chroma_client = chromadb.Client()
            self.collection = self.chroma_client.get_or_create_collection(VECTOR_DB_COLLECTION)
            print("🗄️ Advanced memory database is ready!")
        else:
            self.chroma_client = None
            self.collection = None
            print("📚 Using simple file storage for memories")
        
        # Our memory containers - where all the magic happens!
        self.conversation_history: List[MemoryEntry] = []  # Every conversation we've had
        self.fact_database: Dict[str, List[int]] = {}      # Quick lookup: fact -> conversation turns
        self.turn_counter = 0                              # Keeping track of our adventure progress
        
        self._load_existing_memory()  # Bring back all our precious memories!
    
    def _load_existing_memory(self):
        """Wake up our memory palace and remember everything from before!"""
        memory_file = os.path.join(self.save_path, "memory.json")
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'r') as f:
                    data = json.load(f)
                    self.turn_counter = data.get('turn_counter', 0)
                    
                    # Bring back all our amazing conversations
                    for entry_data in data.get('conversations', []):
                        entry = MemoryEntry(**entry_data)
                        self.conversation_history.append(entry)
                    
                    # Rebuild our fact lookup system
                    self.fact_database = data.get('facts', {})
                    
                    print(f"🎉 Memory restored! Found {len(self.conversation_history)} conversations and {len(self.fact_database)} facts!")
            except Exception as e:
                print(f"⚠️ Couldn't load previous memories (starting fresh): {e}")
        else:
            print("🆕 Starting with a clean memory palace - let's create some epic memories!")
    
    def save_memory(self):
        """Carefully preserve all our precious memories for future adventures!"""
        data = {
            'turn_counter': self.turn_counter,
            'conversations': [
                {
                    'turn_id': entry.turn_id,
                    'timestamp': entry.timestamp,
                    'player_action': entry.player_action,
                    'dm_response': entry.dm_response,
                    'extracted_facts': entry.extracted_facts,
                    'importance_score': entry.importance_score
                }
                for entry in self.conversation_history
            ],
            'facts': self.fact_database
        }
        
        memory_file = os.path.join(self.save_path, "memory.json")
        try:
            with open(memory_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"💾 Memory saved! Protected {len(self.conversation_history)} conversations for posterity!")
        except Exception as e:
            print(f"⚠️ Couldn't save memories (but they're still in active memory): {e}")
    
    def extract_facts(self, text: str) -> List[str]:
        """🔍 Hunt for important details and cool stuff in the conversation!"""
        facts = []
        
        # Look for interesting names, places, and things
        for pattern in ENTITY_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            facts.extend([match.strip() for match in matches if len(match.strip()) > 2])
        
        # Spot relationships and actions between characters
        for pattern in RELATIONSHIP_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                facts.append(f"{match[0]} -> {match[1]}")  # Who did what to whom
        
        return list(set(facts))  # Keep each fact only once!
    
    def calculate_importance(self, player_action: str, dm_response: str) -> float:
        """🌟 Figure out how epic and important this moment was!"""
        text = (player_action + " " + dm_response).lower()
        score = 0.0
        
        # Check for epic keywords that make moments memorable
        for keyword in IMPORTANCE_KEYWORDS:
            if keyword in text:
                score += 1.0  # Each epic keyword makes it more important!
        
        return min(score, 5.0)  # Maximum epicness level is 5!
    
    def add_conversation_turn(self, player_action: str, dm_response: str):
        """📝 Add this awesome moment to our permanent memory collection!"""
        self.turn_counter += 1
        
        # Hunt for interesting facts in this conversation
        facts = self.extract_facts(player_action + " " + dm_response)
        
        # Rate how epic this moment was
        importance = self.calculate_importance(player_action, dm_response)
        
        # Create a beautiful memory entry
        entry = MemoryEntry(
            turn_id=self.turn_counter,
            timestamp=datetime.now().isoformat(),
            player_action=player_action,
            dm_response=dm_response,
            extracted_facts=facts,
            importance_score=importance
        )
        
        self.conversation_history.append(entry)
        
        # Update fact database
        for fact in facts:
            if fact not in self.fact_database:
                self.fact_database[fact] = []
            self.fact_database[fact].append(self.turn_counter)
        
        # Add to vector database for semantic search (if available)
        if self.collection and self.embedder:
            full_text = f"Turn {self.turn_counter}: {player_action} | {dm_response}"
            embedding = self.embedder.encode(full_text).tolist()
            
            self.collection.add(
                embeddings=[embedding],
                documents=[full_text],
                ids=[str(self.turn_counter)],
                metadatas=[{
                    'turn_id': self.turn_counter,
                    'importance': importance,
                    'facts': json.dumps(facts)
                }]
            )
        
        # Keep only last N conversations in memory (while keeping facts)
        if len(self.conversation_history) > MAX_CONVERSATION_HISTORY:
            self.conversation_history = self.conversation_history[-MAX_CONVERSATION_HISTORY:]
        
        self.save_memory()
    
    def retrieve_relevant_memories(self, query: str, max_results: int = None) -> List[str]:
        """Retrieve relevant memories based on query"""
        max_results = max_results or MAX_RETRIEVAL_RESULTS
        
        # If vector search is available, use it
        if self.collection and self.embedder and self.collection.count() > 0:
            # Get embedding for query
            query_embedding = self.embedder.encode(query).tolist()
            
            # Search vector database
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(max_results, self.collection.count())
            )
            
            relevant_memories = []
            if results['documents']:
                for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                    turn_id = metadata['turn_id']
                    importance = metadata['importance']
                    relevant_memories.append(f"[Turn {turn_id}, Importance: {importance:.1f}] {doc}")
            
            return relevant_memories
        
        # Fallback: keyword-based search
        relevant_memories = []
        query_words = set(query.lower().split())
        
        for entry in self.conversation_history[-20:]:  # Search last 20 turns
            text = (entry.player_action + " " + entry.dm_response).lower()
            # Simple keyword matching
            matches = len(query_words.intersection(set(text.split())))
            if matches > 0:
                relevance = matches / len(query_words)
                relevant_memories.append(f"[Turn {entry.turn_id}, Relevance: {relevance:.1f}] {entry.player_action} | {entry.dm_response}")
        
        return sorted(relevant_memories, key=lambda x: float(x.split('Relevance: ')[1].split(']')[0]), reverse=True)[:max_results]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of current memory state"""
        return {
            'total_conversations': len(self.conversation_history),
            'total_facts': len(self.fact_database),
            'recent_facts': list(self.fact_database.keys())[-10:] if self.fact_database else [],
            'turn_counter': self.turn_counter
        }