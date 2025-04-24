#!/usr/bin/env python
# debug_app.py
# Standalone Flask app for debugging the API in a browser

import logging
import random
import string

from flask import Flask, render_template_string
from flask_api_sqlalchemy import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="items")

    def __repr__(self):
        return f"<Item {self.name}>"


# Flask app configuration
class Config:
    """Configuration class for the Flask application."""

    DEBUG = False
    TESTING = False
    # SQLALCHEMY_DATABASE_URI = "sqlite:///debug.db"  # Use file DB for persistence
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://user:password@postgres:5432/test_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "debug-secret-key"


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Create SQLAlchemy instance
    db = SQLAlchemy(app)

    # Import the SQLAlchemy Base and tables into Flask-SQLAlchemy
    with app.app_context():
        Base.metadata.bind = db.engine
    db.Model = Base

    # Create API instance
    Api(
        app,
        db,
        title="Flask API SQLAlchemy Debug App",
        description="Debug interface for manually testing the API",
        version="1.0",
        doc="/docs",  # Swagger UI will be available at /docs
        want_logs=True,
    )  # Enable API logs

    # Create all tables
    with app.app_context():
        db.create_all()

        # Check if we need to create sample data
        if db.session.query(User).count() == 0:
            # Create sample users
            populate_sample_data(db)

    # Add a simple home page that provides links to API docs
    @app.route("/")
    def home():
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Flask API SQLAlchemy Debug App</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #333; }
                .container { border: 1px solid #ddd; padding: 20px; border-radius: 5px; }
                .endpoint { margin-bottom: 15px; }
                a { color: #0066cc; text-decoration: none; }
                a:hover { text-decoration: underline; }
                code { background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>Flask API SQLAlchemy Debug App</h1>
            <div class="container">
                <h2>API Documentation</h2>
                <p>Visit the <a href="/docs">Swagger UI documentation</a> to interactively test the API endpoints.</p>
                
                <h2>Available API Endpoints</h2>
                <div class="endpoint">
                    <h3>Users</h3>
                    <ul>
                        <li><code>GET /api/users/</code> - List all users</li>
                        <li><code>POST /api/users/</code> - Create a new user</li>
                        <li><code>GET /api/users/{id}</code> - Get a specific user</li>
                        <li><code>PUT /api/users/{id}</code> - Update a user</li>
                        <li><code>DELETE /api/users/{id}</code> - Delete a user</li>
                    </ul>
                </div>
                
                <div class="endpoint">
                    <h3>Items</h3>
                    <ul>
                        <li><code>GET /api/items/</code> - List all items</li>
                        <li><code>POST /api/items/</code> - Create a new item</li>
                        <li><code>GET /api/items/{id}</code> - Get a specific item</li>
                        <li><code>PUT /api/items/{id}</code> - Update an item</li>
                        <li><code>DELETE /api/items/{id}</code> - Delete an item</li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """)  # noqa: E501

    return app, db


def populate_sample_data(db):
    """Populate the database with sample data for debugging."""
    logger.info("Creating sample data for debugging...")

    # Create sample users
    users = []
    for i in range(3):
        username = f"user{i}"
        user = User(username=username, email=f"{username}@example.com", is_active=True)
        users.append(user)
        db.session.add(user)

    # Create sample items
    items = []
    for i in range(5):
        # Assign to a random user
        user = random.choice(users)
        item = Item(
            name=f"Item {i}",
            description=f"This is a sample item {i} for debugging",
            user_id=user.id,
        )
        items.append(item)
        db.session.add(item)

    # Commit changes
    try:
        db.session.commit()
        logger.info(f"Created {len(users)} sample users and {len(items)} sample items")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating sample data: {e}")
        raise


def generate_random_string(length=10):
    """Generate a random string of specified length."""
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


if __name__ == "__main__":
    app, db = create_app()

    # Run the Flask development server
    app.run(host="0.0.0.0", port=5000, debug=False)
