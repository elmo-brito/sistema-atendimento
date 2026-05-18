import csv
import io
from app.models import Solicitacao, SLA, LogAuditoria
from app.repositories.solicitacao_repository import SolicitacaoRepository

class ReportService:
    def __init__(self):
        self.sol_repo = SolicitacaoRepository()

    def get_dashboard_metrics(self):
        solicitacoes = self.sol_repo.get_all()
        total = len(solicitacoes)
        if total == 0:
            return {"total": 0, "mtta": 0, "mttr": 0}
            
        resolvidos = [s for s in solicitacoes if s.status in ['Resolvido', 'Fechado']]
        
        # MTTR (Mean Time To Resolve)
        mttr_total = 0
        for s in resolvidos:
            sla_log = SLA.query.filter_by(solicitacao_id=s.id).filter(SLA.resolvido_em != None).first()
            if sla_log and sla_log.resolvido_em:
                diff = sla_log.resolvido_em - s.criado_em
                mttr_total += diff.total_seconds()
            else:
                diff = s.atualizado_em - s.criado_em
                mttr_total += diff.total_seconds()
        
        avg_mttr = (mttr_total / len(resolvidos)) / 3600 if resolvidos else 0 # em horas
        
        # MTTA (Mean Time To Assign)
        mtta_total = 0
        atribuidos = 0
        for s in solicitacoes:
            log = LogAuditoria.query.filter_by(tabela='solicitacoes', registro_id=s.id, acao='atribuir_chamado').first()
            if log:
                diff = log.criado_em - s.criado_em
                mtta_total += diff.total_seconds()
                atribuidos += 1
        
        avg_mtta = (mtta_total / atribuidos) / 3600 if atribuidos else 0 # em horas
        
        return {
            "total": total,
            "resolvidos": len(resolvidos),
            "mtta": round(avg_mtta, 2),
            "mttr": round(avg_mttr, 2),
            "pendentes": total - len(resolvidos)
        }

    def gerar_csv_volumetria(self):
        solicitacoes = self.sol_repo.get_all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Protocolo', 'Cliente', 'Atendente', 'Categoria', 'Titulo', 'Status', 'Prioridade', 'SLA', 'Criado em'])
        
        for s in solicitacoes:
            writer.writerow([
                s.protocolo,
                s.cliente.nome,
                s.atendente.nome if s.atendente else 'N/A',
                s.categoria.nome,
                s.titulo,
                s.status,
                s.prioridade,
                s.prazo_sla.strftime('%Y-%m-%d %H:%M:%S') if s.prazo_sla else 'N/A',
                s.criado_em.strftime('%Y-%m-%d %H:%M:%S')
            ])
            
        return output.getvalue()
