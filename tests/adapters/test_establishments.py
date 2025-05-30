import pytest
import json
from domain.models.establishment import Establishment, EstablishmentTag
from domain.models.tag import Tag


def test_get_establishments_list(client, session, auth_headers):
    """Test getting list of establishments."""
    # Create test establishments
    est1 = Establishment(name="Place 1", description="Description 1")
    est2 = Establishment(name="Place 2", description="Description 2")
    session.add_all([est1, est2])
    session.commit()

    response = client.get("/establishments", headers=auth_headers)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]["name"] == "Place 1"
    assert data[1]["name"] == "Place 2"


def test_get_establishment_by_id(client, session, auth_headers):
    """Test getting single establishment by ID."""
    est = Establishment(id=1, name="Test Place", description="Test Description")
    session.add(est)
    session.commit()

    response = client.get("/establishments/1", headers=auth_headers)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["name"] == "Test Place"
    assert data["description"] == "Test Description"


def test_get_nonexistent_establishment(client, auth_headers):
    """Test getting non-existent establishment."""
    response = client.get("/establishments/999", headers=auth_headers)
    assert response.status_code == 404


def test_create_establishment_as_admin(client, session, auth_headers):
    """Test creating new establishment as admin."""
    data = {
        "name": "New Place",
        "description": "New Description",
        "tags": ["Cozy", "Quiet"],
    }

    response = client.post("/establishments", json=data, headers=auth_headers)
    assert response.status_code == 201

    est = session.query(Establishment).first()
    assert est.name == "New Place"
    assert est.description == "New Description"


def test_create_establishment_as_user(client, session):
    """Test creating establishment as regular user."""
    headers = {"Authorization": "Bearer user-token"}
    data = {"name": "New Place", "description": "New Description"}

    response = client.post("/establishments", json=data, headers=headers)
    assert response.status_code == 403


def test_add_tags_to_establishment(client, session, auth_headers):
    """Test adding tags to establishment."""
    # Create establishment and tags
    est = Establishment(id=1, name="Test Place", description="Test Description")
    tag1 = Tag(name="Cozy")
    tag2 = Tag(name="Quiet")
    session.add_all([est, tag1, tag2])
    session.commit()

    data = {"tags": ["Cozy", "Quiet"]}

    response = client.post("/establishments/1/tags", json=data, headers=auth_headers)
    assert response.status_code == 200

    est = session.query(Establishment).get(1)
    assert len(est.tags) == 2


def test_search_establishments(client, session, auth_headers):
    """Test searching establishments."""
    # Create test establishments with tags
    est1 = Establishment(name="Cozy Cafe", description="A cozy place")
    est1.tags = [EstablishmentTag(tag_name="Cozy", count=1)]

    est2 = Establishment(name="Quiet Library", description="A quiet place")
    est2.tags = [EstablishmentTag(tag_name="Quiet", count=1)]

    session.add_all([est1, est2])
    session.commit()

    # Search by tag
    data = {"tags": ["Cozy"], "search_term": ""}

    response = client.post("/establishments/search", json=data, headers=auth_headers)
    assert response.status_code == 200

    results = json.loads(response.data)
    assert len(results) == 1
    assert results[0]["name"] == "Cozy Cafe"


def test_search_establishments_by_term(client, session, auth_headers):
    """Test searching establishments by term."""
    # Create test establishments
    est1 = Establishment(name="Coffee Shop", description="Best coffee")
    est2 = Establishment(name="Tea House", description="Best tea")
    session.add_all([est1, est2])
    session.commit()

    data = {"tags": [], "search_term": "coffee"}

    response = client.post("/establishments/search", json=data, headers=auth_headers)
    assert response.status_code == 200

    results = json.loads(response.data)
    assert len(results) == 1
    assert results[0]["name"] == "Coffee Shop"


def test_search_establishments_combined(client, session, auth_headers):
    """Test searching establishments by both tags and term."""
    # Create test establishments with tags
    est1 = Establishment(name="Cozy Coffee", description="A cozy coffee place")
    est1.tags = [EstablishmentTag(tag_name="Cozy", count=1)]

    est2 = Establishment(name="Cozy Tea", description="A cozy tea place")
    est2.tags = [EstablishmentTag(tag_name="Cozy", count=1)]

    session.add_all([est1, est2])
    session.commit()

    data = {"tags": ["Cozy"], "search_term": "coffee"}

    response = client.post("/establishments/search", json=data, headers=auth_headers)
    assert response.status_code == 200

    results = json.loads(response.data)
    assert len(results) == 1
    assert results[0]["name"] == "Cozy Coffee"
