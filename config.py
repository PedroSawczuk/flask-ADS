class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Banco de dados em memória para testes
    SQLALCHEMY_TRACK_MODIFICATIONS = False
