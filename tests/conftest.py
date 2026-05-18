import pytest
from app import create_app, db
from config import Config
from app.models import Categoria, Usuario

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth_client(client, app):
    # Create and login a client
    with app.app_context():
        from app.services.auth_service import AuthService
        auth = AuthService()
        auth.register('Cliente Teste', 'cliente@teste.com', 'senha123', perfil='cliente')
        
        cat = Categoria(nome='Geral_Conftest')
        db.session.add(cat)
        db.session.commit()
        cat_id = cat.id
        
    client.post('/login', data={'email': 'cliente@teste.com', 'senha': 'senha123'}, follow_redirects=True)
    return client, cat_id
