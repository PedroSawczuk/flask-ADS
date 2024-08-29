# In conftest.py or a dedicated test config file
import pytest
from app import create_app, db

class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture
def client():
    app = create_app(TestConfig)  # Use TestConfig for testing
    with app.app_context():
        db.create_all()  # Create the tables for testing
        yield app.test_client()
        db.drop_all()  # Clean up after the test
