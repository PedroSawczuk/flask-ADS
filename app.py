import os
from flask import Flask, render_template
from database import db
from controller.cliente_controller import cliente_blueprint
from controller.produto_controller import produto_blueprint

def create_app(config=None):
    app = Flask(__name__)

    # Configuração padrão
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_DIR = os.path.join(BASE_DIR, 'dao')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(DB_DIR, 'ifro2024.db')
    app.secret_key = 'seu segredo'

    # Aplicando configurações personalizadas, se fornecidas
    if config:
        app.config.from_object(config)
    
    db.init_app(app)

    # Registrando blueprints
    app.register_blueprint(cliente_blueprint, url_prefix='/clientes')
    app.register_blueprint(produto_blueprint, url_prefix='/produtos')

    return app

# Criação da aplicação
app = create_app()

# Função para criar tabelas
def create_tables():
    with app.app_context():
        db.create_all()
        print('Tabelas criadas com sucesso!')

# Criando tabelas ao iniciar o arquivo
create_tables()

# Rota principal
@app.route('/')
def home():
    return render_template('home.html')

# Executando a aplicação
if __name__ == '__main__':
    app.run(debug=True)
