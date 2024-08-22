import os
from flask import Flask, render_template
from database import db  
from controller.cliente_controller import cliente_blueprint
from controller.produto_controller import produto_blueprint

def create_app(config=None):
    app = Flask(__name__)

    # Configuração padrão
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
    DB_DIR = os.path.join(BASE_DIR, 'db')  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(DB_DIR, 'ifro2024.db')  
    app.secret_key = 'seu segredo'

    # Aplicando configurações personalizadas, se fornecidas
    if config:
        app.config.from_object(config)
    
    db.init_app(app)  

    app.register_blueprint(cliente_blueprint, url_prefix='/clientes')
    app.register_blueprint(produto_blueprint, url_prefix='/produtos')

    return app



def create_tables():
    with app.app_context(): 
        db.create_all() 
        print('Tabelas criadas com sucesso!')


app = create_app()


create_tables()

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    create_tables()  
    app.run(debug=True)
