from dataclasses import dataclass
from typing import Optional


@dataclass
class Tag:
    """Domain model for Tag (mood)."""

    name: str
    description: Optional[str] = None

    def __str__(self) -> str:
        return f"<Tag {self.name}>"


@dataclass
class TagRelationship:
    """Domain model for relationship between tags with weights."""

    id: Optional[int]
    source_tag_name: str
    target_tag_name: str
    weight: float  # Weight between 0 and 1

    def __str__(self) -> str:
        return f"<TagRelationship {self.source_tag_name} -> {self.target_tag_name} ({self.weight})>"
