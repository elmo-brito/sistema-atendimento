from app.models import Categoria
from app.repositories.base import BaseRepository
from app import cache

class CategoriaRepository(BaseRepository):
    model = Categoria

    @cache.cached(timeout=300, key_prefix='all_categorias')
    def get_all(self):
        return super().get_all()

    @cache.memoize(timeout=300)
    def get_by_id(self, id):
        return super().get_by_id(id)

    def get_by_nome(self, nome):
        return self.model.query.filter_by(nome=nome).first()
