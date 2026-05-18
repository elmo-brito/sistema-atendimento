from datetime import datetime, timezone
from app.models import LogAuditoria
from app import db
import json

class AuditService:
    @staticmethod
    def log(usuario_id, acao, tabela=None, registro_id=None, dados_anteriores=None, dados_novos=None, detalhes=None, ip=None, user_agent=None):
        log = LogAuditoria(
            usuario_id=usuario_id,
            acao=acao,
            tabela=tabela,
            registro_id=registro_id,
            dados_anteriores=json.dumps(dados_anteriores) if dados_anteriores else None,
            dados_novos=json.dumps(dados_novos) if dados_novos else None,
            detalhes=detalhes,
            ip=ip,
            user_agent=user_agent
        )
        db.session.add(log)
        db.session.commit()
        return log
