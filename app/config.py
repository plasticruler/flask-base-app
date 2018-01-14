import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
environment_supplement = 'dev.env' if os.environ.get('FLASK_DEBUG')=='1' else 'production.env' 
load_dotenv(os.path.join(basedir,environment_supplement))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db')    
    SQLALCHEMY_TRACK_MODIFICATIONS = False    
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO','1')=='1'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_SENDER')
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    ADMINS = [MAIL_DEFAULT_SENDER]
    LOGIN_VIEW = 'auth.login'
    DEBUG = os.environ.get('FLASK_DEBUG') or False
    RECORDS_PER_PAGE = 30
    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    @staticmethod
    def init_app(app):
        pass     
    

config = {
    'dev':DevConfig,    
    'default': DevConfig
}
