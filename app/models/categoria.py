from app import db

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(200))
    # Note: refactor.md mentions 'icone', 'cor', 'ativo' were added/removed? 
    # Let's check the migration 3a34acbc7db8_overhaul_schema_v2.py for latest Categorias fields.
    icone = db.Column(db.String(50))
    cor = db.Column(db.String(20))
    ativo = db.Column(db.Boolean, default=True)
    prazo_horas = db.Column(db.Integer, default=48)

    def __repr__(self):
        return f'<Categoria {self.nome}>'
