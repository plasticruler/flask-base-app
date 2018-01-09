from flask import Blueprint
bp = Blueprint('crypto',__name__)
from app.crypto import routes