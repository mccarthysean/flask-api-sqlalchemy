# tests/test_api_endpoints.py
# Tests for the API endpoints
import random
import string
from http import HTTPStatus

from flask.testing import FlaskClient
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from tests.conftest import User


def test_database_content(db):
    users = db.session.query(User).all()
    print(f"Users in database: {users}")


# @pytest.mark.skip(reason="Not working yet")
def test_get_users_not_empty(client: FlaskClient, api: Api):
    """Test getting all users when the database is not empty."""

    # Make a GET request to the users endpoint
    response = client.get("/api/users/")

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.OK
    assert response.json, "Response should not be empty"
    assert len(response.json) > 0, "Response should contain users"


# @pytest.mark.skip(reason="Not working yet")
def test_create_user(client: FlaskClient, api: Api):
    """Test creating a new user via the API."""

    # Make a POST request to create a user
    random_username = "".join(random.choice(string.ascii_letters) for _ in range(10))
    random_email = f"{random_username}@notarealco.com"

    response = client.post(
        "/api/users/",
        json={
            "username": random_username,
            "email": random_email,
            "is_active": True,
        },
        content_type="application/json",
    )

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.CREATED
    assert response.json["username"] == random_username
    assert response.json["email"] == random_email
    assert response.json["is_active"] is True
    assert response.json["id"] is not None
    assert "id" in response.json


# @pytest.mark.skip(reason="Not working yet")
def test_get_users(client: FlaskClient, api: Api, user_data: dict, db: SQLAlchemy):
    """Test getting all users."""
    # Make a GET request to the users endpoint
    response = client.get("/api/users/")

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.OK
    users = response.json
    # Check if the database is not empty
    assert len(users) > 0, "Response should contain users"


# @pytest.mark.skip(reason="Not working yet")
def test_get_user(client: FlaskClient, api: Api, db: SQLAlchemy):
    """Test getting a specific user."""

    username: str = "".join(random.choice(string.ascii_letters) for _ in range(10))
    email: str = f"{username}@notarealco.com"
    user_model: User = User(
        username=username,
        email=email,
        is_active=True,
    )
    # Add the user to the database
    db.session.add(user_model)
    db.session.commit()

    # Make a GET request to the user endpoint
    response = client.get(f"/api/users/{user_model.id}")

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.OK
    assert response.json["id"] == user_model.id
    assert response.json["username"] == user_model.username
    assert response.json["email"] == user_model.email


def test_get_user_not_found(client: FlaskClient, api: Api):
    """Test getting a user that doesn't exist."""
    # Make a GET request for a non-existent user
    response = client.get("/api/users/999")

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.NOT_FOUND


# @pytest.mark.skip(reason="Not working yet")
def test_update_user(client: FlaskClient, api: Api, db: SQLAlchemy):
    """Test updating a user."""

    # Create a user to update
    original_username: str = "".join(
        random.choice(string.ascii_letters) for _ in range(10)
    )  # noqa: E501
    original_email: str = f"{original_username}@notarealco.com"
    new_user = User(
        username=original_username,
        email=original_email,
        is_active=True,
    )
    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    # Data for updating the user
    updated_username: str = "".join(
        random.choice(string.ascii_letters) for _ in range(10)
    )  # noqa: E501
    updated_email: str = f"{updated_username}@notarealco.com"
    update_data = {"username": updated_username, "email": updated_email}

    # Make a PUT request to update the user
    response = client.put(
        f"/api/users/{new_user.id}",
        json=update_data,
        content_type="application/json",
    )

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.OK
    assert response.json["username"] == updated_username
    assert response.json["email"] == updated_email
    assert response.json["id"] == new_user.id


# @pytest.mark.skip(reason="Not working yet")
def test_delete_user(client: FlaskClient, api: Api, db: SQLAlchemy):
    """Test deleting a user."""
    # Create a user to delete
    username: str = "".join(random.choice(string.ascii_letters) for _ in range(10))
    new_user = User(
        username=username,
        email=f"{username}@notarealco.com",
        is_active=True,
    )
    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()
    new_user_id: int = new_user.id
    # Assert that the user was created
    assert new_user_id is not None

    # Try to get the deleted user
    get_response = client.get(f"/api/users/{new_user_id}")

    # Assert that the user was created
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json["id"] == new_user_id
    assert get_response.json["username"] == new_user.username
    assert get_response.json["email"] == new_user.email
    assert get_response.json["is_active"] is True

    # Make a DELETE request to delete the user
    response = client.delete(f"/api/users/{new_user_id}")

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.NO_CONTENT

    # Try to get the deleted user
    get_response = client.get(f"/api/users/{new_user_id}")

    # Assert that the user was deleted
    assert get_response.status_code == HTTPStatus.NOT_FOUND


def test_get_items(client: FlaskClient, api: Api):
    """Test getting all items."""
    # Make a GET request to the items endpoint
    response = client.get("/api/items/")

    # Assert that the response is correct
    assert response.status_code == HTTPStatus.OK
    assert len(response.json) > 0, "Response should contain items"


def test_create_item(client, api: Api, db: SQLAlchemy):
    """Test creating a new item via the API."""
    # Create a user to associate with the item
    username: str = "".join(random.choice(string.ascii_letters) for _ in range(10))
    email: str = f"{username}@notarealco.com"
    new_user = User(
        username=username,
        email=email,
        is_active=True,
    )
    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    # Payload must include ALL required fields
    payload = {
        "name": "Test Item",
        "description": "This is a test item",
        "user_id": new_user.id,  # This is critical!
    }

    # Make the API request
    response = client.post("/api/items/", json=payload, content_type="application/json")

    # Assertions
    assert response.status_code == 201
    assert response.json["name"] == payload["name"]
    assert response.json["user_id"] == new_user.id
