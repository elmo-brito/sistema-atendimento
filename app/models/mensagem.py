from app import db
from datetime import datetime

class Mensagem(db.Model):
    __tablename__ = 'mensagens'
    
    id = db.Column(db.Integer, primary_key=True)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey('solicitacoes.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    autor = db.relationship("Usuario", backref="mensagens")
    anexos = db.relationship("Anexo", backref="mensagem", lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Mensagem {self.id}>'
