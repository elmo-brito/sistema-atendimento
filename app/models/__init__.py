from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

# --- Models ---

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    perfil = db.Column(db.String(20), nullable=False, default='cliente') # cliente, atendente, admin
    ativo = db.Column(db.Boolean, default=True)
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_exp = db.Column(db.DateTime, nullable=True)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    solicitacoes_criadas = db.relationship('Solicitacao', backref='cliente', lazy='dynamic', foreign_keys='Solicitacao.cliente_id')
    solicitacoes_atribuidas = db.relationship('Solicitacao', backref='atendente', lazy='dynamic', foreign_keys='Solicitacao.atendente_id')
    mensagens = db.relationship('Mensagem', backref='autor', lazy='dynamic')
    logs = db.relationship('LogAuditoria', backref='usuario', lazy='dynamic')

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<Usuario {self.email}>'

@login.user_loader
def load_user(id):
    return db.session.get(Usuario, int(id))

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(200))
    prazo_horas = db.Column(db.Integer, default=48)
    
    solicitacoes = db.relationship('Solicitacao', backref='categoria', lazy='dynamic')
    artigos = db.relationship('Artigo', backref='categoria', lazy='dynamic')

    def __repr__(self):
        return f'<Categoria {self.nome}>'

class Solicitacao(db.Model):
    __tablename__ = 'solicitacoes'
    id = db.Column(db.Integer, primary_key=True)
    protocolo = db.Column(db.String(20), unique=True, index=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    atendente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default='Aberto')
    prioridade = db.Column(db.String(20), default='Média')
    prazo_sla = db.Column(db.DateTime)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    atualizado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    mensagens = db.relationship('Mensagem', backref='solicitacao', lazy='dynamic', cascade="all, delete-orphan")
    sla_logs = db.relationship('SLA', backref='solicitacao', lazy='dynamic', cascade="all, delete-orphan")
    avaliacao = db.relationship('Avaliacao', backref='solicitacao', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Solicitacao {self.protocolo}>'

class Mensagem(db.Model):
    __tablename__ = 'mensagens'
    id = db.Column(db.Integer, primary_key=True)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey('solicitacoes.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    anexos = db.relationship('Anexo', backref='mensagem_obj', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Mensagem {self.id}>'

class Anexo(db.Model):
    __tablename__ = 'anexos'
    id = db.Column(db.Integer, primary_key=True)
    mensagem_id = db.Column(db.Integer, db.ForeignKey('mensagens.id'), nullable=False)
    caminho = db.Column(db.String(255), nullable=False)
    nome_original = db.Column(db.String(150))
    tipo = db.Column(db.String(50))
    tamanho = db.Column(db.Integer)

    def __repr__(self):
        return f'<Anexo {self.id}>'

class SLA(db.Model):
    __tablename__ = 'sla_logs'
    id = db.Column(db.Integer, primary_key=True)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey('solicitacoes.id'), nullable=False)
    vencimento = db.Column(db.DateTime, nullable=False)
    cumprido = db.Column(db.Boolean, default=False)
    resolvido_em = db.Column(db.DateTime)

    def __repr__(self):
        return f'<SLA {self.id} Solicitacao={self.solicitacao_id}>'

class LogAuditoria(db.Model):
    __tablename__ = 'logs_auditoria'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    acao = db.Column(db.String(100), nullable=False)
    tabela = db.Column(db.String(50))
    registro_id = db.Column(db.Integer)
    detalhes = db.Column(db.Text)
    ip = db.Column(db.String(45))
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    def __repr__(self):
        return f'<LogAuditoria {self.id} Acao={self.acao}>'

class Artigo(db.Model):
    __tablename__ = 'artigos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)

    def __repr__(self):
        return f'<Artigo {self.titulo}>'

class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'
    id = db.Column(db.Integer, primary_key=True)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey('solicitacoes.id'), unique=True, nullable=False)
    nota = db.Column(db.Integer, nullable=False) # 1 a 5
    comentario = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
