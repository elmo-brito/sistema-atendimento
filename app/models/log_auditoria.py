from app import db
from datetime import datetime

class LogAuditoria(db.Model):
    __tablename__ = 'logs_auditoria'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    acao = db.Column(db.String(100), nullable=False)
    tabela = db.Column(db.String(50))
    registro_id = db.Column(db.Integer)
    detalhes = db.Column(db.Text)
    ip = db.Column(db.String(45))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship("Usuario", backref="logs")

    def __repr__(self):
        return f'<LogAuditoria {self.acao}>'
