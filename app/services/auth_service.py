from app.repositories.usuario_repository import UsuarioRepository
from flask_login import logout_user
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone
from app import db
import uuid

class AuthService:
    def __init__(self):
        self.repo = UsuarioRepository()

    def register(self, nome, email, senha, perfil='cliente'):
        if self.repo.get_by_email(email):
            raise ValueError("E-mail já cadastrado.")
        
        senha_hash = generate_password_hash(senha)
        usuario = self.repo.create(nome=nome, email=email, senha_hash=senha_hash, perfil=perfil)
        return usuario

    def login(self, email, senha):
        usuario = self.repo.get_by_email(email)
        if usuario and usuario.check_senha(senha) and usuario.ativo:
            return usuario
        return None

    def logout(self):
        logout_user()

    def alterar_senha(self, user_id, senha_atual, nova_senha):
        usuario = self.repo.get_by_id(user_id)
        if not usuario or not usuario.check_senha(senha_atual):
            raise ValueError("Senha atual incorreta.")
        
        usuario.senha_hash = generate_password_hash(nova_senha)
        self.repo.update(usuario)
        return True

    def recuperar_senha(self, email):
        usuario = self.repo.get_by_email(email)
        if not usuario:
            return False
        
        token = uuid.uuid4().hex
        expiracao = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=2)
        
        usuario.reset_token = token
        usuario.reset_token_exp = expiracao
        self.repo.update(usuario)
        
        # Simulação de envio de e-mail (RF018)
        print(f"DEBUG: Link de recuperação enviado para {email}: /auth/reset-senha/{token}")
        
        return True

    def resetar_senha(self, token, nova_senha):
        usuario = self.repo.model.query.filter_by(reset_token=token).first()
        
        if not usuario:
            raise ValueError("Token inválido.")
            
        if usuario.reset_token_exp < datetime.now(timezone.utc).replace(tzinfo=None):
            raise ValueError("Token expirado.")
            
        usuario.senha_hash = generate_password_hash(nova_senha)
        usuario.reset_token = None
        usuario.reset_token_exp = None
        self.repo.update(usuario)
        return True
