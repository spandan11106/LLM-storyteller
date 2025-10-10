# storyteller/core/memory.py
"""
Memory system for long-term conversation storage and retrieval
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

# Try to import optional dependencies with fallbacks
try:
    from sentence_transformers import SentenceTransformer
    HAS_EMBEDDINGS = True
except ImportError:
    HAS_EMBEDDINGS = False
    
try:
    import chromadb
    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False


@dataclass
class MemoryEntry:
    """Represents a single conversation turn in memory"""
    
    turn_id: int
    timestamp: str
    player_action: str
    dm_response: str
    extracted_facts: List[str]
    importance_score: float


class DocumentMemorySystem:
    """Document-based memory with token linking and retrieval"""
    
    def __init__(self, save_path: str = None):
        self.save_path = save_path or MEMORY_SAVE_PATH
        os.makedirs(self.save_path, exist_ok=True)
        
        # Initialize embedding model for semantic search (with fallback)
        if HAS_EMBEDDINGS:
            self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        else:
            self.embedder = None
        
        # Initialize vector database (with fallback)
        if HAS_CHROMADB:
            self.chroma_client = chromadb.Client()
            self.collection = self.chroma_client.get_or_create_collection(VECTOR_DB_COLLECTION)
        else:
            self.chroma_client = None
            self.collection = None
        
        # Memory storage
        self.conversation_history: List[MemoryEntry] = []
        self.fact_database: Dict[str, List[int]] = {}  # fact -> [turn_ids]
        self.turn_counter = 0
        
        self._load_existing_memory()
    
    def _load_existing_memory(self):
        """Load existing memory from disk"""
        memory_file = os.path.join(self.save_path, "memory.json")
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'r') as f:
                    data = json.load(f)
                    self.turn_counter = data.get('turn_counter', 0)
                    
                    # Rebuild conversation history
                    for entry_data in data.get('conversations', []):
                        entry = MemoryEntry(**entry_data)
                        self.conversation_history.append(entry)
                    
                    # Rebuild fact database
                    self.fact_database = data.get('facts', {})
            except Exception as e:
                print(f"Warning: Could not load existing memory: {e}")
    
    def save_memory(self):
        """Save memory to disk"""
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
        except Exception as e:
            print(f"Warning: Could not save memory: {e}")
    
    def extract_facts(self, text: str) -> List[str]:
        """Extract important facts/entities from text"""
        facts = []
        
        # Extract named entities (people, places, items)
        for pattern in ENTITY_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            facts.extend([match.strip() for match in matches if len(match.strip()) > 2])
        
        # Extract relationships and actions
        for pattern in RELATIONSHIP_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                facts.append(f"{match[0]} -> {match[1]}")
        
        return list(set(facts))  # Remove duplicates
    
    def calculate_importance(self, player_action: str, dm_response: str) -> float:
        """Calculate importance score for a conversation turn"""
        text = (player_action + " " + dm_response).lower()
        score = 0.0
        
        for keyword in IMPORTANCE_KEYWORDS:
            if keyword in text:
                score += 1.0
        
        return min(score, 5.0)  # Cap at 5.0
    
    def add_conversation_turn(self, player_action: str, dm_response: str):
        """Add a new conversation turn to memory"""
        self.turn_counter += 1
        
        # Extract facts from both player action and DM response
        facts = self.extract_facts(player_action + " " + dm_response)
        
        # Calculate importance
        importance = self.calculate_importance(player_action, dm_response)
        
        # Create memory entry
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