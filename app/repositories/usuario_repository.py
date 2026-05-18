from app.models import Usuario, Solicitacao
from app.repositories.base import BaseRepository
from sqlalchemy import func
from app import db

class UsuarioRepository(BaseRepository):
    model = Usuario

    def get_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def get_atendentes(self):
        return self.model.query.filter_by(perfil='atendente', ativo=True).all()

    def get_least_busy_atendente(self):
        # Subquery to count active solicitations per atendente
        active_counts = db.session.query(
            Solicitacao.atendente_id,
            func.count(Solicitacao.id).label('count')
        ).filter(Solicitacao.status.in_(['Aberto', 'Em atendimento', 'Aguardando cliente', 'Aguardando terceiros']))\
         .group_by(Solicitacao.atendente_id).subquery()

        # Join with Usuario and sort by count
        atendente = db.session.query(Usuario).filter(
            Usuario.perfil == 'atendente',
            Usuario.ativo == True
        ).outerjoin(active_counts, Usuario.id == active_counts.c.atendente_id)\
            .order_by(active_counts.c.count.asc().nullsfirst(), Usuario.id.asc())\
            .first()
        
        return atendente
