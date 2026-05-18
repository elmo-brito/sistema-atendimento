from app import create_app, db
from app.models import Usuario, Categoria

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # Check if admin already exists
        if not Usuario.query.filter_by(email='admin@sac.com').first():
            admin = Usuario(nome='Administrador', email='admin@sac.com', perfil='admin')
            admin.set_senha('admin123')
            db.session.add(admin)
            print("Admin user created: admin@sac.com / admin123")
        
        # Add some categories
        default_categories = ['Suporte Técnico', 'Financeiro', 'Sugestões', 'Reclamações']
        for cat_name in default_categories:
            if not Categoria.query.filter_by(nome=cat_name).first():
                db.session.add(Categoria(nome=cat_name))
                print(f"Category created: {cat_name}")
        
        db.session.commit()
        print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
