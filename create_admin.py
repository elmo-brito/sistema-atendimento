from app import create_app, db
from app.models import Usuario
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# 🔐 Dados do novo administrador
nome = "Administrador"
email = "admin@sistema.com"
senha = "admin123"  # você pode alterar depois
perfil = "admin"

# 🔄 Gera o hash da senha
senha_hash = generate_password_hash(senha)

# 🧱 Cria o usuário
admin = Usuario(
    nome=nome,
    email=email,
    senha_hash=senha_hash,
    perfil=perfil,
    ativo=True
)

# 💾 Salva no banco
db.session.add(admin)
db.session.commit()

print(f"✅ Usuário administrador criado com sucesso!\nEmail: {email}\nSenha: {senha}")
