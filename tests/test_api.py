import pytest
import json

@pytest.fixture
def admin_user(app):
    with app.app_context():
        from app.models import Usuario
        user = Usuario(nome="Admin", email="admin@test.com", perfil="admin")
        user.set_senha("password")
        from app import db
        db.session.add(user)
        db.session.commit()
        return user

def test_api_register(client):
    data = {
        "nome": "API User",
        "email": "api@test.com",
        "senha": "password123"
    }
    response = client.post('/api/auth/register', 
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 201
    assert response.get_json()['status'] == 'success'

def test_api_login(client, admin_user):
    data = {
        "email": "admin@test.com",
        "senha": "password"
    }
    response = client.post('/api/auth/login', 
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'success'

def test_api_get_solicitacoes_unauthorized(client):
    response = client.get('/api/solicitacoes')
    assert response.status_code == 302 # Redirects to login

def test_api_get_solicitacoes_authorized(client, admin_user):
    # Login first
    client.post('/api/auth/login', 
                data=json.dumps({"email": "admin@test.com", "senha": "password"}),
                content_type='application/json')
    
    response = client.get('/api/solicitacoes')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'success'
