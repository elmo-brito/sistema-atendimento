from app import create_app, db
from app.models import Usuario
from flask_login import current_user, login_user
from flask import session

app = create_app()

with app.test_request_context('/'):
    try:
        print(f"Checking if current_user is authenticated...")
        authenticated = current_user.is_authenticated
        print(f"current_user.is_authenticated: {authenticated}")
        
        user = Usuario.query.first()
        if user:
            print(f"Simulating login for user: {user.email}")
            # Mocking the session to include user_id
            session['_user_id'] = str(user.id)
            # Re-access current_user should now trigger load_user
            print(f"current_user after session mock: {current_user}")
            print(f"current_user.is_authenticated: {current_user.is_authenticated}")
            if current_user.is_authenticated and current_user.id == user.id:
                print("Success! user_loader correctly loaded the user.")
            else:
                print("Failed! user_loader did not load the user correctly.")
        else:
            print("No users found in database to test actual loading.")
            
        print("Success! No 'Missing user_loader' exception raised.")
    except Exception as e:
        print(f"Caught exception: {e}")
        import traceback
        traceback.print_exc()
