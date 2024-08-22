"""
Claudinei de Oliveira - pt-BR - 19-06-2023
Manipulando o banco de dados sqlite3 
Adaptado de Giridhar, 2016
""" 
from flask import Blueprint, render_template, request, redirect, url_for
from models.produto_model import Produto

produto_blueprint = Blueprint('produto', __name__)

@produto_blueprint.route("/")
def index():
    produtos = Produto.get_produtos()
    return render_template('produtos/list_produtos.html', produtos=produtos)

@produto_blueprint.route("/novo", methods=['GET', 'POST'])
def novo():
    if request.method == 'POST':
        descricao = request.form.get('descricao')
        preco = request.form.get('preco')
        produto = Produto(descricao=descricao, preco=preco)
        produto.salvar()
        return redirect(url_for('produto.index'))
    return render_template('produtos/novo_produto.html')

@produto_blueprint.route("/atualiza/<int:id>/<int:status>", methods=['GET'])
def atualiza(id, status):
    produto = Produto.get_produto(id)
    produto.status = status
    produto.atualizar()
    return redirect(url_for('produto.index'))

@produto_blueprint.route("/deleta/<int:id>", methods=['GET'])
def deleta(id):
    produto = Produto.get_produto(id)
    produto.deletar()
    return redirect(url_for('produto.index'))

@produto_blueprint.route("/editar/<int:id>", methods=['GET', 'POST'])
def editar(id):
    produto = Produto.get_produto(id)
    if request.method == 'POST':
        produto.descricao = request.form.get('descricao')
        produto.preco = request.form.get('preco')
        produto.atualizar()
        return redirect(url_for('produto.index'))
    return render_template('produtos/editar_produto.html', produto=produto)

def init_app(app):
    # Associando as funções de exibição às respectivas rotas utilizando a função add_url_rule do objeto app do Flask.
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/produto/novo', 'novo', novo, methods=['GET', 'POST'])
    app.add_url_rule('/produto/atualiza/<int:id>/<int:status>', 'atualiza', atualiza, methods=['GET'])
    app.add_url_rule('/produto/deleta/<int:id>', 'deleta', deleta, methods=['GET'])
