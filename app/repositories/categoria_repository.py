from app.models import Categoria
from app.repositories.base import BaseRepository

class CategoriaRepository(BaseRepository):
    model = Categoria

    def get_by_nome(self, nome):
        return self.model.query.filter_by(nome=nome).first()
