# tests/conftest.py
# Test configuration and fixtures
from typing import Any, Dict, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    JSON,
    TIMESTAMP,
    BigInteger,
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    Interval,
    LargeBinary,
    Numeric,
    SmallInteger,
    String,
    Text,
    Time,
)
from sqlalchemy.dialects.postgresql import (
    ARRAY,
    BIT,
    BYTEA,
    CIDR,
    ENUM,
    # HSTORE,
    INET,
    JSONB,
    MACADDR,
    MONEY,
    REAL,
    TSVECTOR,
    UUID,
    VARCHAR,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from flask_api_sqlalchemy import Api

# engine = create_engine("sqlite:///:memory:")
Base = declarative_base()
# Session = sessionmaker(bind=engine)
# session = Session()


# Configuration for the Flask application
class Config:
    """Configuration class for Flask application."""

    TESTING = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://user:password@postgres:5432/test_db"
    )
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


class AllTypes(Base):
    """Model with all PostgreSQL data types for testing."""

    __tablename__ = "all_types"

    id = Column(Integer, primary_key=True)

    # Numeric types
    smallint_col = Column(SmallInteger)
    integer_col = Column(Integer)
    bigint_col = Column(BigInteger)
    numeric_col = Column(Numeric(10, 2))
    real_col = Column(REAL)
    double_col = Column(Float)
    money_col = Column(MONEY)

    # Character types
    char_col = Column(String(10))
    varchar_col = Column(VARCHAR(255))
    text_col = Column(Text)

    # Date/Time types
    timestamp_col = Column(TIMESTAMP)
    timestamptz_col = Column(TIMESTAMP(timezone=True))
    date_col = Column(Date)
    time_col = Column(Time)
    timetz_col = Column(Time(timezone=True))
    interval_col = Column(Interval)

    # Boolean
    boolean_col = Column(Boolean)

    # Network
    inet_col = Column(INET)
    cidr_col = Column(CIDR)
    macaddr_col = Column(MACADDR)

    # Binary
    bytea_col = Column(BYTEA)
    binary_col = Column(LargeBinary)

    # UUID
    uuid_col = Column(UUID)

    # JSON
    json_col = Column(JSON)
    jsonb_col = Column(JSONB)

    # Arrays
    int_array_col = Column(ARRAY(Integer))
    text_array_col = Column(ARRAY(String))

    # Other types
    enum_col = Column(ENUM("value1", "value2", name="my_enum_type"))
    # hstore_col = Column(HSTORE)
    xml_col = Column(Text)  # SQLAlchemy doesn't have a specific XML type
    tsvector_col = Column(TSVECTOR)
    bit_col = Column(BIT)


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
def all_types_data() -> Dict[str, Any]:
    """Sample data for testing all types of columns.

    Returns:
        Dict[str, Any]: Sample data for all types record
    """
    return {
        "smallint_col": 1,
        "integer_col": 2,
        "bigint_col": 3,
        "numeric_col": 4.5,
        "real_col": 5.6,
        "double_col": 7.8,
        "money_col": "$9.35",
        "char_col": "test",
        "varchar_col": "test",
        "text_col": "test",
        "timestamp_col": None,
        "timestamptz_col": None,
        "date_col": None,
        "time_col": None,
        "timetz_col": None,
        "interval_col": None,
        "boolean_col": True,
        "inet_col": None,
        "cidr_col": None,
        "macaddr_col": None,
        "bytea_col": b"test",
        "binary_col": b"test",
        "uuid_col": None,
        "json_col": {"key": "value"},
        "jsonb_col": {"key": "value"},
        "int_array_col": [1, 2, 3],
        "text_array_col": ["a", "b", "c"],
        # Add other fields as needed
        "enum_col": "value1",
        # "hstore_col": {"key": "value"},
        "xml_col": "<root><child>test</child></root>",
        "tsvector_col": None,
        "bit_col": None,
    }


@pytest.fixture
def item_data() -> Dict[str, Any]:
    """Sample item data for testing.

    Returns:
        Dict[str, Any]: Sample item data
    """
    return {"name": "Test Item", "description": "This is a test item"}


# @pytest.fixture
def create_user(db: SQLAlchemy, user_data: Dict[str, Any]) -> User:
    """Create a user in the database for testing.

    Args:
        db (SQLAlchemy): SQLAlchemy instance
        user_data (Dict[str, Any]): Sample user data

    Returns:
        User: Created user instance
    """
    user_model = db.session.query(User).filter_by(**user_data).first()
    if user_model:
        return user_model

    user = User(**user_data)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating user: {e}")
        # raise

    return user


# @pytest.fixture
def create_item(db: SQLAlchemy, create_user: User, item_data: Dict[str, Any]) -> Item:
    """Create an item in the database for testing.

    Args:
        db (SQLAlchemy): SQLAlchemy instance
        create_user (User): User fixture
        item_data (Dict[str, Any]): Sample item data

    Returns:
        Item: Created item instance
    """
    item_model = db.session.query(Item).filter_by(**item_data).first()
    if item_model:
        return item_model

    item = Item(
        name=item_data["name"],
        description=item_data["description"],
        user_id=create_user.id,
    )

    db.session.add(item)
    db.session.commit()

    return item


# @pytest.fixture
def create_all_types_record(db: SQLAlchemy, all_types_data: Dict[str, Any]) -> AllTypes:
    """Create an item with all types in the database for testing.

    Args:
        db (SQLAlchemy): SQLAlchemy instance
        all_types_data (Dict[str, Any]): Sample data for all items
        create_user (User): User fixture

    Returns:
        AllTypes: Created item with all types instance
    """
    all_types_model = (
        db.session.query(AllTypes)
        .filter_by(xml_col="<root><child>test</child></root>")
        .first()
    )
    if all_types_model:
        return all_types_model

    # Create a record with all types
    all_types = AllTypes(**all_types_data)

    db.session.add(all_types)
    db.session.commit()

    return all_types


@pytest.fixture
def db(
    app: Flask,
    user_data: Dict[str, Any],
    all_types_data: Dict[str, Any],
    item_data: Dict[str, Any],
) -> Generator[SQLAlchemy, None, None]:
    """Create an SQLAlchemy instance.

    Args:
        app (Flask): Flask application fixture

    Returns:
        SQLAlchemy: SQLAlchemy instance
    """

    db = get_db(app)

    # Create all tables
    db.drop_all()
    db.create_all()

    # Insert table records
    user: User = create_user(db, user_data)
    item: Item = create_item(db, user, item_data)
    all_types: AllTypes = create_all_types_record(db, all_types_data)

    assert user
    assert item
    assert all_types

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
