from app import create_app, db
from app.models import Usuario

app = create_app()
client = app.test_client()

print("--- Attempting Login ---")
login_data = {'email': 'admin@sac.com', 'senha': 'admin123'}
response = client.post('/login', data=login_data, follow_redirects=True)

print(f"Login Response Status: {response.status_code}")
print(f"Login Response URL: {response.request.url}")

if response.status_code == 500:
    print("--- 500 ERROR DETECTED ON LOGIN/REDIRECT ---")
    print(response.data.decode('utf-8'))
else:
    print("--- Attempting Dashboard Access ---")
    response = client.get('/admin/dashboard')
    print(f"Dashboard Response Status: {response.status_code}")
    if response.status_code == 500:
        print("--- 500 ERROR DETECTED ON DASHBOARD ---")
        # We can't easily get the traceback from response.data if DEBUG is off, 
        # but in our environment DEBUG=True is usually set in run.py.
        # However, create_app uses Config which might not have it.
        print(response.data.decode('utf-8'))
