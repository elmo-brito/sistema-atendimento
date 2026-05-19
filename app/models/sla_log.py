from app import db
from datetime import datetime

class SLA(db.Model):
    __tablename__ = 'sla_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey('solicitacoes.id'), nullable=False)
    vencimento = db.Column(db.DateTime, nullable=False)
    cumprido = db.Column(db.Boolean, default=False)
    resolvido_em = db.Column(db.DateTime)

    solicitacao = db.relationship("Solicitacao", backref="sla_logs")

    def __repr__(self):
        return f'<SLA {self.id}>'
