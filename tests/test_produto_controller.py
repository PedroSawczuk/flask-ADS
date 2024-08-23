import sys
import os
import pytest
from models.produto_model import *
from app import create_app, db as _db
# Adiciona o diretório raiz do projeto ao caminho de importação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test Flask application."""
    app = create_app(config_name="testing")  # Substitua "myapp" pelo nome do seu módulo/pacote Flask
    # Aqui você pode configurar o app para o modo de teste, como definir uma URL de banco de dados de teste

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()

@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_criacao_produto(client):
    """Testa a criação de um novo produto."""
    data = {
        'descricao': 'Test Product',
        'preco': '10.50'
    }
    response = client.post('/', data=data, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Produto \"Test Product\" adicionado com sucesso!" in response.data

def test_delecao_produto(client):
    """Testa a exclusão de um produto existente."""
    # Primeiro, crie um produto para teste
    produto = Produto(descricao="Product to Delete", preco=9.99)
    produto.salvar()

    # Agora, tente excluí-lo
    response = client.get(f'/deleta/{produto.id}', follow_redirects=True)
    
    assert response.status_code == 200
    # Note que aqui assumimos que não há uma mensagem específica para confirmação de deleção,
    # então apenas verificamos o status HTTP. Ajuste conforme sua lógica de negócio.
