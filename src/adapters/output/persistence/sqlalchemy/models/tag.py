from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from domain.models.tag import Tag, TagRelationship
from .base import Base


class TagModel(Base):
    """SQLAlchemy model for tags."""

    __tablename__ = "tags"

    name = Column(String(50), primary_key=True)
    description = Column(String(500))

    def to_domain(self) -> Tag:
        """Convert to domain model."""
        return Tag(name=self.name, description=self.description)

    @staticmethod
    def from_domain(tag: Tag) -> "TagModel":
        """Create from domain model."""
        return TagModel(name=tag.name, description=tag.description)


class TagRelationshipModel(Base):
    """SQLAlchemy model for tag relationships."""

    __tablename__ = "tag_relationships"

    source_tag_name = Column(String(50), ForeignKey("tags.name"), primary_key=True)
    target_tag_name = Column(String(50), ForeignKey("tags.name"), primary_key=True)
    weight = Column(Float, default=0.0)

    source_tag = relationship("TagModel", foreign_keys=[source_tag_name])
    target_tag = relationship("TagModel", foreign_keys=[target_tag_name])

    def to_domain(self) -> TagRelationship:
        """Convert to domain model."""
        return TagRelationship(
            source_tag_name=self.source_tag_name,
            target_tag_name=self.target_tag_name,
            weight=self.weight,
        )
