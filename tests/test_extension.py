# tests/test_extension.py
# Tests for the API extension
from flask import Flask
from flask_api_sqlalchemy import Api
from flask_sqlalchemy import SQLAlchemy


def test_extension_initialization(app: Flask, db: SQLAlchemy):
    """Test that the extension can be initialized properly."""
    # Create API instance
    api = Api()

    # Initialize the extension
    api.init_app(app, db)

    # Assert that the extension is properly initialized
    assert api.app == app
    assert api.db == db
    assert api.blueprint is not None
    assert api.api is not None


def test_model_discovery(app: Flask, db: SQLAlchemy):
    """Test that the extension discovers models correctly."""

    # Create models
    class TestUser(db.Model):
        __tablename__ = "test_user"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), nullable=False)

    class TestProduct(db.Model):
        __tablename__ = "test_product"
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), nullable=False)

    # Create tables
    db.create_all()

    # Create API instance
    api = Api()
    api.init_app(app, db)

    # Assert that models are discovered
    assert "TestUser" in api.models
    assert "TestProduct" in api.models

    # Assert that API models are created
    assert "TestUser" in api.api_models
    assert "TestProduct" in api.api_models

    # Assert that namespaces are created
    assert "TestUser" in api.namespaces
    assert "TestProduct" in api.namespaces


def test_sqlalchemy_type_mapping(app: Flask, db: SQLAlchemy):
    """Test mapping of SQLAlchemy types to Flask-RESTX fields."""

    # Create model with various column types
    class TypeTest(db.Model):
        __tablename__ = "type_test"
        id = db.Column(db.Integer, primary_key=True)
        string_col = db.Column(db.String(80), nullable=False)
        text_col = db.Column(db.Text, nullable=True)
        integer_col = db.Column(db.Integer, nullable=False)
        float_col = db.Column(db.Float, nullable=True)
        boolean_col = db.Column(db.Boolean, nullable=False)
        date_col = db.Column(db.Date, nullable=True)
        datetime_col = db.Column(db.DateTime, nullable=True)

    # Create tables
    db.create_all()

    # Create API instance
    api = Api()
    api.init_app(app, db)

    # Get the generated API model
    api_model = api.api_models["TypeTest"]

    # Assert that fields are mapped correctly
    assert "id" in api_model
    assert "string_col" in api_model
    assert "text_col" in api_model
    assert "integer_col" in api_model
    assert "float_col" in api_model
    assert "boolean_col" in api_model
    assert "date_col" in api_model
    assert "datetime_col" in api_model
