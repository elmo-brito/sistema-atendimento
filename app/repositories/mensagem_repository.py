from app.models import Mensagem
from app.repositories.base import BaseRepository

class MensagemRepository(BaseRepository):
    model = Mensagem

    def get_by_solicitacao(self, solicitacao_id):
        return self.model.query.filter_by(solicitacao_id=solicitacao_id).order_by(Mensagem.criado_em.asc()).all()
