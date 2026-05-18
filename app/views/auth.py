from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.services.auth_service import AuthService

bp = Blueprint('auth', __name__, url_prefix='/')
auth_service = AuthService()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = auth_service.login(email, senha)

        if not usuario:
            flash('Email ou senha inválidos ou conta desativada.')
            return redirect(url_for('auth.login'))

        login_user(usuario)
        flash('Login realizado com sucesso!')
        
        if usuario.perfil == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif usuario.perfil == 'atendente':
            return redirect(url_for('solicitacoes.lista_atendente'))
        else:
            return redirect(url_for('solicitacoes.lista_cliente'))

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    logout_user()
    flash('Você saiu do sistema.')
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        try:
            auth_service.register(nome, email, senha)
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e))

    return render_template('auth/register.html')


@bp.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        if auth_service.recuperar_senha(email):
            flash('Se o e-mail existir, um link de recuperação foi enviado.')
        else:
            flash('Se o e-mail existir, um link de recuperação foi enviado.')
        return redirect(url_for('auth.login'))

    return render_template('auth/recuperar_senha.html')


@bp.route('/reset-senha/<token>', methods=['GET', 'POST'])
def reset_senha(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')
        try:
            auth_service.resetar_senha(token, nova_senha)
            flash('Senha redefinida com sucesso!')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e))

    return render_template('auth/reset_senha.html', token=token)


@bp.route('/alterar-senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    if request.method == 'POST':
        senha_atual = request.form.get('senha_atual')
        nova_senha = request.form.get('nova_senha')
        try:
            auth_service.alterar_senha(current_user.id, senha_atual, nova_senha)
            flash('Senha alterada com sucesso!')
            return redirect(url_for('main.index'))
        except ValueError as e:
            flash(str(e))

    return render_template('auth/alterar_senha.html')

