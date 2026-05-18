from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from app.services.auth_service import AuthService
from app.services.solicitacao_service import SolicitacaoService
from app.models import Solicitacao

bp = Blueprint('api', __name__, url_prefix='/api')
auth_service = AuthService()
solicitacao_service = SolicitacaoService()

def json_response(data=None, message=None, status="success", code=200):
    response = {
        "status": status,
        "message": message,
        "data": data
    }
    return jsonify(response), code

@bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        usuario = auth_service.register(
            nome=data.get('nome'),
            email=data.get('email'),
            senha=data.get('senha')
        )
        return json_response(
            data={"id": usuario.id, "email": usuario.email},
            message="Usuário criado com sucesso.",
            code=201
        )
    except ValueError as e:
        return json_response(status="error", message=str(e), code=400)

@bp.route('/auth/login', methods=['POST'])
def login():
    from flask_login import login_user
    data = request.get_json()
    usuario = auth_service.login(data.get('email'), data.get('senha'))
    if usuario:
        login_user(usuario)
        return json_response(data={"id": usuario.id, "email": usuario.email}, message="Login realizado.")
    return json_response(status="error", message="Credenciais inválidas.", code=401)

@bp.route('/solicitacoes', methods=['GET'])
@login_required
def get_solicitacoes():
    if current_user.perfil == 'cliente':
        solicitacoes = current_user.solicitacoes_criadas.all()
    else:
        solicitacoes = Solicitacao.query.all()
    
    data = [{
        "id": s.id,
        "protocolo": s.protocolo,
        "titulo": s.titulo,
        "status": s.status,
        "prazo_sla": s.prazo_sla.isoformat() if s.prazo_sla else None
    } for s in solicitacoes]
    
    return json_response(data=data)

@bp.route('/solicitacoes', methods=['POST'])
@login_required
def create_solicitacao():
    data = request.get_json()
    try:
        solicitacao = solicitacao_service.criar_solicitacao(
            cliente_id=current_user.id,
            categoria_id=data.get('categoria_id'),
            titulo=data.get('titulo'),
            descricao=data.get('descricao')
        )
        return json_response(
            data={"id": solicitacao.id, "protocolo": solicitacao.protocolo},
            message="Solicitação criada.",
            code=201
        )
    except Exception as e:
        return json_response(status="error", message=str(e), code=400)
