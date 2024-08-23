import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from config import TestConfig
from database import db
from models.produto_model import Produto

class ProdutoModelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura a aplicação e o banco de dados para testes."""
        cls.app = create_app(TestConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Limpa o banco de dados após os testes e remove o contexto da aplicação."""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_salvar_produto(self):
        """Teste para salvar um produto no banco de dados."""
        produto = Produto(descricao='Produto Teste', preco=10.0)
        produto.salvar()
        produto_salvo = Produto.query.filter_by(descricao='Produto Teste').first()
        self.assertIsNotNone(produto_salvo)
        self.assertEqual(produto_salvo.descricao, 'Produto Teste')
        self.assertEqual(produto_salvo.preco, 10.0)

    def test_atualizar_produto(self):
        """Teste para atualizar um produto existente."""
        produto = Produto(descricao='Produto Atualizar', preco=20.0)
        produto.salvar()
        produto.descricao = 'Produto Atualizado'
        produto.preco = 25.0
        produto.atualizar()
        produto_atualizado = Produto.query.filter_by(id=produto.id).first()
        self.assertEqual(produto_atualizado.descricao, 'Produto Atualizado')
        self.assertEqual(produto_atualizado.preco, 25.0)

    def test_deletar_produto(self):
        """Teste para deletar um produto do banco de dados."""
        produto = Produto(descricao='Produto Deletar', preco=30.0)
        produto.salvar()
        produto.deletar()
        produto_deletado = Produto.query.filter_by(descricao='Produto Deletar').first()
        self.assertIsNone(produto_deletado)

    def test_get_produtos(self):
        """Teste para obter todos os produtos do banco de dados."""
        produto1 = Produto(descricao='Produto 1', preco=40.0)
        produto2 = Produto(descricao='Produto 2', preco=50.0)
        produto1.salvar()
        produto2.salvar()
        produtos = Produto.get_produtos()
        self.assertGreaterEqual(len(produtos), 2)
        self.assertIn(produto1, produtos)
        self.assertIn(produto2, produtos)

if __name__ == '__main__':
    unittest.main()
