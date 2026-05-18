from app import create_app, db
from app.models import Categoria, Subcategoria, Usuario, Solicitacao
from app.services.solicitacao_service import SolicitacaoService

def seed():
    app = create_app()
    with app.app_context():
        # Clear some data if needed, but let's just add
        
        # 1. Ensure categories and subcategories
        cat_infra = Categoria.query.filter_by(nome='Infraestrutura').first()
        if not cat_infra:
            cat_infra = Categoria(nome='Infraestrutura', descricao='Problemas de hardware, rede e servidores', prazo_horas=24)
            db.session.add(cat_infra)
            db.session.flush()
            
            sub1 = Subcategoria(nome='Rede/Internet', categoria_id=cat_infra.id)
            sub2 = Subcategoria(nome='Hardware/Desktop', categoria_id=cat_infra.id)
            db.session.add_all([sub1, sub2])

        cat_soft = Categoria.query.filter_by(nome='Software').first()
        if not cat_soft:
            cat_soft = Categoria(nome='Software', descricao='Problemas em sistemas e aplicativos', prazo_horas=48)
            db.session.add(cat_soft)
            db.session.flush()
            
            sub3 = Subcategoria(nome='ERP/Financeiro', categoria_id=cat_soft.id)
            sub4 = Subcategoria(nome='E-mail/Outlook', categoria_id=cat_soft.id)
            db.session.add_all([sub3, sub4])

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
