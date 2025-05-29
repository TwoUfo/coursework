from typing import List, Dict, Optional

from domain.models.tag import Tag, TagRelationship
from domain.ports.input.tag_service import TagServicePort
from domain.ports.output.tag_repository import TagRepositoryPort
from domain.services.mood_graph import MoodGraph


class TagService(TagServicePort):
    """Implementation of tag service."""

    def __init__(self, tag_repository: TagRepositoryPort):
        self.tag_repository = tag_repository
        self._mood_graph = None

    def create_tag(self, name: str, description: Optional[str] = None) -> Tag:
        """Create a new tag."""
        tag = Tag(name=name, description=description)
        return self.tag_repository.save(tag)

    def create_relationship(
        self, source_name: str, target_name: str, weight: float
    ) -> TagRelationship:
        """Create a relationship between two tags with a weight."""
        if weight < 0 or weight > 1:
            raise ValueError("Weight must be between 0 and 1")

        source_tag = self.tag_repository.get_by_name(source_name)
        target_tag = self.tag_repository.get_by_name(target_name)

        if not source_tag or not target_tag:
            raise ValueError("Both source and target tags must exist")

        relationship = TagRelationship(
            id=None,
            source_tag_name=source_name,
            target_tag_name=target_name,
            weight=weight,
        )
        saved_rel = self.tag_repository.save_relationship(relationship)

        self._mood_graph = None

        return saved_rel

    def get_tag(self, name: str) -> Optional[Tag]:
        """Get tag by name."""
        return self.tag_repository.get_by_name(name)

    def get_all_tags(self) -> List[Tag]:
        """Get all available tags."""
        return self.tag_repository.get_all()

    def get_mood_graph(self) -> Dict[str, Dict[str, float]]:
        """Get the complete mood graph with computed weights using Floyd-Warshall."""
        if self._mood_graph is None:
            relationships = self.tag_repository.get_all_relationships()
            self._mood_graph = MoodGraph(relationships)

        return self._mood_graph.get_all_relationships()
