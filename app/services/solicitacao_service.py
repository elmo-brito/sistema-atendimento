import uuid
from datetime import timedelta
from app.repositories.solicitacao_repository import SolicitacaoRepository
from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.models import Solicitacao, Mensagem, Anexo, SLA, LogAuditoria, Avaliacao
from app.utils.datetime_utils import utc_now
from app import db

class SolicitacaoService:
    def __init__(self):
        self.repo = SolicitacaoRepository()
        self.cat_repo = CategoriaRepository()
        self.user_repo = UsuarioRepository()

    def criar_solicitacao(self, cliente_id, categoria_id, titulo, descricao, prioridade='Média'):
        categoria = self.cat_repo.get_by_id(categoria_id)
        if not categoria:
            raise ValueError("Categoria não encontrada.")

        # Gerar protocolo: ANO-HASH (RF004)
        agora = utc_now()
        protocolo = f"{agora.year}-{uuid.uuid4().hex[:6].upper()}"
        
        # Calcular SLA (RN001, RN002)
        prazo_horas = categoria.prazo_horas if categoria.prazo_horas else 48
        prazo_sla = agora + timedelta(hours=prazo_horas)
        
        # Atribuição Automática (RF004)
        atendente = self.user_repo.get_least_busy_atendente()
        atendente_id = atendente.id if atendente else None
        status = 'Em atendimento' if atendente_id else 'Aberto'

        solicitacao = self.repo.create(
            protocolo=protocolo,
            cliente_id=cliente_id,
            atendente_id=atendente_id,
            categoria_id=categoria_id,
            titulo=titulo,
            descricao=descricao,
            status=status,
            prazo_sla=prazo_sla,
            prioridade=prioridade
        )
        
        # Registrar log de SLA inicial
        sla_log = SLA(
            solicitacao_id=solicitacao.id,
            vencimento=prazo_sla
        )
        db.session.add(sla_log)

        # Log de Auditoria (RF019)
        log = LogAuditoria(
            usuario_id=cliente_id,
            acao='criar_chamado',
            tabela='solicitacoes',
            registro_id=solicitacao.id,
            detalhes=f'Chamado criado com protocolo {protocolo}'
        )
        db.session.add(log)
        db.session.commit()
        
        return solicitacao

    def reabrir_solicitacao(self, solicitacao_id, usuario_id):
        solicitacao = self.repo.get_by_id(solicitacao_id)
        if not solicitacao:
            raise ValueError("Solicitação não encontrada.")
        
        if solicitacao.status not in ['Resolvido', 'Fechado']:
            raise ValueError("Somente solicitações resolvidas ou fechadas podem ser reabertas.")
        
        # Regra de 7 dias (RN004)
        agora = utc_now()
        if solicitacao.atualizado_em < agora - timedelta(days=7):
            raise ValueError("O prazo para reabertura de 7 dias expirou.")
        
        solicitacao.status = 'Aberto'
        
        # Novo ciclo de SLA (RN001)
        prazo_horas = solicitacao.categoria.prazo_horas if solicitacao.categoria.prazo_horas else 48
        solicitacao.prazo_sla = agora + timedelta(hours=prazo_horas)
        
        self.repo.update(solicitacao)
        
        # Novo log de SLA
        sla_log = SLA(
            solicitacao_id=solicitacao.id,
            vencimento=solicitacao.prazo_sla
        )
        db.session.add(sla_log)

        log = LogAuditoria(
            usuario_id=usuario_id,
            acao='reabrir_chamado',
            tabela='solicitacoes',
            registro_id=solicitacao.id
        )
        db.session.add(log)
        db.session.commit()
        
        return solicitacao

    def responder_solicitacao(self, solicitacao_id, usuario_id, mensagem_texto, novo_status=None):
        solicitacao = self.repo.get_by_id(solicitacao_id)
        if not solicitacao:
            raise ValueError("Solicitação não encontrada.")
        
        mensagem = Mensagem(
            solicitacao_id=solicitacao.id,
            usuario_id=usuario_id,
            mensagem=mensagem_texto or "Atualização de status"
        )
        db.session.add(mensagem)

        if novo_status and novo_status != solicitacao.status:
            solicitacao.status = novo_status
            
            if novo_status == 'Resolvido':
                sla_log = SLA.query.filter_by(solicitacao_id=solicitacao.id).order_by(SLA.vencimento.desc()).first()
                if sla_log and not sla_log.resolvido_em:
                    agora = utc_now()
                    sla_log.resolvido_em = agora
                    sla_log.cumprido = agora <= sla_log.vencimento
                    db.session.add(sla_log)

            self.repo.update(solicitacao)
            
            log = LogAuditoria(
                usuario_id=usuario_id,
                acao='alterar_status',
                tabela='solicitacoes',
                registro_id=solicitacao.id,
                detalhes=f'Status alterado para {novo_status}'
            )
            db.session.add(log)
        
        db.session.commit()
        return mensagem

    def atribuir_solicitacao(self, solicitacao_id, atendente_id, usuario_id_executor):
        solicitacao = self.repo.get_by_id(solicitacao_id)
        if not solicitacao:
            raise ValueError("Solicitação não encontrada.")
            
        solicitacao.atendente_id = atendente_id
        if solicitacao.status == 'Aberto':
            solicitacao.status = 'Em atendimento'
            
        self.repo.update(solicitacao)
        
        log = LogAuditoria(
            usuario_id=usuario_id_executor,
            acao='atribuir_chamado',
            tabela='solicitacoes',
            registro_id=solicitacao.id,
            detalhes=f'Chamado atribuído ao usuário {atendente_id}'
        )
        db.session.add(log)
        db.session.commit()
        return solicitacao

    def encerrar_automaticamente(self):
        # Chamados em "Aguardando cliente" por mais de 5 dias (RN005)
        limite = utc_now() - timedelta(days=5)
        solicitacoes = self.repo.model.query.filter_by(status='Aguardando cliente')\
            .filter(Solicitacao.atualizado_em < limite).all()
        
        count = 0
        for s in solicitacoes:
            s.status = 'Fechado'
            log = LogAuditoria(
                usuario_id=None,
                acao='encerramento_automatico',
                tabela='solicitacoes',
                registro_id=s.id
            )
            db.session.add(log)
            count += 1
        
        db.session.commit()
        return count

    def avaliar_solicitacao(self, solicitacao_id, usuario_id, nota, comentario=None):
        solicitacao = self.repo.get_by_id(solicitacao_id)
        if not solicitacao:
            raise ValueError("Solicitação não encontrada.")
        if solicitacao.cliente_id != usuario_id:
            raise ValueError("Apenas o cliente pode avaliar.")
        
        # RN006: A avaliação só pode ser feita uma vez por chamado "Resolvido"
        if solicitacao.status != 'Resolvido':
             raise ValueError("Apenas chamados resolvidos podem ser avaliados.")
        
        if Avaliacao.query.filter_by(solicitacao_id=solicitacao_id).first():
            raise ValueError("Este chamado já foi avaliado.")
            
        avaliacao = Avaliacao(solicitacao_id=solicitacao_id, nota=nota, comentario=comentario)
        db.session.add(avaliacao)
        
        solicitacao.status = 'Fechado'
        db.session.commit()
        return avaliacao
