
from app import db
from app.models import BaseModel

class CryptoExchange(BaseModel):
    __tablename__ = 'cryptoexchange'
    url = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100), unique=True)
    active = db.Column(db.Boolean(), default=True)
    
class CryptoInstrument(BaseModel):
    __tablename__ = 'cryptoinstrument'
    name = db.Column(db.String(30), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    note = db.Column(db.String(512))
    active = db.Column(db.Boolean(), default=True)
    def __repr__(self):
        return "{} ({})".format(self.name,self.code)

instrument_exchange_table = db.Table('instrument_exchange',
                    db.Column('cryptoinstrument_id', db.Integer, db.ForeignKey('cryptoinstrument.id'), primary_key = True), 
                    db.Column('cryptoexchange_id', db.Integer, db.ForeignKey('cryptoexchange.id'), primary_key = True))

class Currency(BaseModel):
    __tablename__ = 'currency'
    name = db.Column(db.String(20),unique=True,nullable=False)
    code = db.Column(db.String(3), unique=True, nullable=False)
    def __repr__(self):
        return "{} ({})".format(self.name,self.code)

class CryptoInstrumentPrice(BaseModel):
    __doc__ = "Price of instrument on exchange expressed in associated currency."
    __tablename__ = 'cryptoinstrumentprice'    
    crytoinstrument_id = db.Column(db.Integer,db.ForeignKey('cryptoinstrument.id'),nullable=False)
    cryptoexchange_id = db.Column(db.Integer,db.ForeignKey('cryptoexchange.id'),nullable=False)
    price = db.Column(db.Float(precision=10,asdecimal=True),nullable=False)    
    currency = db.Column(db.Integer,db.ForeignKey('currency.id'), nullable=False)

class DataProvider(BaseModel):
    __tablename__ = 'dataprovider'
    name = db.Column(db.String(80), unique=True)    
    urls = db.relationship('DataProviderSourceUrl',backref='dataprovider',lazy='dynamic')
    def __repr__(self):
        return self.name

class MessageType(BaseModel):    
    __tablename__ = 'messagetype'
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(1024))

class DataProviderSourceUrl(BaseModel):
    __tablename__ = 'dataprovidersourceurl'
    url = db.Column(db.String(1024))
    description = db.Column(db.String(1024))
    auth_user = db.Column(db.String(50))
    auth_password =db.Column(db.String(80))
    auth_method = db.Column(db.Integer, nullable=False)
    use_authentication = db.Column(db.Boolean)
    dataprovider_id = db.Column(db.Integer,db.ForeignKey('dataprovider.id'), nullable=False)
    #dataprovider = db.relationship('DataProvider',backref='dataprovidersourceurl')
    messagetype_id = db.Column(db.Integer, db.ForeignKey('messagetype.id'), nullable=False)
    messagetype = db.relationship('MessageType',backref='dataprovidersourceurl')    

class ProviderTransactionRequest(BaseModel):
    __tablename__ = 'providertransactionrequest'
    url = db.Column(db.String(1024))
    dataprovider_id = db.Column(db.Integer,db.ForeignKey('dataprovider.id'), nullable=False)
    dataprovidersourceurl_id = db.Column(db.Integer, db.ForeignKey('dataprovidersourceurl.id'), nullable=False)    
    content = db.Column(db.String(2048))
    dataprovider = db.relationship('DataProvider',backref='providertransactionrequest')
    processed = db.Column(db.Boolean, default=False)
    dataprovidersourceurl = db.relationship('DataProviderSourceUrl', backref='providertransactionrequest')




