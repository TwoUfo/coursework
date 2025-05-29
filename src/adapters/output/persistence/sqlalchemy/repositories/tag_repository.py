from typing import List, Optional

from sqlalchemy.orm import Session

from adapters.output.persistence.sqlalchemy.models.tag import (
    TagModel,
    TagRelationshipModel,
)
from domain.models.tag import Tag, TagRelationship
from domain.ports.output.tag_repository import TagRepositoryPort


class SQLAlchemyTagRepository(TagRepositoryPort):
    """SQLAlchemy implementation of TagRepositoryPort."""

    def __init__(self, session: Session):
        self.session = session

    def save(self, tag: Tag) -> Tag:
        """Save a tag to the database."""
        tag_model = TagModel.from_domain(tag)
        self.session.merge(tag_model)  # Use merge instead of add for upsert behavior
        self.session.commit()
        return tag_model.to_domain()

    def get_by_name(self, name: str) -> Optional[Tag]:
        """Get a tag by name."""
        tag_model = self.session.query(TagModel).get(name)
        return tag_model.to_domain() if tag_model else None

    def get_all(self) -> List[Tag]:
        """Get all tags."""
        tag_models = self.session.query(TagModel).all()
        return [model.to_domain() for model in tag_models]

    def save_relationship(self, relationship: TagRelationship) -> TagRelationship:
        """Save a tag relationship to the database."""
        rel_model = TagRelationshipModel.from_domain(relationship)
        self.session.add(rel_model)
        self.session.commit()
        return rel_model.to_domain()

    def get_all_relationships(self) -> List[TagRelationship]:
        """Get all tag relationships."""
        rel_models = self.session.query(TagRelationshipModel).all()
        return [model.to_domain() for model in rel_models]
