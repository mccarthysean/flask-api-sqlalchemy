# tests/test_api_endpoints.py
# Tests for the API endpoints
from http import HTTPStatus
from typing import Any, Dict

from flask.testing import FlaskClient
from flask_restx import Api
from tests.conftest import Item, User


def test_database_content(db):
    users = db.session.query(User).all()
    print(f"Users in database: {users}")


# @pytest.mark.skip(reason="Not working yet")
def test_get_users_empty(client: FlaskClient, api: Api):
    """Test getting all users when the database is empty."""
    # Make a GET request to the users endpoint
    response = client.get("/api/users/")

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.OK
    assert response.json == []


# @pytest.mark.skip(reason="Not working yet")
def test_create_user(client: FlaskClient, api: Api, user_data: Dict[str, Any]):
    """Test creating a new user via the API."""
    # Make a POST request to create a user
    response = client.post(
        "/api/users/", json=user_data, content_type="application/json"
    )

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.CREATED
    assert response.json["username"] == user_data["username"]
    assert response.json["email"] == user_data["email"]
    assert "id" in response.json


# @pytest.mark.skip(reason="Not working yet")
def test_get_users(client: FlaskClient, api: Api, create_user: User):
    """Test getting all users."""
    # Make a GET request to the users endpoint
    response = client.get("/api/users/")

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.OK
    assert len(response.json) == 1
    assert response.json[0]["id"] == create_user.id
    assert response.json[0]["username"] == create_user.username
    assert response.json[0]["email"] == create_user.email


# @pytest.mark.skip(reason="Not working yet")
def test_get_user(client: FlaskClient, api: Api, create_user: User):
    """Test getting a specific user."""
    # Make a GET request to the user endpoint
    response = client.get(f"/api/users/{create_user.id}")

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.OK
    assert response.json["id"] == create_user.id
    assert response.json["username"] == create_user.username
    assert response.json["email"] == create_user.email


def test_get_user_not_found(client: FlaskClient, api: Api):
    """Test getting a user that doesn't exist."""
    # Make a GET request for a non-existent user
    response = client.get("/api/users/999")

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.NOT_FOUND


# @pytest.mark.skip(reason="Not working yet")
def test_update_user(client: FlaskClient, api: Api, create_user: User):
    """Test updating a user."""
    # Data for updating the user
    update_data = {"username": "updateduser", "email": "updated@example.com"}

    # Make a PUT request to update the user
    response = client.put(
        f"/api/users/{create_user.id}",
        json=update_data,
        content_type="application/json",
    )

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.OK
    assert response.json["username"] == update_data["username"]
    assert response.json["email"] == update_data["email"]
    assert response.json["id"] == create_user.id


# @pytest.mark.skip(reason="Not working yet")
def test_delete_user(client: FlaskClient, api: Api, create_user: User):
    """Test deleting a user."""
    # Make a DELETE request to delete the user
    response = client.delete(f"/api/users/{create_user.id}")

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.NO_CONTENT

    # Try to get the deleted user
    get_response = client.get(f"/api/users/{create_user.id}")

    # Assert that the user was deleted
    assert get_response.status_code == HTTPStatus.NOT_FOUND


def test_get_items(client: FlaskClient, api: Api, create_item: Item):
    """Test getting all items."""
    # Make a GET request to the items endpoint
    response = client.get("/api/items/")

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.OK
    assert len(response.json) == 1
    assert response.json[0]["id"] == create_item.id
    assert response.json[0]["name"] == create_item.name
    assert response.json[0]["description"] == create_item.description
    assert response.json[0]["user_id"] == create_item.user_id


def test_create_item(client, api, create_user):
    # Payload must include ALL required fields
    payload = {
        "name": "Test Item",
        "description": "This is a test item",
        "user_id": create_user.id,  # This is critical!
    }

    # Make the API request
    response = client.post("/api/items/", json=payload, content_type="application/json")

    # Assertions
    assert response.status_code == 201
    assert response.json["name"] == payload["name"]
    assert response.json["user_id"] == create_user.id
