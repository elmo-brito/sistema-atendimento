import pytest
from app.models import Usuario

def test_register_unique_email(client, app):
    # Register first user
    response = client.post('/register', data={
        'nome': 'Teste 1',
        'email': 'teste@exemplo.com',
        'senha': 'password123'
    }, follow_redirects=True)
    assert b'Cadastro realizado com sucesso' in response.data

    # Try to register same email
    response = client.post('/register', data={
        'nome': 'Teste 2',
        'email': 'teste@exemplo.com',
        'senha': 'password456'
    }, follow_redirects=True)
    assert b'E-mail j\xc3\xa1 cadastrado' in response.data

def test_login_invalid_credentials(client, app):
    response = client.post('/login', data={
        'email': 'naoexiste@exemplo.com',
        'senha': 'wrong'
    }, follow_redirects=True)
    assert b'Email ou senha inv\xc3\xa1lidos' in response.data
