import logging
import os
from flask import Flask
from logging.handlers import RotatingFileHandler

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login.login'
login_manager.login_message = ('Please log in to access this page.')
bootstrap = Bootstrap()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)


    # Initialize Extensions

    # Register Blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.login import bp as login_bp
    app.register_blueprint(login_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.checkin import bp as checkin_bp
    app.register_blueprint(checkin_bp)

    from app.availability import bp as availability_bp
    app.register_blueprint(availability_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    # Logging
    if not app.debug and not app.config['TESTING']:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log',
                                           maxBytes=app.config['MAX_LOG_SIZE'],
                                           backupCount=app.config['MAX_LOGS'])

        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('App Startup')

    return app

from app import models