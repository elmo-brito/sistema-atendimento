from app import create_app, db
from app.models import Usuario

app = create_app()
with app.app_context():
    # Update all users to be active if they are NULL
    users = Usuario.query.filter(Usuario.ativo == None).all()
    print(f"Updating {len(users)} users with NULL active status...")
    for u in users:
        u.ativo = True
    db.session.commit()
    print("Done.")
