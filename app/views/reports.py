from flask import Blueprint, Response, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from app.services.report_service import ReportService

bp = Blueprint('reports', __name__, url_prefix='/reports')
report_service = ReportService()

@bp.before_request
@login_required
def check_admin_or_atendente():
    if current_user.perfil not in ['admin', 'atendente']:
        flash('Acesso negado.')
        return redirect(url_for('main.index'))

@bp.route('/dashboard')
def dashboard():
    metrics = report_service.get_dashboard_metrics()
    return render_template('reports/dashboard.html', metrics=metrics)

@bp.route('/export/volumetria')
def export_volumetria():
    csv_data = report_service.gerar_csv_volumetria()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=relatorio_volumetria.csv"}
    )
