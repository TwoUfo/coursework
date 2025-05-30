from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from domain.models.tag import Tag, TagRelationship


class TagServicePort(ABC):
    """Interface for tag service."""

    @abstractmethod
    def create_tag(self, name: str, description: Optional[str] = None) -> Tag:
        """Create a new tag."""
        pass

    @abstractmethod
    def create_tag_if_not_exists(self, name: str, description: Optional[str] = None) -> Tag:
        """Create a tag if it doesn't exist, otherwise return existing tag."""
        pass

    @abstractmethod
    def create_relationship(
        self, source_name: str, target_name: str, weight: float
    ) -> TagRelationship:
        """Create a relationship between two tags with a weight."""
        pass

    @abstractmethod
    def get_tag(self, name: str) -> Optional[Tag]:
        """Get tag by name."""
        pass

    @abstractmethod
    def get_all_tags(self) -> List[Tag]:
        """Get all available tags."""
        pass

    @abstractmethod
    def get_mood_graph(self) -> Dict[str, Dict[str, float]]:
        """Get the complete mood graph with computed weights using Floyd-Warshall."""
        pass
