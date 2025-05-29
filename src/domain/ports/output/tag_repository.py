from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.tag import Tag, TagRelationship


class TagRepositoryPort(ABC):
    """Interface for tag repository."""

    @abstractmethod
    def save(self, tag: Tag) -> Tag:
        """Save a tag to the database."""
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Tag]:
        """Get a tag by name."""
        pass

    @abstractmethod
    def get_all(self) -> List[Tag]:
        """Get all tags."""
        pass

    @abstractmethod
    def save_relationship(self, relationship: TagRelationship) -> TagRelationship:
        """Save a tag relationship to the database."""
        pass

    @abstractmethod
    def get_all_relationships(self) -> List[TagRelationship]:
        """Get all tag relationships."""
        pass
