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

        dados_validos = {
            'nome': nome,
            'cpf': cpf,
            'logradouro': logradouro,
            'numero': numero,
            'complemento': complemento,
            'bairro': bairro,
            'cep': cep,
            'cidade': cidade,
            'uf': uf,
            'telefone': telefone,
            'email': email
        }

        try:
            # Validação dos dados
            dados_validos['nome'] = Validador.valida_nome(nome)
            dados_validos['cpf'] = Validador.valida_cpf(cpf)
            dados_validos['email'] = Validador.valida_email(email)
            dados_validos['cep'] = Validador.valida_cep(cep)
            dados_validos['logradouro'], dados_validos['numero'], dados_validos['complemento'], dados_validos['bairro'], dados_validos['cep'], dados_validos['cidade'], dados_validos['uf'] = Validador.valida_endereco(logradouro, numero, complemento, bairro, cep, cidade, uf)

            # Criação do cliente
            cliente = Clientes(
                nome=dados_validos['nome'], cpf=dados_validos['cpf'], logradouro=dados_validos['logradouro'],
                numero=dados_validos['numero'], complemento=dados_validos['complemento'], bairro=dados_validos['bairro'],
                cep=dados_validos['cep'], cidade=dados_validos['cidade'], uf=dados_validos['uf'],
                telefone=dados_validos['telefone'], email=dados_validos['email']
            )
            cliente.salvar()
            flash('Cliente cadastrado com sucesso!', 'success')
            return redirect(url_for('cliente.index'))

        except ValueError as e:
            flash(f'Erro: {e}', 'error')
            return render_template('clientes/novo_cliente.html', **dados_validos)

    return render_template('clientes/novo_cliente.html')

@cliente_blueprint.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Clientes.get_cliente(id)
    if not cliente:
        flash('Cliente não encontrado.', 'error')
        return redirect(url_for('cliente.index'))

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

        dados_validos = {
            'nome': nome,
            'cpf': cpf,
            'logradouro': logradouro,
            'numero': numero,
            'complemento': complemento,
            'bairro': bairro,
            'cep': cep,
            'cidade': cidade,
            'uf': uf,
            'telefone': telefone,
            'email': email
        }

        try:
            # Validação dos dados
            dados_validos['nome'] = Validador.valida_nome(nome)
            dados_validos['cpf'] = Validador.valida_cpf(cpf)
            dados_validos['email'] = Validador.valida_email(email)
            dados_validos['cep'] = Validador.valida_cep(cep)
            dados_validos['logradouro'], dados_validos['numero'], dados_validos['complemento'], dados_validos['bairro'], dados_validos['cep'], dados_validos['cidade'], dados_validos['uf'] = Validador.valida_endereco(logradouro, numero, complemento, bairro, cep, cidade, uf)

            # Atualização do cliente
            cliente.nome = dados_validos['nome']
            cliente.cpf = dados_validos['cpf']
            cliente.logradouro = dados_validos['logradouro']
            cliente.numero = dados_validos['numero']
            cliente.complemento = dados_validos['complemento']
            cliente.bairro = dados_validos['bairro']
            cliente.cep = dados_validos['cep']
            cliente.cidade = dados_validos['cidade']
            cliente.uf = dados_validos['uf']
            cliente.telefone = dados_validos['telefone']
            cliente.email = dados_validos['email']
            cliente.atualizar()
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('cliente.index'))

        except ValueError as e:
            flash(f'Erro: {e}', 'error')

    # Preenche o formulário com os dados atuais do cliente
    return render_template('clientes/editar_cliente.html', cliente=cliente)

@cliente_blueprint.route("/deleta/<int:id>", methods=['GET'])
def deleta_cliente(id):
    cliente = Clientes.get_cliente(id)
    if not cliente:
        flash('Cliente não encontrado.', 'error')
        return redirect(url_for('cliente.index'))

    cliente.deletar()
    flash('Cliente deletado com sucesso!', 'success')
    return redirect(url_for('cliente.index'))

def init_app(app):
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/cliente/novo', 'novo_cliente', novo_cliente, methods=['GET', 'POST'])
    app.add_url_rule('/editar/<int:id>', 'editar_cliente', editar_cliente, methods=['GET', 'POST'])
    app.add_url_rule('/cliente/deleta/<int:id>', 'deleta_cliente', deleta_cliente, methods=['GET'])
