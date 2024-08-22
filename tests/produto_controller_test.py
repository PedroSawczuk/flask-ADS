import unittest
from app import create_app
from models.produto_model import Produto
from flask import url_for

class ProdutoControllerTestCase(unittest.TestCase):
    def setUp(self):
        """Configura o ambiente para os testes."""
        self.app = create_app('config.TestConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Cria o banco de dados e as tabelas
        with self.app.app_context():
            Produto.__table__.create(self.app.config['SQLALCHEMY_DATABASE'])
    
    def tearDown(self):
        """Remove o ambiente de testes."""
        with self.app.app_context():
            Produto.__table__.drop(self.app.config['SQLALCHEMY_DATABASE'])
        self.app_context.pop()

    def test_criar_produto(self):
        """Testa a criação de um produto."""
        response = self.client.post(url_for('produto.index'), data={
            'descricao': 'Produto Teste',
            'preco': '123,45'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento após criação
        self.assertIn(b'Produto "Produto Teste" adicionado com sucesso!', response.data)

        # Verifica se o produto foi realmente adicionado
        with self.app.app_context():
            produto = Produto.query.filter_by(descricao='Produto Teste').first()
            self.assertIsNotNone(produto)
            self.assertEqual(produto.preco, 123.45)

    def test_deletar_produto(self):
        """Testa a exclusão de um produto."""
        produto = Produto(descricao='Produto Deletar', preco=50.0)
        produto.salvar()

        response = self.client.get(url_for('produto.deleta', id=produto.id))
        self.assertEqual(response.status_code, 302)  # Redirecionamento após exclusão

        # Verifica se o produto foi realmente removido
        with self.app.app_context():
            produto = Produto.query.get(produto.id)
            self.assertIsNone(produto)

if __name__ == '__main__':
    unittest.main()
