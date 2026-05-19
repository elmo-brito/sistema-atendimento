from app import db
from datetime import datetime

class Solicitacao(db.Model):
    __tablename__ = 'solicitacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    protocolo = db.Column(db.String(20), nullable=False, unique=True, index=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    atendente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default="Aberto")
    prioridade = db.Column(db.String(20), default="Média")
    prazo_sla = db.Column(db.DateTime)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cliente = db.relationship("Usuario", foreign_keys=[cliente_id], backref=db.backref("solicitacoes_cliente", lazy='dynamic'))
    atendente = db.relationship("Usuario", foreign_keys=[atendente_id], backref=db.backref("solicitacoes_atendente", lazy='dynamic'))
    categoria = db.relationship("Categoria", backref="solicitacoes")
    
    mensagens = db.relationship("Mensagem", backref="solicitacao", lazy='dynamic', cascade="all, delete-orphan")
    anexos = db.relationship("Anexo", backref="solicitacao", lazy='dynamic', cascade="all, delete-orphan")
    historicos = db.relationship("Historico", backref="solicitacao", lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Solicitacao {self.protocolo}>'
