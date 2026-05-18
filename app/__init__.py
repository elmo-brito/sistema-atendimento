from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Por favor, faça login para acessar esta página.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.views import auth, main, solicitacoes, admin, api, reports
    from app.utils import uploads
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(solicitacoes.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(reports.bp)
    app.register_blueprint(uploads.bp)

    import os
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    import logging
    from logging.handlers import RotatingFileHandler
    import os

    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Evita criar o log como root durante migrações
    if not os.environ.get("FLASK_MIGRATE"):
        file_handler = RotatingFileHandler('logs/sistema.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Sistema startup')

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f'Server Error: {error}')
        import traceback
        app.logger.error(traceback.format_exc())
        return "Internal Server Error", 500

    return app

from app import models
