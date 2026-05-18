import pytest
from app.models import Usuario, Categoria, Solicitacao
from datetime import datetime, timedelta, timezone

def test_criar_solicitacao_protocolo_e_sla(auth_client):
    client, cat_id = auth_client
    
    response = client.post('/solicitacao/nova', data={
        'categoria_id': cat_id,
        'titulo': 'Problema teste',
        'descricao': 'Descricao do problema'
    }, follow_redirects=True)
    
    assert b'Solicita\xc3\xa7\xc3\xa3o registrada com sucesso' in response.data
    
    with client.application.app_context():
        solicitacao = Solicitacao.query.first()
        assert solicitacao is not None
        assert solicitacao.protocolo.startswith(str(datetime.now().year))
        assert solicitacao.prazo_sla is not None
        # Check if SLA is approx 48h from now (default)
        assert solicitacao.prazo_sla > datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=47)

def test_upload_arquivo(auth_client, app):
    client, cat_id = auth_client
    import io
    
    # Create a dummy file
    data = {
        'categoria_id': cat_id,
        'titulo': 'Problema com anexo',
        'descricao': 'Veja o anexo',
        'anexos': (io.BytesIO(b"conteudo do arquivo"), 'teste.txt')
    }
    
    response = client.post('/solicitacao/nova', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b'Solicita\xc3\xa7\xc3\xa3o registrada com sucesso' in response.data
    
    with app.app_context():
        from app.models import Anexo
        anexo = Anexo.query.first()
        assert anexo is not None
        assert 'teste.txt' in anexo.caminho
