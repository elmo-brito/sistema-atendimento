from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from app.models import Solicitacao, Categoria, Mensagem, Usuario


bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')
    
    if current_user.perfil == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif current_user.perfil == 'atendente':
        return redirect(url_for('solicitacoes.lista_atendente'))
    else:
        return redirect(url_for('solicitacoes.lista_cliente'))

@bp.route('/base-conhecimento')
def base_conhecimento():
    query = request.args.get('q')
    if query:
        artigos = Artigo.query.filter(Artigo.titulo.contains(query) | Artigo.conteudo.contains(query)).all()
    else:
        artigos = Artigo.query.all()
    return render_template('base_conhecimento.html', artigos=artigos, query=query)
