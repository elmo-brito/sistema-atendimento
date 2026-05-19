from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Solicitacao, Categoria, Mensagem, Usuario
from app.services.solicitacao_service import SolicitacaoService
from app.utils.auth import role_required
from app import db
from datetime import datetime, timezone

bp = Blueprint('solicitacoes', __name__)
solicitacao_service = SolicitacaoService()

@bp.route('/minhas-solicitacoes')
@login_required
def lista_cliente():
    solicitacoes = current_user.solicitacoes_cliente.order_by(Solicitacao.criado_em.desc()).all()
    return render_template('solicitacoes/lista_cliente.html', solicitacoes=solicitacoes)

@bp.route('/atendimento')
@login_required
@role_required('atendente', 'admin')
def lista_atendente():
    args = request.args.to_dict()
    solicitacoes = solicitacao_service.repo.search(**args)
    categorias = Categoria.query.all()
    atendentes = Usuario.query.filter_by(perfil='atendente', ativo=True).all()
        
    return render_template('solicitacoes/lista_atendente.html', 
                           solicitacoes=solicitacoes, 
                           categorias=categorias,
                           atendentes=atendentes)

@bp.route('/solicitacao/nova', methods=['GET', 'POST'])
@login_required
def nova():
    categorias = Categoria.query.all()
    if request.method == 'POST':
        categoria_id = request.form.get('categoria_id')
        prioridade = request.form.get('prioridade', 'Média')
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        
        try:
            solicitacao = solicitacao_service.criar_solicitacao(
                cliente_id=current_user.id,
                categoria_id=categoria_id,
                prioridade=prioridade,
                titulo=titulo,
                descricao=descricao
            )
            
            # Anexos (RF007)
            from app.utils.uploads import save_anexo
            arquivos = request.files.getlist('anexos')
            
            # Criar mensagem inicial se houver anexos (ou sempre, para timeline)
            mensagem = Mensagem(solicitacao_id=solicitacao.id, usuario_id=current_user.id, mensagem=descricao)
            db.session.add(mensagem)
            db.session.flush()
            
            for file in arquivos:
                if file.filename:
                    save_anexo(file, solicitacao_id=solicitacao.id, mensagem_id=mensagem.id)
            
            db.session.commit()
            flash(f'Solicitação registrada com sucesso! Protocolo: {solicitacao.protocolo}', 'success')
            return redirect(url_for('solicitacoes.detalhes', id=solicitacao.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar solicitação: {str(e)}', 'error')
            
    return render_template('solicitacoes/nova.html', categorias=categorias)

@bp.route('/solicitacao/<int:id>')
@login_required
def detalhes(id):
    solicitacao = db.get_or_404(Solicitacao, id)
    
    # Restrição para clientes (RN007)
    if current_user.perfil == 'cliente' and solicitacao.cliente_id != current_user.id:
        flash('Você não tem permissão para ver este chamado.', 'error')
        return redirect(url_for('main.index'))
    
    atendentes = []
    if current_user.perfil in ['atendente', 'admin']:
        atendentes = Usuario.query.filter_by(perfil='atendente', ativo=True).all()
        
    return render_template('solicitacoes/detalhes.html', 
                           solicitacao=solicitacao, 
                           atendentes=atendentes,
                           now=datetime.now(timezone.utc).replace(tzinfo=None))

@bp.route('/solicitacao/<int:id>/responder', methods=['POST'])
@login_required
def responder(id):
    solicitacao = db.get_or_404(Solicitacao, id)
    
    if current_user.perfil == 'cliente' and solicitacao.cliente_id != current_user.id:
        flash('Acesso negado.', 'error')
        return redirect(url_for('main.index'))
    
    conteudo = request.form.get('mensagem')
    arquivos = request.files.getlist('anexos')
    
    if conteudo or (arquivos and arquivos[0].filename):
        novo_status = None
        if current_user.perfil in ['atendente', 'admin']:
            novo_status = request.form.get('status')
        elif solicitacao.status == 'Aguardando cliente':
            novo_status = 'Em atendimento'
            
        try:
            mensagem = solicitacao_service.responder_solicitacao(
                solicitacao_id=id,
                usuario_id=current_user.id,
                mensagem_texto=conteudo,
                novo_status=novo_status
            )
            
            from app.utils.uploads import save_anexo
            for file in arquivos:
                if file.filename:
                    save_anexo(file, solicitacao_id=solicitacao.id, mensagem_id=mensagem.id)
                    
            db.session.commit()
            flash('Resposta enviada com sucesso.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao enviar resposta: {str(e)}', 'error')
        
    return redirect(url_for('solicitacoes.detalhes', id=solicitacao.id))

@bp.route('/solicitacao/<int:id>/atribuir', methods=['POST'])
@login_required
@role_required('admin')
def atribuir(id):
    atendente_id = request.form.get('atendente_id')
    try:
        solicitacao_service.atribuir_solicitacao(id, atendente_id, current_user.id)
        flash('Chamado atribuído com sucesso.', 'success')
    except Exception as e:
        flash(f'Erro ao atribuir chamado: {str(e)}', 'error')
    return redirect(url_for('solicitacoes.detalhes', id=id))

@bp.route('/solicitacao/<int:id>/avaliar', methods=['POST'])
@login_required
def avaliar(id):
    nota = int(request.form.get('nota', 5))
    comentario = request.form.get('comentario')
    try:
        solicitacao_service.avaliar_solicitacao(id, current_user.id, nota, comentario)
        flash('Obrigado pela sua avaliação! O chamado foi encerrado.', 'success')
    except Exception as e:
        flash(f'Erro ao avaliar: {str(e)}', 'error')
    return redirect(url_for('solicitacoes.detalhes', id=id))

@bp.route('/solicitacao/<int:id>/reabrir', methods=['POST'])
@login_required
def reabrir(id):
    try:
        solicitacao_service.reabrir_solicitacao(id, current_user.id)
        flash('Chamado reaberto com sucesso.', 'success')
    except Exception as e:
        flash(f'Erro ao reabrir chamado: {str(e)}', 'error')
    return redirect(url_for('solicitacoes.detalhes', id=id))
