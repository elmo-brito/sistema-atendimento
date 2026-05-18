from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Usuario, Categoria, Solicitacao
from app.services.admin_service import AdminService
from app.utils.auth import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')
admin_service = AdminService()

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = admin_service.get_dashboard_stats()
    total_usuarios = Usuario.query.count()
    return render_template('admin/dashboard.html', 
                           stats=stats,
                           total_usuarios=total_usuarios)

@bp.route('/usuarios')
@login_required
@admin_required
def usuarios():
    usuarios = admin_service.listar_usuarios()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@bp.route('/usuario/<int:id>/perfil', methods=['POST'])
@login_required
@admin_required
def usuario_perfil(id):
    novo_perfil = request.form.get('perfil')
    try:
        admin_service.atualizar_perfil_usuario(id, novo_perfil)
        flash('Perfil do usuário atualizado com sucesso.')
    except Exception as e:
        flash(f'Erro ao atualizar perfil: {str(e)}', 'error')
    return redirect(url_for('admin.usuarios'))

@bp.route('/categorias', methods=['GET', 'POST'])
@login_required
@admin_required
def categorias():
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        prazo_horas = int(request.form.get('prazo_horas', 48))
        try:
            admin_service.criar_categoria(nome, descricao, prazo_horas)
            flash('Categoria adicionada com sucesso.')
        except Exception as e:
            flash(f'Erro ao criar categoria: {str(e)}', 'error')
        return redirect(url_for('admin.categorias'))
    
    categorias = Categoria.query.all()
    return render_template('admin/categorias.html', categorias=categorias)

@bp.route('/categoria/<int:id>/edit', methods=['POST'])
@login_required
@admin_required
def editar_categoria(id):
    prazo_horas = int(request.form.get('prazo_horas'))
    descricao = request.form.get('descricao')
    try:
        admin_service.atualizar_categoria(id, prazo_horas=prazo_horas, descricao=descricao)
        flash('Categoria atualizada com sucesso.')
    except Exception as e:
        flash(f'Erro ao atualizar categoria: {str(e)}', 'error')
    return redirect(url_for('admin.categorias'))
