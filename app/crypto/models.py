
from app import db
from app.models import BaseModel

class CryptoExchange(BaseModel):
    __tablename__ = 'cryptoexchange'
    url = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100), unique=True)
    active = db.Column(db.Boolean(), default=True)
    
class CryptoInstrument(BaseModel):
    __tablename__ = 'cryptoinstrument'
    name = db.Column(db.String(30), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    note = db.Column(db.String(512))
    active = db.Column(db.Boolean(), default=True)

instrument_exchange_table = db.Table('instrument_exchange',
                    db.Column('cryptoinstrument_id', db.Integer, db.ForeignKey('cryptoinstrument.id'), primary_key = True), 
                    db.Column('cryptoexchange_id', db.Integer, db.ForeignKey('cryptoexchange.id'), primary_key = True))

class CryptoFiatCurrency(BaseModel):
    __tablename__ = 'currency'
    name = db.Column(db.String(20),unique=True,nullable=False)
    code = db.Column(db.String(3), unique=True, nullable=False)

class CryptoInstrumentPrice(BaseModel):
    __doc__ = "Price of instrument on exchange expressed in associated currency."
    __tablename__ = 'cryptoinstrumentprice'    
    instrument_id = db.Column(db.Integer,db.ForeignKey('cryptoinstrument.id'),nullable=False)
    exchange_id = db.Column(db.Integer,db.ForeignKey('cryptoexchange.id'),nullable=False)
    price = db.Column(db.Float(precision=10,asdecimal=True),nullable=False)    
    currency = db.Column(db.Integer,db.ForeignKey('currency.id'), nullable=False)

class DataProvider(BaseModel):
    __tablename__ = 'dataprovider'
    name = db.Column(db.String(80), unique=True)
    auth_user = db.Column(db.String(50))
    auth_password =db.Column(db.String(80))
    auth_method = db.Column(db.Integer, nullable=False)

class DataProviderSourceUrl(BaseModel):
    __tablename__ = 'dataprovidersourceurl'
    url = db.Column(db.String(1024))
    provider_id = db.Column(db.Integer,db.ForeignKey('dataprovider.id'), nullable=False)

class ProviderTransactionRequest(BaseModel):
    __tablename__ = 'providertransactionrequest'
    url = db.Column(db.String(1024))
    dataprovider_id = db.Column(db.Integer,db.ForeignKey('dataprovider.id'), nullable=False)
    dataprovidersourceurl_id = db.Column(db.Integer, db.ForeignKey('dataprovidersourceurl.id'), nullable=False)
    message_type_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(2048))



