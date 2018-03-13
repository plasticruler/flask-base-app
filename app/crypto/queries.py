from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from sqlalchemy import func, desc
from app.crypto.models import *

def GetLastCoinPrices(coin_id,interval=5,recordlimit=10): #default is hour      
    result = CryptoInstrumentPriceMarketData.query.filter_by(cryptoinstrument_id=coin_id, interval=interval).order_by(desc('retreived_datetime')).limit(recordlimit).all()    
    return result
      