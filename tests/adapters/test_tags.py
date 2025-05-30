import pytest
import json
from domain.models.tag import Tag, TagRelationship


def test_get_tags_list(client, session, auth_headers):
    """Test getting list of tags."""
    # Create test tags
    tag1 = Tag(name="Happy", description="Feeling happy")
    tag2 = Tag(name="Calm", description="Feeling calm")
    session.add_all([tag1, tag2])
    session.commit()

    response = client.get("/tags", headers=auth_headers)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]["name"] == "Happy"
    assert data[1]["name"] == "Calm"


def test_create_tag_as_admin(client, session, auth_headers):
    """Test creating new tag as admin."""
    data = {"name": "Excited", "description": "Feeling excited"}

    response = client.post("/tags", json=data, headers=auth_headers)
    assert response.status_code == 201

    tag = session.query(Tag).first()
    assert tag.name == "Excited"
    assert tag.description == "Feeling excited"


def test_create_tag_as_user(client, session):
    """Test creating tag as regular user."""
    headers = {"Authorization": "Bearer user-token"}
    data = {"name": "Excited", "description": "Feeling excited"}

    response = client.post("/tags", json=data, headers=headers)
    assert response.status_code == 403


def test_create_duplicate_tag(client, session, auth_headers):
    """Test creating tag with duplicate name."""
    # Create initial tag
    tag = Tag(name="Happy", description="Feeling happy")
    session.add(tag)
    session.commit()

    data = {"name": "Happy", "description": "Another happy description"}

    response = client.post("/tags", json=data, headers=auth_headers)
    assert response.status_code == 400
    assert b"Tag already exists" in response.data


def test_create_tag_relationship(client, session, auth_headers):
    """Test creating tag relationship."""
    # Create tags
    tag1 = Tag(name="Happy", description="Feeling happy")
    tag2 = Tag(name="Excited", description="Feeling excited")
    session.add_all([tag1, tag2])
    session.commit()

    data = {"source_tag_name": "Happy", "target_tag_name": "Excited", "weight": 0.8}

    response = client.post("/tags/relationships", json=data, headers=auth_headers)
    assert response.status_code == 201

    rel = session.query(TagRelationship).first()
    assert rel.source_tag_name == "Happy"
    assert rel.target_tag_name == "Excited"
    assert rel.weight == 0.8


def test_create_invalid_tag_relationship(client, session, auth_headers):
    """Test creating relationship with non-existent tags."""
    data = {
        "source_tag_name": "NonExistent1",
        "target_tag_name": "NonExistent2",
        "weight": 0.8,
    }

    response = client.post("/tags/relationships", json=data, headers=auth_headers)
    assert response.status_code == 400


def test_get_tag_relationships(client, session, auth_headers):
    """Test getting tag relationships."""
    # Create tags and relationship
    tag1 = Tag(name="Happy", description="Feeling happy")
    tag2 = Tag(name="Excited", description="Feeling excited")
    rel = TagRelationship(
        source_tag_name="Happy", target_tag_name="Excited", weight=0.8
    )
    session.add_all([tag1, tag2, rel])
    session.commit()

    response = client.get("/tags/Happy/relationships", headers=auth_headers)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["source_tag_name"] == "Happy"
    assert data[0]["target_tag_name"] == "Excited"
    assert data[0]["weight"] == 0.8


def test_get_nonexistent_tag_relationships(client, auth_headers):
    """Test getting relationships for non-existent tag."""
    response = client.get("/tags/NonExistent/relationships", headers=auth_headers)
    assert response.status_code == 404


def test_create_tag_with_invalid_data(client, auth_headers):
    """Test creating tag with invalid data."""
    data = {"name": "", "description": "Invalid tag"}  # Empty name

    response = client.post("/tags", json=data, headers=auth_headers)
    assert response.status_code == 400


def test_create_relationship_with_invalid_weight(client, session, auth_headers):
    """Test creating relationship with invalid weight."""
    # Create tags
    tag1 = Tag(name="Happy", description="Feeling happy")
    tag2 = Tag(name="Excited", description="Feeling excited")
    session.add_all([tag1, tag2])
    session.commit()

    data = {
        "source_tag_name": "Happy",
        "target_tag_name": "Excited",
        "weight": 1.5,  # Weight should be between 0 and 1
    }

    response = client.post("/tags/relationships", json=data, headers=auth_headers)
    assert response.status_code == 400
