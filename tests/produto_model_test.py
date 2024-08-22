import unittest
from app import create_app, db
from config import TestConfig
from models.produto_model import Produto

class ProdutoControllerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestConfig)
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_criar_produto(self):
        response = self.client.post('/produtos/', data={
            'descricao': 'Produto Teste',
            'preco': '19.99'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após a criação
        self.assertIn(b'Produto "Produto Teste" adicionado com sucesso!', response.data)

        # Verifica se o produto foi adicionado ao banco de dados
        produto = Produto.query.first()
        self.assertIsNotNone(produto)
        self.assertEqual(produto.descricao, 'Produto Teste')
        self.assertEqual(produto.preco, 19.99)

    def test_deletar_produto(self):
        produto = Produto(descricao='Produto a ser deletado', preco=10.00)
        produto.salvar()

        response = self.client.get(f'/produtos/deleta/{produto.id}')
        self.assertEqual(response.status_code, 302)  # Redireciona após a exclusão

        # Verifica se o produto foi removido do banco de dados
        produto_deletado = Produto.query.get(produto.id)
        self.assertIsNone(produto_deletado)

    def test_editar_produto(self):
        produto = Produto(descricao='Produto Original', preco=5.00)
        produto.salvar()

        response = self.client.post(f'/produtos/editar/{produto.id}', data={
            'descricao': 'Produto Editado',
            'preco': '9.99'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após a atualização

        # Verifica se o produto foi atualizado no banco de dados
        produto_atualizado = Produto.query.get(produto.id)
        self.assertEqual(produto_atualizado.descricao, 'Produto Editado')
        self.assertEqual(produto_atualizado.preco, 9.99)

    def test_listar_produtos(self):
        Produto(descricao='Produto 1', preco=15.00).salvar()
        Produto(descricao='Produto 2', preco=25.00).salvar()

        response = self.client.get('/produtos/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Produto 1', response.data)
        self.assertIn(b'Produto 2', response.data)

if __name__ == '__main__':
    unittest.main()
