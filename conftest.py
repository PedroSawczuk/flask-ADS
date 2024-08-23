import pytest
from flask import Flask
from app import create_app  # Adjust the import according to your project structure

@pytest.fixture
def client():
    app = create_app()  # Ensure you have a factory function to create your Flask app
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client
