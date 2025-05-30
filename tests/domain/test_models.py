import pytest
from datetime import datetime

from domain.models.user import User
from domain.models.tag import Tag, TagRelationship
from domain.models.establishment import Establishment, EstablishmentTag


def test_user_model():
    """Test User model."""
    user = User(id=1, email="test@example.com", password_hash="hash123", is_admin=False)

    assert user.id == 1
    assert user.email == "test@example.com"
    assert user.password_hash == "hash123"
    assert not user.is_admin

    # Test to_dict method
    user_dict = user.to_dict()
    assert user_dict["id"] == 1
    assert user_dict["email"] == "test@example.com"
    assert user_dict["is_admin"] is False
    assert "password_hash" not in user_dict


def test_tag_model():
    """Test Tag model."""
    tag = Tag(name="Happy", description="Feeling happy")

    assert tag.name == "Happy"
    assert tag.description == "Feeling happy"
    assert str(tag) == "<Tag Happy>"


def test_tag_relationship_model():
    """Test TagRelationship model."""
    relationship = TagRelationship(
        id=1, source_tag_name="Happy", target_tag_name="Excited", weight=0.8
    )

    assert relationship.id == 1
    assert relationship.source_tag_name == "Happy"
    assert relationship.target_tag_name == "Excited"
    assert relationship.weight == 0.8
    assert str(relationship) == "<TagRelationship Happy -> Excited (0.8)>"


def test_establishment_tag_model():
    """Test EstablishmentTag model."""
    est_tag = EstablishmentTag(tag_name="Cozy", count=3)

    assert est_tag.tag_name == "Cozy"
    assert est_tag.count == 3


def test_establishment_model():
    """Test Establishment model."""
    tags = [
        EstablishmentTag(tag_name="Cozy", count=3),
        EstablishmentTag(tag_name="Quiet", count=2),
    ]

    establishment = Establishment(
        id=1,
        name="Test Place",
        description="A test establishment",
        tags=tags,
        score=0.95,
    )

    assert establishment.id == 1
    assert establishment.name == "Test Place"
    assert establishment.description == "A test establishment"
    assert len(establishment.tags) == 2
    assert establishment.score == 0.95
    assert isinstance(establishment.created_at, datetime)
    assert str(establishment) == "<Establishment Test Place>"


def test_establishment_model_default_values():
    """Test Establishment model default values."""
    establishment = Establishment(
        id=1, name="Test Place", description="A test establishment", tags=[]
    )

    assert establishment.score is None
    assert isinstance(establishment.created_at, datetime)
    assert establishment.tags == []
