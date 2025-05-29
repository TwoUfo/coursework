from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.establishment import Establishment


class EstablishmentServicePort(ABC):
    """Interface for establishment service."""

    @abstractmethod
    def create_establishment(
        self, name: str, description: Optional[str] = None
    ) -> Establishment:
        """Create a new establishment."""
        pass

    @abstractmethod
    def add_tag_to_establishment(self, establishment_id: int, tag_name: str) -> None:
        """Add a tag count to an establishment."""
        pass

    @abstractmethod
    def search_by_moods(
        self, tag_names: List[str], limit: int = 10
    ) -> List[Establishment]:
        """Search establishments by mood tags, using the mood graph for related moods."""
        pass

    @abstractmethod
    def get_establishment(self, establishment_id: int) -> Optional[Establishment]:
        """Get establishment by ID."""
        pass
