# tests/conftest.py
# Test configuration and fixtures
from typing import Any, Dict, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_api_sqlalchemy import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("sqlite:///:memory:")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# Configuration for the Flask application
class Config:
    """Configuration class for Flask application."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Test models
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="items")


def get_app() -> Flask:
    """Create and configure a Flask app for testing.

    Returns:
        Flask: Flask application configured for testing
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    return app


def get_db(app: Flask) -> SQLAlchemy:
    """Create an SQLAlchemy instance.

    Args:
        app (Flask): Flask application instance

    Returns:
        SQLAlchemy: SQLAlchemy instance
    """
    # Create Flask-SQLAlchemy instance
    db = SQLAlchemy(app)

    # Import the SQLAlchemy Base and tables into Flask-SQLAlchemy
    # This is tricky but can be done by associating the metadata
    Base.metadata.bind = db.engine

    # Create tables from the Base metadata
    Base.metadata.create_all(db.engine)

    # Add utility methods to make the interface similar to Flask-SQLAlchemy
    db.Model = Base

    return db


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    """Create and configure a Flask app for testing.

    Yields:
        Generator[Flask, None, None]: Flask application configured for testing
    """
    # Create the Flask application
    app = get_app()

    # Create an application context
    with app.app_context():
        yield app


@pytest.fixture
def db(app: Flask) -> Generator[SQLAlchemy, None, None]:
    """Create an SQLAlchemy instance.

    Args:
        app (Flask): Flask application fixture

    Returns:
        SQLAlchemy: SQLAlchemy instance
    """

    db = get_db(app)

    # Create all tables
    db.create_all()

    yield db

    # Clean up
    db.session.remove()
    db.drop_all()


@pytest.fixture
def api(app: Flask, db: Generator[SQLAlchemy, None, None]) -> Api:
    """Create an API instance.

    Args:
        app (Flask): Flask application fixture
        db (SQLAlchemy): SQLAlchemy instance

    Returns:
        Api: API instance
    """
    api = Api()
    api.init_app(app, db)
    return api


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create a test client for the Flask application.

    Args:
        app (Flask): Flask application fixture

    Returns:
        FlaskClient: Flask test client
    """
    return app.test_client()


@pytest.fixture
def user_data() -> Dict[str, Any]:
    """Sample user data for testing.

    Returns:
        Dict[str, Any]: Sample user data
    """
    return {"username": "testuser", "email": "test@example.com", "is_active": True}


@pytest.fixture
def create_user(db: SQLAlchemy, user_data: Dict[str, Any]) -> User:
    """Create a user in the database for testing.

    Args:
        db (SQLAlchemy): SQLAlchemy instance
        user_data (Dict[str, Any]): Sample user data

    Returns:
        User: Created user instance
    """
    user = User(
        username=user_data["username"],
        email=user_data["email"],
        is_active=user_data["is_active"],
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def item_data() -> Dict[str, Any]:
    """Sample item data for testing.

    Returns:
        Dict[str, Any]: Sample item data
    """
    return {"name": "Test Item", "description": "This is a test item"}


@pytest.fixture
def create_item(db: SQLAlchemy, create_user: User, item_data: Dict[str, Any]) -> Item:
    """Create an item in the database for testing.

    Args:
        db (SQLAlchemy): SQLAlchemy instance
        create_user (User): User fixture
        item_data (Dict[str, Any]): Sample item data

    Returns:
        Item: Created item instance
    """
    item = Item(
        name=item_data["name"],
        description=item_data["description"],
        user_id=create_user.id,
    )

    db.session.add(item)
    db.session.commit()

    return item
