from app import create_app, db
from app.models import Papel, Permissao, Usuario

def seed_rbac():
    app = create_app()
    with app.app_context():
        # 1. Permissões
        permissoes = [
            ('Gerenciar usuários', 'gerenciar_usuarios'),
            ('Gerenciar papéis', 'gerenciar_papeis'),
            ('Gerenciar permissões', 'gerenciar_permissoes'),
            ('Gerenciar categorias', 'gerenciar_categorias'),
            ('Gerenciar subcategorias', 'gerenciar_subcategorias'),
            ('Gerenciar SLA', 'gerenciar_sla'),
            ('Gerenciar chamados', 'gerenciar_chamados'),
            ('Ver chamados', 'ver_chamados'),
            ('Reatribuir chamados', 'reatribuir_chamados'),
            ('Criar comentários internos', 'criar_comentarios_internos'),
            ('Criar comentários externos', 'criar_comentarios_externos'),
            ('Ver auditoria', 'ver_auditoria'),
            ('Exportar relatórios', 'exportar_relatorios'),
            ('Gerenciar configurações globais', 'gerenciar_configuracoes_globais'),
        ]

        perm_objs = {}
        for nome, slug in permissoes:
            perm = Permissao.query.filter_by(slug=slug).first()
            if not perm:
                perm = Permissao(nome=nome, slug=slug)
                db.session.add(perm)
            perm_objs[slug] = perm
        
        db.session.commit()

        # 2. Papéis
        all_slugs = [p[1] for p in permissoes]
        papeis = {
            'Administrador': all_slugs,
            'Supervisor': [
                'ver_chamados', 'gerenciar_chamados', 'reatribuir_chamados', 
                'criar_comentarios_internos', 'criar_comentarios_externos', 
                'ver_auditoria', 'exportar_relatorios', 'gerenciar_sla'
            ],
            'Atendente': [
                'ver_chamados', 'gerenciar_chamados', 
                'criar_comentarios_internos', 'criar_comentarios_externos'
            ],
            'Cliente': [
                'ver_chamados', 'criar_comentarios_externos'
            ],
            'Auditor': [
                'ver_chamados', 'ver_auditoria', 'exportar_relatorios'
            ],
            'Gestor de SLA': [
                'gerenciar_sla', 'exportar_relatorios'
            ],
            'Gestor de Categorias': [
                'gerenciar_categorias', 'gerenciar_subcategorias'
            ],
            'Gestor de Usuários': [
                'gerenciar_usuarios'
            ]
        }

        for nome_papel, slugs in papeis.items():
            papel = Papel.query.filter_by(nome=nome_papel).first()
            if not papel:
                papel = Papel(nome=nome_papel)
                db.session.add(papel)
            
            # Atualizar permissões
            papel.permissoes = [perm_objs[slug] for slug in slugs]
        
        db.session.commit()

        # 3. Atribuir Admin ao primeiro usuário se existir
        admin_user = Usuario.query.filter_by(email='admin@example.com').first()
        if not admin_user:
            admin_user = Usuario(nome='Administrador', email='admin@example.com', perfil='admin')
            admin_user.set_senha('admin123')
            db.session.add(admin_user)
            db.session.commit()
        
        admin_role = Papel.query.filter_by(nome='Administrador').first()
        if admin_role not in admin_user.papeis:
            admin_user.papeis.append(admin_role)
            db.session.commit()

        print("RBAC seeded successfully!")

if __name__ == '__main__':
    seed_rbac()
