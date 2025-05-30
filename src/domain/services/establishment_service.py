from typing import List, Dict, Optional

from domain.models.establishment import Establishment, EstablishmentTag
from domain.models.comment import Comment
from domain.ports.input.establishment_service import EstablishmentServicePort
from domain.ports.output.establishment_repository import EstablishmentRepositoryPort
from domain.ports.output.comment_repository import CommentRepositoryPort
from domain.ports.input.tag_service import TagServicePort
from domain.services.tag_service import TagService


class EstablishmentService(EstablishmentServicePort):
    """Service for managing establishments."""

    def __init__(
        self,
        establishment_repository: EstablishmentRepositoryPort,
        comment_repository: CommentRepositoryPort,
        tag_service: TagService,
    ):
        self.establishment_repository = establishment_repository
        self.comment_repository = comment_repository
        self.tag_service = tag_service

    def create_establishment(self, data: Dict) -> Establishment:
        """Create a new establishment."""
        establishment = Establishment(
            id=None, name=data["name"], description=data.get("description", ""), tags=[]
        )
        return self.establishment_repository.save(establishment)

    def get_establishment(self, establishment_id: int) -> Optional[Establishment]:
        """Get an establishment by ID."""
        return self.establishment_repository.get_by_id(establishment_id)

    def get_all_establishments(self) -> List[Establishment]:
        """Get all establishments."""
        return self.establishment_repository.get_all()

    def add_tag_to_establishment(
        self, establishment_id: int, tag_name: str
    ) -> EstablishmentTag:
        """Add a tag to an establishment."""
        self.tag_service.create_tag_if_not_exists(tag_name)
        return self.establishment_repository.add_tag(establishment_id, tag_name)

    def search_establishments(
        self, tag_weights: Dict[str, float], limit: int = 10
    ) -> List[Establishment]:
        """Search establishments by tags and their weights."""
        if not tag_weights:
            raise ValueError("At least one tag must be provided")

        return self.establishment_repository.get_by_tags(tag_weights, limit)

    def search_by_moods(
        self, tag_names: List[str], limit: int = 10
    ) -> List[Establishment]:
        """Search establishments by mood tags, using the mood graph for related moods."""
        mood_graph = self.tag_service.get_mood_graph()

        tag_weights: Dict[str, float] = {}

        for tag_name in tag_names:
            tag_weights[tag_name] = 1.0

            if tag_name in mood_graph:
                for related_name, weight in mood_graph[tag_name].items():
                    if (
                        related_name not in tag_weights
                        or weight > tag_weights[related_name]
                    ):
                        tag_weights[related_name] = weight

        return self.establishment_repository.get_by_tags(tag_weights, limit)

    def add_comment(self, establishment_id: int, text: str, rating: int) -> Comment:
        """Add a comment to an establishment."""
        if not 1 <= rating <= 10:
            raise ValueError("Rating must be between 1 and 10")

        establishment = self.get_establishment(establishment_id)
        if not establishment:
            raise ValueError(f"Establishment with id {establishment_id} not found")

        comment = Comment(
            id=None,
            establishment_id=establishment_id,
            text=text,
            rating=rating,
        )
        return self.comment_repository.save(comment)
