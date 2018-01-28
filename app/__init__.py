import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, Blueprint
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
import chartkick
import logging
from logging.handlers import SMTPHandler
from flask_bootstrap import Bootstrap, WebCDN


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
bootstrap = Bootstrap()


def create_app(config_name='dev'):
    app = Flask(__name__, static_folder='./static')
    config[config_name].init_app(app)

    app.config.from_object(config[config_name])  
    
    db.init_app(app)   

    bootstrap.init_app(app)
    app.extensions['bootstrap']['cdns']['jquery'] = WebCDN('//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/')
    mail.init_app(app)
    login.init_app(app)    
    logging.basicConfig(format='%(asctime)s %(message)s')


    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp,url_prefix='/error')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.crypto import bp as crypto_bp
    app.register_blueprint(crypto_bp, url_prefix='/crypto')

    #chartkick specific
    ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
    app.register_blueprint(ck, url_prefix='/ck')
    app.jinja_env.add_extension("chartkick.ext.charts")
    
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler( \
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']), \
                fromaddr='no-reply@' + app.config['MAIL_SERVER'], \
                toaddrs=app.config['ADMINS'], subject='Application Failure', \
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)        
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/application.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

    #sqlalchemy sqlengine logging
    if app.config['SQLALCHEMY_ECHO']:
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    
    
    app.logger.setLevel(logging.DEBUG)    
        
    app.logger.info('Application startup')

    return app
