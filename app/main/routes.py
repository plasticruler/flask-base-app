from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from app import db

from app.main import bp,forms
from app.models import ExpenseType, Expense
from sqlalchemy import func




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
    return render_template('expensetype.html',form=form)

@bp.route('/expense',methods=['GET','POST'])
@login_required
def expense():
    form = forms.ExpenseForm()
    expensetypes = [(c.id,c.name) for c in ExpenseType.query.order_by('name')]
    form.expensetype_id.choices = expensetypes    
    last_10 = Expense.query.limit(10)    
    chart_data = db.session.query(Expense.expensetype_id,func.sum(Expense.price).label('sum_prices')).group_by(Expense.expensetype_id)    
    chart_data = [[str(ExpenseType.query.get(x[0]).name),float(x[1])] for x in chart_data] #can't get name otherwise?
    if form.validate_on_submit():
        ext = Expense(note=form.note.data, paid_date=form.paid_date.data,expensetype_id=int(form.expensetype_id.data), price=float(form.price.data), units=int(form.units.data))
        db.session.add(ext)
        db.session.commit()        
        flash("Expense recorded '{}'.".format(ext))        
    return render_template('expense.html',form=form,chart_data=chart_data, last_10=last_10)