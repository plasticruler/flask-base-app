from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from app import db
from app.main import bp,forms
from app.models import ExpenseType, Expense




@bp.route('/index', methods=['GET'])
@login_required
def index():        
    return render_template('index.html', title='welcome')

@bp.route('/expensetype',methods=['GET','POST'])
@login_required
def expensetype():
    form = forms.ExpenseTypeForm()
    if form.validate_on_submit():
        ext = ExpenseType(name=form.name.data)        
        db.session.add(ext)
        db.session.commit()
        flash("Expense type '{}' added.".format(form.name.data))        
    return render_template('expense.html',form=form)

@bp.route('/expense',methods=['GET','POST'])
@login_required
def expense():
    form = forms.ExpenseForm()
    expensetypes = [(c.id,c.name) for c in ExpenseType.query.order_by('name')]
    form.expensetype_id.choices = expensetypes
    if form.validate_on_submit():
        ext = Expense(expensetype_id=int(form.expensetype_id.data), price=float(form.price.data), units=int(form.units.data))
        db.session.add(ext)
        db.session.commit()
        flash("Expense recorded '{}'.".format(ext))        
    return render_template('expense.html',form=form)