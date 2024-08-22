"""
José Estevão Machado Zanetti - pt-br - 15/08/2024
Cliente Models
"""

import regex
from sqlalchemy import *
from database import db

class Validador:

    @staticmethod
    def valida_nome(nome):
        if not nome:
            raise ValueError('Nome inválido.')
        pattern = r'^[\p{L}\'\-\s]+$'
        if not regex.match(pattern, nome):
            raise ValueError('Nome inválido. Não use números ou caracteres especiais.')
        nome = regex.sub(r'\s+', ' ', nome).strip()
        partes_do_nome = nome.split()
        preposicoes = ['da', 'de', 'do', 'das', 'dos']
        nome_formatado = ' '.join([parte.capitalize() if parte.lower() not in preposicoes else parte.lower() for parte in partes_do_nome])
        return nome_formatado

    @staticmethod
    def valida_cpf(cpf):
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError('CPF inválido. Deve ter 11 dígitos numéricos...')
        if cpf in ['0' * 11, '1' * 11, '2' * 11, '3' * 11, '4' * 11, '5' * 11, '6' * 11, '7' * 11, '8' * 11, '9' * 11]:
            raise ValueError('CPF inválido. Sequência repetida...')
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        if resto < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto
        if int(cpf[9]) != digito1:
            raise ValueError('CPF inválido. Dígito verificador 1 não confere...')
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        if resto < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto
        if int(cpf[10]) != digito2:
            raise ValueError('CPF inválido. Dígito verificador 2 não confere...')
        return cpf

    @staticmethod
    def valida_email(email):
        pattern = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        if not regex.match(pattern, email):
            raise ValueError('Email inválido.')
        return email

    @staticmethod
    def valida_cep(cep):
        pattern = r'^\d{5}-\d{3}$'
        if not regex.match(pattern, cep):
            raise ValueError('CEP inválido. Deve seguir o formato 00000-000.')
        return cep

    @staticmethod
    def formata_texto(texto):
        return ' '.join(word.capitalize() if word.lower() not in ['da', 'de', 'do', 'das', 'dos'] else word.lower() for word in regex.sub(r'\s+', ' ', texto).strip().split())

    @staticmethod
    def valida_endereco(logradouro, numero, complemento, bairro, cep, cidade, uf):
        logradouro = Validador.formata_texto(logradouro)
        bairro = Validador.formata_texto(bairro)
        cidade = Validador.formata_texto(cidade)
        cep = Validador.valida_cep(cep)
        if not all([logradouro, numero, bairro, cep, cidade, uf]):
            raise ValueError('Todos os campos de endereço, exceto complemento, são obrigatórios.')
        if not regex.match(r'^[A-Z]{2}$', uf):
            raise ValueError('UF inválido. Deve ser composto por duas letras maiúsculas.')
        return logradouro, numero, complemento, bairro, cep, cidade, uf


class Pessoas:
    __abstract__ = True
    def __init__(self, nome, cpf, logradouro, numero, complemento, bairro, cep, cidade, uf, telefone, email):
        self.nome = Validador.valida_nome(nome)
        self.__cpf = Validador.valida_cpf(cpf)
        self.email = Validador.valida_email(email)
        self.telefone = telefone
        
        logradouro, numero, complemento, bairro, cep, cidade, uf = Validador.valida_endereco(logradouro, numero, complemento, bairro, cep, cidade, uf)
        
        self.endereco = {
            'logradouro': logradouro,
            'numero': numero,
            'complemento': complemento,
            'bairro': bairro,
            'cep': cep,
            'cidade': cidade,
            'uf': uf
        }


    @property
    def cpf(self):
        return self.__cpf

class Clientes(Pessoas, db.Model):
    def __init__(self, nome, cpf, logradouro, numero, complemento, bairro, cep, cidade, uf, telefone, email):
        super().__init__(nome, cpf, logradouro, numero, complemento, bairro, cep, cidade, uf, telefone, email)

    __tablename__ = 'clientes'  

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    cpf = db.Column(db.String, nullable=False)  
    logradouro = db.Column(db.String, nullable=False) 
    numero = db.Column(db.String, nullable=False)
    complemento = db.Column(db.String, nullable=False)
    bairro = db.Column(db.String, nullable=False)
    cep = db.Column(db.String, nullable=False)  
    cidade = db.Column(db.String, nullable=False)  
    uf = db.Column(db.String, nullable=False)  
    telefone = db.Column(db.String, nullable=False)  
    email = db.Column(db.String, nullable=False)  

    def __init__(self, nome, cpf, logradouro, numero, complemento, bairro,
                 cep, cidade, uf, telefone, email, id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cep = cep
        self.cidade = cidade
        self.uf = uf
        self.telefone = telefone
        self.email = email

    
    def salvar(self):
        db.session.add(self)
        db.session.commit() 

    
    def atualizar(self):
        db.session.commit()  

    
    def deletar(self):
        db.session.delete(self)  
        db.session.commit()  

    @staticmethod
    def get_clientes():
        return db.session.query(Clientes).all()

    @staticmethod
    def get_cliente(id):
        return db.session.query(Clientes).get(id)