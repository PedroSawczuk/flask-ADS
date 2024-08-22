"""
Pedro Henrique Sawczuk Monteiro - pt-br - 15/08/2024
Cliente Controller
"""

from models.cliente_model import Clientes, Validador
from flask import Blueprint, render_template, request, redirect, url_for, flash

cliente_blueprint = Blueprint('cliente', __name__)

@cliente_blueprint.route('/')
def index():
    clientes = Clientes.get_clientes()
    return render_template('clientes/list_clientes.html', clientes=clientes)

@cliente_blueprint.route('/novo', methods=['GET', 'POST'])
def novo_cliente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        logradouro = request.form.get('logradouro')
        numero = request.form.get('numero')
        complemento = request.form.get('complemento')
        bairro = request.form.get('bairro')
        cep = request.form.get('cep')
        cidade = request.form.get('cidade')
        uf = request.form.get('uf')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        try:
            # Validação dos dados
            nome = Validador.valida_nome(nome)
            cpf = Validador.valida_cpf(cpf)
            email = Validador.valida_email(email)
            cep = Validador.valida_cep(cep)
            logradouro, numero, complemento, bairro, cep, cidade, uf = Validador.valida_endereco(logradouro, numero, complemento, bairro, cep, cidade, uf)

            # Criação do cliente
            cliente = Clientes(nome=nome, cpf=cpf, logradouro=logradouro, numero=numero,
                               complemento=complemento, bairro=bairro, cep=cep,
                               cidade=cidade, uf=uf, telefone=telefone, email=email)
            cliente.salvar()
            flash('Cliente cadastrado com sucesso!', 'success')
            return redirect(url_for('cliente.index'))
        except ValueError as e:
            flash(f'Erro: {e}', 'error')
            # Retorna o formulário com os valores válidos preenchidos e o campo problemático vazio
            return render_template('clientes/novo_cliente.html', nome=nome, cpf=cpf, logradouro=logradouro,
                                   numero=numero, complemento=complemento, bairro=bairro, cep=cep, 
                                   cidade=cidade, uf=uf, telefone=telefone, email=email)

    return render_template('clientes/novo_cliente.html')

@cliente_blueprint.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Clientes.get_cliente(id)
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        logradouro = request.form.get('logradouro')
        numero = request.form.get('numero')
        complemento = request.form.get('complemento')
        bairro = request.form.get('bairro')
        cep = request.form.get('cep')
        cidade = request.form.get('cidade')
        uf = request.form.get('uf')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        try:
            # Validação dos dados
            Validador.valida_nome(nome)
            Validador.valida_cpf(cpf)
            Validador.valida_email(email)
            Validador.valida_cep(cep)
            logradouro, numero, complemento, bairro, cep, cidade, uf = Validador.valida_endereco(logradouro, numero, complemento, bairro, cep, cidade, uf)

            # Atualização do cliente
            cliente.nome = nome
            cliente.cpf = cpf
            cliente.logradouro = logradouro
            cliente.numero = numero
            cliente.complemento = complemento
            cliente.bairro = bairro
            cliente.cep = cep
            cliente.cidade = cidade
            cliente.uf = uf
            cliente.telefone = telefone
            cliente.email = email
            cliente.atualizar()
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('cliente.index'))
        except ValueError as e:
            flash(f'Erro: {e}', 'error')

    return render_template('clientes/editar_cliente.html', cliente=cliente)

@cliente_blueprint.route("/deleta/<int:id>", methods=['GET'])
def deleta_cliente(id):
    cliente = Clientes.get_cliente(id)
    cliente.deletar()
    flash('Cliente deletado com sucesso!', 'success')
    return redirect(url_for('cliente.index'))

def init_app(app):
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/cliente/novo', 'novo_cliente', novo_cliente, methods=['GET', 'POST'])
    app.add_url_rule('/editar/<int:id>', 'editar_cliente', editar_cliente, methods=['GET', 'POST'])
    app.add_url_rule('/cliente/deleta/<int:id>', 'deleta_cliente', deleta_cliente, methods=['GET'])
