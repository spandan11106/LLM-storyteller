# storyteller/core/character.py
"""
Character creation and management system
"""

from dataclasses import dataclass
from typing import Dict, Any
from ..config import DEFAULT_ATTRIBUTES


@dataclass
class Character:
    """Represents a player character with background and attributes"""
    
    name: str
    background: str
    personality: str
    goals: str
    attributes: Dict[str, Any]
    
    def __post_init__(self):
        """Ensure character has all required attributes"""
        # Fill in missing attributes with defaults
        for attr, default_value in DEFAULT_ATTRIBUTES.items():
            if attr not in self.attributes:
                self.attributes[attr] = default_value
    
    def get_attribute(self, attribute: str) -> int:
        """Get character attribute value"""
        return self.attributes.get(attribute, 0)
    
    def set_attribute(self, attribute: str, value: int):
        """Attributes are locked after creation (no-op)"""
        pass
    
    def get_description(self) -> str:
        """Get a formatted description of the character"""
        return f"""Character: {self.name}
Background: {self.background}
Personality: {self.personality}
Goals: {self.goals}
Attributes: {self.attributes}"""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert character to dictionary for serialization"""
        return {
            'name': self.name,
            'background': self.background,
            'personality': self.personality,
            'goals': self.goals,
            'attributes': self.attributes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Character':
        """Create character from dictionary"""
        return cls(
            name=data['name'],
            background=data['background'],
            personality=data['personality'],
            goals=data['goals'],
            attributes=data['attributes']
        )