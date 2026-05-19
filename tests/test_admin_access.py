import pytest
from app.models import Usuario
from flask_login import login_user

def test_admin_access_integrity(client, app):
    with app.app_context():
        # Create an admin user if not exists
        admin = Usuario.query.filter_by(email='admin_test@sistema.com').first()
        if not admin:
            admin = Usuario(nome='Admin Test', email='admin_test@sistema.com', perfil='admin')
            admin.set_senha('admin123')
            from app import db
            db.session.add(admin)
            db.session.commit()
            admin_id = admin.id
        else:
            admin_id = admin.id

    # Login as admin
    client.post('/login', data={
        'email': 'admin_test@sistema.com',
        'senha': 'admin123'
    }, follow_redirects=True)

    # Test access to admin dashboard
    response = client.get('/admin/dashboard')
    assert response.status_code == 200
    assert b'Dashboard' in response.data

    # Test access to users management
    response = client.get('/admin/usuarios')
    assert response.status_code == 200
    assert b'Usu\xc3\xa1rios' in response.data

    # Test access to categories management
    response = client.get('/admin/categorias')
    assert response.status_code == 200
    assert b'Categorias' in response.data

def test_client_access_denied_to_admin(client, app):
    with app.app_context():
        # Create a client user if not exists
        cliente = Usuario.query.filter_by(email='cliente_test@sistema.com').first()
        if not cliente:
            cliente = Usuario(nome='Cliente Test', email='cliente_test@sistema.com', perfil='cliente')
            cliente.set_senha('cliente123')
            from app import db
            db.session.add(cliente)
            db.session.commit()

    # Login as client
    client.post('/login', data={
        'email': 'cliente_test@sistema.com',
        'senha': 'cliente123'
    }, follow_redirects=True)

    # Test denied access to admin dashboard
    response = client.get('/admin/dashboard')
    # According to specs, it should be 403 or redirect with error. 
    # Let's see what the current implementation does.
    assert response.status_code in [403, 302]
