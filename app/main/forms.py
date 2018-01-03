from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, DateTimeField
from wtforms.validators import InputRequired, Email, Length, NumberRange
from custom_widgets import render_datetime_widget
#forms go here
class ExpenseTypeForm(FlaskForm):
    name = StringField('Name',validators=[InputRequired(),Length(min=4,max=15)])
    submit = SubmitField('Save')

class ExpenseForm(FlaskForm):
    expensetype_id = SelectField('Expense Type',choices=[],coerce=int)
    price = StringField('Price', validators=[InputRequired(), NumberRange(min=1)])
    units = StringField('Units purchases',validators=[InputRequired(),NumberRange(min=0.1)])    
    paid_date = DateTimeField('Paid Date', validators=[InputRequired()],format="%Y-%m-%d %H:%M:%S", widget=render_datetime_widget)
    note = StringField('Note')
    submit = SubmitField('Save')