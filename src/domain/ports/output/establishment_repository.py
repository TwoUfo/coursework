from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from domain.models.establishment import Establishment, EstablishmentTag


class EstablishmentRepositoryPort(ABC):
    """Interface for establishment repository."""

    @abstractmethod
    def save(self, establishment: Establishment) -> Establishment:
        """Save an establishment to the database."""
        pass

    @abstractmethod
    def get_by_id(self, establishment_id: int) -> Optional[Establishment]:
        """Get an establishment by ID."""
        pass

    @abstractmethod
    def add_tag(self, establishment_id: int, tag_name: str) -> EstablishmentTag:
        """Add or increment a tag count for an establishment."""
        pass

    @abstractmethod
    def get_by_tags(
        self, tag_weights: Dict[str, float], limit: int = 10
    ) -> List[Establishment]:
        """
        Get establishments by tags and their weights.

        Args:
            tag_weights: Dictionary mapping tag names to their weights
            limit: Maximum number of results to return
        """
        pass
