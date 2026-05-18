from app import create_app, db
from app.models import Usuario, Solicitacao, Historico

app = create_app()
with app.app_context():
    print("Checking for NULL criado_em...")
    users = Usuario.query.filter(Usuario.criado_em == None).all()
    print(f"Users with NULL criado_em: {len(users)}")
    
    sols = Solicitacao.query.filter(Solicitacao.criado_em == None).all()
    print(f"Solicitacoes with NULL criado_em: {len(sols)}")
    
    sols_upd = Solicitacao.query.filter(Solicitacao.atualizado_em == None).all()
    print(f"Solicitacoes with NULL atualizado_em: {len(sols_upd)}")
    
    hist = Historico.query.filter(Historico.criado_em == None).all()
    print(f"Historico with NULL criado_em: {len(hist)}")
