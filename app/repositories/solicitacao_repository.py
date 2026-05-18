from app.models import Solicitacao
from app.repositories.base import BaseRepository

class SolicitacaoRepository(BaseRepository):
    model = Solicitacao

    def get_by_protocolo(self, protocolo):
        return self.model.query.filter_by(protocolo=protocolo).first()

    def get_by_cliente(self, cliente_id):
        return self.model.query.filter_by(cliente_id=cliente_id).all()

    def search(self, **kwargs):
        query = self.model.query
        
        if kwargs.get('status'):
            query = query.filter_by(status=kwargs['status'])
        if kwargs.get('categoria_id'):
            query = query.filter_by(categoria_id=kwargs['categoria_id'])
        if kwargs.get('atendente_id'):
            query = query.filter_by(atendente_id=kwargs['atendente_id'])
        if kwargs.get('prioridade'):
            query = query.filter_by(prioridade=kwargs['prioridade'])
        if kwargs.get('busca'):
            search = f"%{kwargs['busca']}%"
            query = query.filter(Solicitacao.titulo.ilike(search) | Solicitacao.descricao.ilike(search) | Solicitacao.protocolo.ilike(search))
            
        return query.order_by(Solicitacao.atualizado_em.desc()).all()
