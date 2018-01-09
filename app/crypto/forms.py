from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo,Length, ValidationError

class CryptoExchangeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=3)])
    url = StringField('Url', validators=[DataRequired(),Length(min=10)])
    active = BooleanField('Is Active')
    submit = SubmitField('Save')

class CryptoFiatCurrencyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5)])
    code = StringField('Display Code', validators=[DataRequired(),Length(min=3,max=3)])
    submit = SubmitField('Save')

class CryptoInstrumentForm(FlaskForm):
    name = StringField('Currency Name', validators=[DataRequired(),Length(min=5)])
    code = StringField('Display Code', validators=[DataRequired(),Length(min=3,max=3)])
    note = StringField('Note')
    active = BooleanField('Is Active')
    submit = SubmitField('Save')


class DataProviderForm(FlaskForm):
    name = StringField('Provider Name', validators=[DataRequired, Length(min=5)])
    auth_user = StringField('Auth User')
    auth_password = StringField('Auth Password')
    auth_method = SelectField('Auth Methods',choices=[{'basic-auth':0}],coerce=int)

    
