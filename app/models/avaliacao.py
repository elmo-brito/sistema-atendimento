from app import db
from datetime import datetime

class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey('solicitacoes.id'), nullable=False, unique=True)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    solicitacao = db.relationship("Solicitacao", backref=db.backref("avaliacao", uselist=False))

    def __repr__(self):
        return f'<Avaliacao {self.nota} para Solicitacao {self.solicitacao_id}>'
