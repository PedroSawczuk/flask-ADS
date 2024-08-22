import unittest
from app import create_app, db
from config import TestConfig
from models.produto_model import Produto

class TestIndexHtml(unittest.TestCase):

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

    def test_index_page_loads_correctly(self):
        response = self.client.get('/produtos/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Produtos', response.data)
        self.assertIn(b'Adicionar Novo Produto', response.data)

    def test_lista_produtos_exibida(self):
        Produto(descricao='Produto 1', preco=10.00).salvar()
        Produto(descricao='Produto 2', preco=20.00).salvar()

        response = self.client.get('/produtos/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Produto 1', response.data)
        self.assertIn(b'Produto 2', response.data)

    def test_mensagem_sem_produtos(self):
        response = self.client.get('/produtos/')
        self.assertEqual(response.status_code, 200)
        # Decodificar o conteúdo da resposta para comparar com a string esperada
        response_data = response.data.decode('utf-8')
        self.assertIn('Ainda não existem produtos cadastrados...', response_data)

    def test_botoes_acao_presentes(self):
        Produto(descricao='Produto para teste', preco=15.00).salvar()
        response = self.client.get('/produtos/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ativar', response.data)  # Verifica botão Ativar/Desativar
        self.assertIn(b'Editar', response.data)
        self.assertIn(b'Deletar', response.data)

if __name__ == '__main__':
    unittest.main()
