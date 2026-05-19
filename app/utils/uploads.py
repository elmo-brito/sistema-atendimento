import os
from flask import Blueprint, current_app, send_from_directory, flash, redirect, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename
from app import db
from app.models import Anexo, Mensagem

bp = Blueprint('utils', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

def save_anexo(file, solicitacao_id, mensagem_id=None):
    if file and allowed_file(file.filename):
        # RN006: 5MB limit
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        
        if size > 5 * 1024 * 1024:
            return False
            
        filename = secure_filename(file.filename)
        # Add timestamp to avoid collisions
        filename = f"{solicitacao_id}_{filename}"
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        anexo = Anexo(
            solicitacao_id=solicitacao_id,
            mensagem_id=mensagem_id,
            caminho=filename,
            tipo=file.content_type,
            tamanho=size
        )
        db.session.add(anexo)
        return True
    return False
