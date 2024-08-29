import pytest
from models.produto_model import Produto
from app import create_app, db

@pytest.fixture(scope='module')
def client():
    app = create_app('config.TestConfig')  # Use uma configuração de teste
    app.testing = True

    with app.app_context():
        db.create_all()  # Cria as tabelas
        yield app.test_client()
        db.drop_all()  # Limpa após o teste

def test_add_product(client):
    # Define os dados do produto
    produto_data = {
        'descricao': 'Produto Teste',
        'preco': '19,99'
    }

    # Envia uma solicitação POST para adicionar o produto
    response = client.post('/produtos/', data=produto_data)
    
    # Verifica o código de status da resposta
    assert response.status_code == 302  # Redireciona após POST
    
    # Verifica se o produto foi adicionado
    produtos = Produto.get_produtos()
    produto = next((p for p in produtos if p.descricao == 'Produto Teste'), None)
    assert produto is not None
    assert produto.preco == 19.99

def test_update_product(client):
    # Adiciona um produto para atualizar
    produto_data = {
        'descricao': 'Produto Teste',
        'preco': '19,99'
    }
    response = client.post('/produtos/', data=produto_data)
    assert response.status_code == 302  # Redireciona após POST

    # Recupera o produto adicionado
    produto = Produto.get_produtos()
    produto = next((p for p in produto if p.descricao == 'Produto Teste'), None)
    assert produto is not None

    # Define os dados atualizados do produto
    update_data = {
        'descricao': 'Produto Teste Atualizado',
        'preco': '29,99'
    }

    # Envia uma solicitação POST para atualizar o produto
    response = client.post(f'/produtos/editar/{produto.id}', data=update_data)
    assert response.status_code == 302  # Redireciona após POST
    
    # Verifica se o produto foi atualizado
    produto_atualizado = Produto.get_produto(produto.id)
    assert produto_atualizado.descricao == 'Produto Teste Atualizado'
    assert produto_atualizado.preco == 29.99

def test_delete_product(client):
    # Adiciona um produto para excluir
    produto_data = {
        'descricao': 'Produto Teste',
        'preco': '19,99'
    }
    response = client.post('/produtos/', data=produto_data)
    assert response.status_code == 302  # Redireciona após POST

    # Recupera o produto adicionado
    produto = Produto.get_produtos()
    produto = next((p for p in produto if p.descricao == 'Produto Teste'), None)
    assert produto is not None

    # Envia uma solicitação GET para excluir o produto
    response = client.get(f'/produtos/deleta/{produto.id}')
    assert response.status_code == 302  # Redireciona após GET
    
    # Verifica se o produto foi excluído
    produto_excluido = Produto.get_produto(produto.id)
    assert produto_excluido is None
