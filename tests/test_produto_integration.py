# test_integration.py
import pytest
from app import create_app, db
from models.produto_model import Produto

@pytest.fixture(scope='module')
def client():
    app = create_app('config.TestConfig')  # Use a test config
    app.testing = True

    with app.app_context():
        db.create_all()  # Create tables
        yield app.test_client()
        db.drop_all()  # Clean up after the test

def test_add_product(client):
    # Define product details
    produto_data = {
        'descricao': 'Produto Teste',
        'preco': '19,99'
    }

    # Send a POST request to add the product
    response = client.post('/produtos/', data=produto_data)
    
    # Assert that the product was added successfully
    assert response.status_code == 302  # Redirect after POST
    
    # Follow the redirect to check if the product exists in the database
    produtos = Produto.get_produtos()
    
    assert any(p.descricao == 'Produto Teste' for p in produtos)
