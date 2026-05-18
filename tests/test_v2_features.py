import pytest
from datetime import datetime, timedelta, timezone
from app.models import Solicitacao, Categoria, Usuario, SLA
from app.services.solicitacao_service import SolicitacaoService
from app import db

def test_sla_calculo(app, auth_client):
    client, _ = auth_client
    
    with app.app_context():
        cat = Categoria(nome="Critico", prazo_horas=10)
        db.session.add(cat)
        db.session.commit()
        cat_id = cat.id

        service = SolicitacaoService()
        sol = service.criar_solicitacao(cliente_id=1, categoria_id=cat_id, titulo="Urgente", descricao="...")
        
        assert sol.prazo_sla is not None
        diff = sol.prazo_sla - datetime.now(timezone.utc).replace(tzinfo=None)
        assert 9.9 < diff.total_seconds() / 3600 < 10.1

def test_reabertura_regras(app, auth_client):
    client, cat_id = auth_client
    
    with app.app_context():
        sol = Solicitacao(
            protocolo="TEST-REOPEN",
            cliente_id=1,
            categoria_id=cat_id,
            titulo="Para reabrir",
            descricao="...",
            status="Resolvido"
        )
        db.session.add(sol)
        db.session.commit()
        sol_id = sol.id

        service = SolicitacaoService()

        # Reabrir com sucesso
        service.reabrir_solicitacao(sol_id, 1)
        assert sol.status == "Aberto"

        # Simular chamado fechado há mais de 7 dias
        sol.status = "Fechado"
        sol.atualizado_em = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=8)
        db.session.commit()
        
        with pytest.raises(ValueError, match="prazo para reabertura de 7 dias expirou"):
            service.reabrir_solicitacao(sol_id, 1)

def test_atribuicao_automatica(app):
    with app.app_context():
        # Criar atendentes
        a1 = Usuario(nome="Atendente 1", email="a1@test.com", perfil="atendente")
        a1.set_senha("123")
        a2 = Usuario(nome="Atendente 2", email="a2@test.com", perfil="atendente")
        a2.set_senha("123")
        db.session.add_all([a1, a2])

        # Cliente
        c1 = Usuario(nome="C1", email="c1@test.com", perfil="cliente")
        c1.set_senha("123")
        db.session.add(c1)

        cat = Categoria(nome="Geral", prazo_horas=24)
        db.session.add(cat)
        db.session.commit()

        service = SolicitacaoService()

        s1 = service.criar_solicitacao(c1.id, cat.id, "T1", "D1")
        assert s1.atendente_id in [a1.id, a2.id]
        
        s2 = service.criar_solicitacao(c1.id, cat.id, "T2", "D2")
        assert s2.atendente_id != s1.atendente_id
