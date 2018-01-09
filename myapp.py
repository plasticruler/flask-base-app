from app import create_app, db
from app.models import User, Expense, ExpenseType
from app.crypto.models import CryptoExchange, CryptoInstrument, ProviderTransactionRequest
from flask_migrate import Migrate
import os

from celery import Celery
import click
from app.utils import DownloadURL
from app.provider_tracking import PTR

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app,db)

@app.cli.command('dl')
def download():
    url = 'http://wttr.in/cape%20town'
    ptr = PTR(1, 909, url,app=app)
    #we'll push this onto a task queue after reading the params from cmd line
    u = DownloadURL(url,ptr=ptr)
    g = u()


@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User': User,'Expense':Expense, 'ExpenseType':ExpenseType, 'CryptoExchange':CryptoExchange}