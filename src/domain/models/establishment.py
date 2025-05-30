from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from .comment import Comment


@dataclass
class EstablishmentTag:
    """Tag associated with an establishment."""

    tag_name: str
    count: int = 1


@dataclass
class Establishment:
    """Domain model for Establishment."""

    id: Optional[int]
    name: str
    description: str
    tags: List[EstablishmentTag]
    comments: List[Comment] = None
    score: Optional[float] = None
    created_at: datetime = datetime.utcnow()

    def __str__(self) -> str:
        return f"<Establishment {self.name}>"
