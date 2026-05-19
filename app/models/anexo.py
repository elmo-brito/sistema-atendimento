from app import db

class Anexo(db.Model):
    __tablename__ = 'anexos'
    
    id = db.Column(db.Integer, primary_key=True)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey('solicitacoes.id'), nullable=False)
    mensagem_id = db.Column(db.Integer, db.ForeignKey('mensagens.id'))
    caminho = db.Column(db.String(255), nullable=False)
    nome_original = db.Column(db.String(255))
    tipo = db.Column(db.String(50))
    tamanho = db.Column(db.Integer)

    def __repr__(self):
        return f'<Anexo {self.caminho}>'
