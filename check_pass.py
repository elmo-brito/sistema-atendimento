from app import create_app, db
from app.models import Usuario

app = create_app()
with app.app_context():
    user = Usuario.query.filter_by(email='admin@sac.com').first()
    if user:
        print(f"User found: {user.email}")
        print(f"Password 'admin123' check: {user.check_senha('admin123')}")
        print(f"Is active: {user.ativo}")
        print(f"Perfil: {user.perfil}")
    else:
        print("User NOT found")
