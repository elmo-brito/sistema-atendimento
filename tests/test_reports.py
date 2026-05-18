import pytest
from app import db
from app.models import Usuario

def setup_user(app, nome, email, perfil):
    with app.app_context():
        user = Usuario(nome=nome, email=email, perfil=perfil)
        user.set_senha('password')
        db.session.add(user)
        db.session.commit()

def test_reports_dashboard_access_admin(client, app):
    setup_user(app, 'Admin', 'admin@test.com', 'admin')
    client.post('/login', data={'email': 'admin@test.com', 'senha': 'password'}, follow_redirects=True)
    response = client.get('/reports/dashboard')
    assert response.status_code == 200

def test_reports_dashboard_access_atendente(client, app):
    setup_user(app, 'Atendente', 'atendente@test.com', 'atendente')
    client.post('/login', data={'email': 'atendente@test.com', 'senha': 'password'}, follow_redirects=True)
    response = client.get('/reports/dashboard')
    assert response.status_code == 200

def test_reports_dashboard_access_denied_cliente(client, app):
    setup_user(app, 'Cliente', 'cliente@test.com', 'cliente')
    client.post('/login', data={'email': 'cliente@test.com', 'senha': 'password'}, follow_redirects=True)
    response = client.get('/reports/dashboard', follow_redirects=True)
    assert b'Acesso negado.' in response.data

def test_reports_dashboard_unauthorized(client):
    response = client.get('/reports/dashboard', follow_redirects=True)
    assert b'Por favor, fa\xc3\xa7a login para acessar esta p\xc3\xa1gina.' in response.data
