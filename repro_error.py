from app import create_app, db
from app.models import Usuario

app = create_app()
with app.app_context():
    try:
        count = Usuario.query.count()
        print(f"Number of users: {count}")
        user = Usuario.query.first()
        print(f"First user: {user}")
    except Exception as e:
        print(f"Error querying users: {e}")
        import traceback
        traceback.print_exc()
