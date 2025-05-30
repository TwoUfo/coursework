from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.comment import Comment


class CommentRepositoryPort(ABC):
    """Interface for comment repository."""

    @abstractmethod
    def save(self, comment: Comment) -> Comment:
        """Save a comment."""
        pass

    @abstractmethod
    def get_by_establishment_id(self, establishment_id: int) -> List[Comment]:
        """Get all comments for an establishment."""
        pass 