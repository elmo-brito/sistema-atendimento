from app import db
from datetime import datetime

class Artigo(db.Model):
    __tablename__ = 'artigos'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    categoria = db.relationship("Categoria", backref="artigos")

    def __repr__(self):
        return f'<Artigo {self.titulo}>'
