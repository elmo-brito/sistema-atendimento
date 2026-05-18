from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if current_user.perfil not in roles and current_user.perfil != 'admin':
                flash('Você não tem permissão para acessar esta página.', 'error')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.perfil != 'admin':
            flash('Acesso restrito a administradores.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function
