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

class MessageTypeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5)])
    dataprovider_id = SelectField('Data Provider',choices=[],coerce=int)
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Save')

class DataProviderSourceURLForm(FlaskForm):
    dataprovider_id = SelectField('Data Provider',choices=[],coerce=int)
    messagetype_id = SelectField('Message Type', choices=[], coerce=int)
    url = StringField('Source URL', validators=[DataRequired(), Length(min=15)])
    description = StringField('Description')
    auth_method = SelectField('Auth method',choices=[],coerce=int)
    auth_user = StringField('Auth User')
    auth_password = StringField('Auth Password')
    use_authentication = BooleanField('Requires Auth')    
    submit = SubmitField('Save')

class DataProviderForm(FlaskForm):        
    name = StringField('Provider Name', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Save')
