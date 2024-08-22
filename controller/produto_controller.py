from flask import Blueprint, flash, render_template, request, redirect, url_for
from models.produto_model import Produto

produto_blueprint = Blueprint('produto', __name__)

@produto_blueprint.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        descricao = request.form.get('descricao')
        preco = request.form.get('preco')

        # Converte vírgula para ponto no preço
        preco = preco.replace(',', '.')

        produto = Produto(descricao=descricao, preco=float(preco))
        produto.salvar()

        flash(f'Produto "{descricao}" adicionado com sucesso!', 'success')
        return redirect(url_for('produto.index'))

    produtos = Produto.get_produtos()
    return render_template('produtos/index_produto.html', produtos=produtos)

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
        preco = request.form.get('preco')

        # Converte vírgula para ponto no preço
        preco = preco.replace(',', '.')

        produto.preco = float(preco)
        produto.atualizar()
        return redirect(url_for('produto.index'))
    return render_template('produtos/editar_produto.html', produto=produto)

def init_app(app):
    app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/produto/atualiza/<int:id>/<int:status>', 'atualiza', atualiza, methods=['GET'])
    app.add_url_rule('/produto/deleta/<int:id>', 'deleta', deleta, methods=['GET'])
    app.add_url_rule('/produto/editar/<int:id>', 'editar', editar, methods=['GET', 'POST'])
