from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from app import db

from app.crypto import bp, forms

from app.crypto.models import CryptoExchange, CryptoInstrument,CryptoFiatCurrency, DataProvider
from sqlalchemy import func, desc


@bp.route('/exchange', methods=['GET', 'POST'])
@login_required
def exchange():
    form = forms.CryptoExchangeForm()
    if form.validate_on_submit():
        ex = CryptoExchange()
        ex.name = form.name.data
        ex.url = form.url.data
        db.session.add(ex)
        db.session.add(ex)
    return render_template('crypto/exchange.html', form = form)

@bp.route('/currency', methods=['GET','POST'])
@login_required
def fiatcurrency():
    form = forms.CryptoFiatCurrencyForm()
    if form.validate_on_submit():
        c = CryptoFiatCurrency()
        c.name = form.name.data
        c.code = form.code.data
        db.session.add(c)
        db.session.commit()
        flash('New currency added {} ({})'.format(c.name, c.code))        
    return render_template('crypto/currency.html', form=form)

@bp.route('/dataprovider', methods=['GET','POST'])
@login_required
def dataprovider():
    form = forms.DataProviderForm()
    if form.validate_on_submit():
        pass
    return render_template('crypto/dataprovider.html', form=form)
