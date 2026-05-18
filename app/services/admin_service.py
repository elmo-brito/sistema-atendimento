from app.models import Usuario, Solicitacao, Categoria, SLA
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.solicitacao_repository import SolicitacaoRepository
from sqlalchemy import func
from app import db
from datetime import datetime

class AdminService:
    def __init__(self):
        self.user_repo = UsuarioRepository()
        self.cat_repo = CategoriaRepository()
        self.sol_repo = SolicitacaoRepository()

    def get_dashboard_stats(self):
        try:
            total_chamados = self.sol_repo.model.query.count()
            chamados_abertos = self.sol_repo.model.query.filter(Solicitacao.status.in_(['Aberto', 'Em atendimento', 'Aguardando cliente', 'Aguardando terceiros'])).count()
            
            total_resolvidos_sla = SLA.query.filter(SLA.resolvido_em != None).count()
            sla_cumpridos = SLA.query.filter(SLA.cumprido == True).count()
            sla_taxa = (sla_cumpridos / total_resolvidos_sla * 100) if total_resolvidos_sla > 0 else 100

            stats_status = db.session.query(Solicitacao.status, func.count(Solicitacao.id)).group_by(Solicitacao.status).all()
            status_dict = {s[0]: s[1] for s in stats_status} if stats_status else {}
            
            from app.services.report_service import ReportService
            report_service = ReportService()
            metrics = report_service.get_dashboard_metrics()
            
            return {
                'total_chamados': total_chamados,
                'chamados_abertos': chamados_abertos,
                'sla_compliance': round(sla_taxa, 2),
                'status_dist': status_dict,
                'mttr': metrics.get('mttr', 0),
                'mtta': metrics.get('mtta', 0)
            }
        except Exception as e:
            print(f"Error in get_dashboard_stats: {str(e)}")
            return {
                'total_chamados': 0,
                'chamados_abertos': 0,
                'sla_compliance': 0,
                'status_dist': {}
            }

    def listar_usuarios(self):
        return Usuario.query.all()

    def get_usuario(self, user_id):
        return Usuario.query.get(user_id)

    def atualizar_perfil_usuario(self, user_id, novo_perfil):
        user = Usuario.query.get(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")
        if novo_perfil not in ['cliente', 'atendente', 'admin']:
            raise ValueError("Perfil inválido.")
        user.perfil = novo_perfil
        db.session.commit()
        return user

    def criar_categoria(self, nome, descricao, prazo_horas):
        cat = Categoria(nome=nome, descricao=descricao, prazo_horas=prazo_horas)
        db.session.add(cat)
        db.session.commit()
        return cat

    def atualizar_categoria(self, cat_id, **kwargs):
        cat = Categoria.query.get(cat_id)
        if not cat:
            raise ValueError("Categoria não encontrada.")
        for key, value in kwargs.items():
            if hasattr(cat, key):
                setattr(cat, key, value)
        db.session.commit()
        return cat
