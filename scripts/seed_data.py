from app import create_app, db
from app.models import Categoria, Usuario, Solicitacao
from app.services.solicitacao_service import SolicitacaoService

def seed():
    app = create_app()
    with app.app_context():
        # 1. Ensure categories
        cat_infra = Categoria.query.filter_by(nome='Infraestrutura').first()
        if not cat_infra:
            cat_infra = Categoria(nome='Infraestrutura', descricao='Problemas de hardware, rede e servidores', prazo_horas=24)
            db.session.add(cat_infra)

        cat_soft = Categoria.query.filter_by(nome='Software').first()
        if not cat_soft:
            cat_soft = Categoria(nome='Software', descricao='Problemas em sistemas e aplicativos', prazo_horas=48)
            db.session.add(cat_soft)

        # 2. Ensure an attendant
        att = Usuario.query.filter_by(email='atendente@teste.com').first()
        if not att:
            att = Usuario(nome='Atendente Teste', email='atendente@teste.com', perfil='atendente')
            att.set_senha('123456')
            db.session.add(att)

        db.session.commit()
        print("Seed finalizado com sucesso!")

if __name__ == '__main__':
    seed()
