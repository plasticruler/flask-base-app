from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from flask_paginate import Pagination, get_page_args

from app import db
from app.config import *
from app.crypto import bp
from app.crypto.forms import *

from app.crypto.models import *
from sqlalchemy import func, desc

from flask import current_app as app


@bp.route('/exchange', methods=['GET', 'POST'])
@login_required
def exchange():
    form = CryptoExchangeForm()
    if form.validate_on_submit():
        ex = CryptoExchange()
        ex.name = form.name.data
        ex.url = form.url.data
        db.session.add(ex)
        db.session.add(ex)        
        flash('Exchange {} added'.format(ex.name))
        form = CryptoExchangeForm()
    return render_template('crypto/exchange.html', form = form)

@bp.route('/cryptoinstrument',methods=['GET','POST'])
@login_required
def cryptoinstrument():
    form = CryptoInstrumentForm()

    search = False

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 10 #int(app.config['RECORDS_PER_PAGE']) 
    data = CryptoInstrument.query.order_by('name').offset((page-1)*per_page).limit(per_page)
    data_count = CryptoInstrument.query.count()     
    
    pagination = Pagination(bs_version=3, per_page_parameter='per_page', page = page, total = data_count, search = search, record_name = 'cryptoinstrument')

    return render_template('crypto/cryptocoin.html', data=data, pagination=pagination)

@bp.route('/currency', methods=['GET','POST'])
@login_required
def fiatcurrency():
    form = CryptoFiatCurrencyForm()
    if form.validate_on_submit():
        c = Currency()
        c.name = form.name.data
        c.symbol = form.code.data
        db.session.add(c)
        db.session.commit()
        form = CryptoFiatCurrencyForm()
        flash('New currency added {} ({}).'.format(c.name, c.symbol))        
    return render_template('crypto/currency.html', form=form, currencies=Currency.query.order_by('name'))


@bp.route('/dataprovidersourceurl', methods=['GET','POST'])
@login_required
def dataprovidersourceurl():
    form = DataProviderSourceURLForm()
    providers = [(c.id,c.name) for c in DataProvider.query.order_by('name')]
    form.dataprovider_id.choices = providers
    auth_methods = []
    auth_methods.append((-1,'Make a selection'))
    auth_methods.append((0,'http-basic-auth')) 
    form.auth_method.choices = auth_methods
    message_types = [(c.id, c.name) for c in MessageType.query.order_by('name')]
    form.messagetype_id.choices = message_types    
    if form.validate_on_submit():
        dps = DataProviderSourceUrl()
        dps.description = form.description.data
        dps.url = form.url.data
        dps.dataprovider_id = int(form.dataprovider_id.data)
        dps.auth_method = int(form.auth_method.data)
        dps.auth_password = form.auth_password.data
        dps.auth_user = form.auth_user.data
        dps.messagetype_id = int(form.messagetype_id.data)
        db.session.add(dps)
        db.session.commit()
        flash('Source url added.')
    return render_template('crypto/dataprovidersourceurl.html', form=form, provider_sources= DataProviderSourceUrl.query.all())

@bp.route('/messagetype', methods=['GET','POST'])
@login_required
def messagetype():
    form = MessageTypeForm()
    providers = [(c.id,c.name) for c in DataProvider.query.order_by('name')]
    form.dataprovider_id.choices = providers
    if form.validate_on_submit():
        m = MessageType()
        m.description = form.description.data
        m.name = form.name.data
        db.session.add(m)
        db.session.commit()
        flash('Message type added.')
        form = MessageTypeForm()
    return render_template('crypto/messagetype.html',form=form, providers=providers, message_types=MessageType.query.order_by('name'))

@bp.route('/dataprovider', methods=['GET','POST'])
@login_required
def dataprovider():
    form = DataProviderForm()
    
    if form.validate_on_submit():
        dp = DataProvider()
        dp.name = form.name.data
        db.session.add(dp)
        db.session.commit()
        form = DataProviderForm()
        flash('New data provider {} added.'.format(dp.name))
    return render_template('crypto/dataprovider.html', form=form, providers = DataProvider.query.order_by('name'))
