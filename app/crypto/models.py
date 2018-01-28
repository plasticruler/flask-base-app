
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
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    note = db.Column(db.String(1024))
    active = db.Column(db.Boolean(), default=True)
    foreign_id = db.Column(db.Integer)
    image_url = db.Column(db.String(190))
    algorithm = db.Column(db.String(30))
    twitter_handle = db.Column(db.String(30))
    website_ahref_tag = db.Column(db.String(100))
    track_price = db.Column(db.Boolean(), default=False)
    
    def __repr__(self):
        return "{} ({})".format(self.name,self.symbol)

instrument_exchange_table = db.Table('instrument_exchange',
                    db.Column('cryptoinstrument_id', db.Integer, db.ForeignKey('cryptoinstrument.id'), primary_key = True), 
                    db.Column('cryptoexchange_id', db.Integer, db.ForeignKey('cryptoexchange.id'), primary_key = True))

class Currency(BaseModel):
    __tablename__ = 'currency'
    name = db.Column(db.String(20),unique=True,nullable=False)
    symbol = db.Column(db.String(3), unique=True, nullable=False)
    def __repr__(self):
        return "{} ({})".format(self.name,self.symbol)



class DataProvider(BaseModel):
    __tablename__ = 'dataprovider'
    name = db.Column(db.String(80), unique=True)    
    #urls = db.relationship('DataProviderSourceUrl',backref='dataprovider',lazy='dynamic')
    is_active = db.Column(db.Boolean(), default=False)
    def __repr__(self):
        return self.name

class CryptoInstrumentPrice(BaseModel):
    __doc__ = "Price of instrument on exchange expressed in associated currency."
    __tablename__ = 'cryptoinstrumentprice'    
    cryptoinstrument_id = db.Column(db.Integer,db.ForeignKey('cryptoinstrument.id'),nullable=False)    
    dataprovider_id = db.Column(db.Integer,db.ForeignKey('dataprovider.id'),nullable=True)
    price = db.Column(db.Float(precision=10,asdecimal=True),nullable=False)    
    currency_id = db.Column(db.Integer,db.ForeignKey('currency.id'), nullable=False)
    interval = db.Column(db.Integer,nullable=False)
    retreived_datetime = db.Column(db.DateTime)
    def __repr__(self):
        return "At {} 1 {} cost {} in {} and interval {}".format(self.retreived_datetime, CryptoInstrument.query.get(self.cryptoinstrument_id).name, self.price, Currency.query.get(self.currency_id), self.interval)

class CryptoInstrumentPriceMarketData(BaseModel):
    __tablename__ = 'cryptoinstrumentpricemarketdatas'
    cryptoinstrument_id = db.Column(db.Integer,db.ForeignKey('cryptoinstrument.id'),nullable=False)    
    dataprovider_id = db.Column(db.Integer,db.ForeignKey('dataprovider.id'),nullable=True)
    price = db.Column(db.Float(precision=10,asdecimal=True))    
    currency_id = db.Column(db.Integer,db.ForeignKey('currency.id'), nullable=False)
    interval = db.Column(db.Integer,nullable=False)
    retreived_datetime = db.Column(db.DateTime)
    volume_from = db.Column(db.Integer)
    volume_to = db.Column(db.Integer)
    price_open = db.Column(db.Float(precision=10,asdecimal=True))
    price_close = db.Column(db.Float(precision=10,asdecimal=True))
    price_low = db.Column(db.Float(precision=10,asdecimal=True))
    def __init__(self,cip):
        if not type(cip) is CryptoInstrumentPrice:
            raise 'Incorrect type used to initialise CryptoInstrumentPriceMarketData'
        self.cryptoinstrument_id = cip.cryptoinstrument_id    
        self.dataprovider_id = cip.dataprovider_id
        self.price = cip.price
        self.currency_id = cip.currency_id
        self.retreived_datetime = cip.retreived_datetime 
        self.interval = cip.interval  
    def __repr__(self):
        return "Instrument {} at {}".format(CryptoInstrument.query.get(self.cryptoinstrument_id),self.retreived_datetime) 
            

class MessageType(BaseModel):    
    __tablename__ = 'messagetype'
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(1024))
    dataprovider_id = db.Column(db.Integer,db.ForeignKey('dataprovider.id'),nullable=False)

class DataProviderSourceUrl(BaseModel):
    __tablename__ = 'dataprovidersourceurl'
    url = db.Column(db.String(1024))
    description = db.Column(db.String(1024))
    auth_user = db.Column(db.String(50))
    auth_password =db.Column(db.String(80))
    auth_method = db.Column(db.Integer, nullable=False)
    use_authentication = db.Column(db.Boolean())
    auto_added = db.Column(db.Boolean(),default=False)
    #dataprovider_id = db.Column(db.Integer,db.ForeignKey('dataprovider.id'), nullable=False)
    messagetype_id = db.Column(db.Integer, db.ForeignKey('messagetype.id'), nullable=False)
    messagetype = db.relationship('MessageType',backref='dataprovidersourceurl')    

class ProviderTransactionRequest(BaseModel):
    __tablename__ = 'providertransactionrequest'
    url = db.Column(db.String(1024))        
    messagetype_id = db.Column(db.Integer,db.ForeignKey('messagetype.id'),nullable=False)
    content = db.Column(db.String(16384))       
    messagetype = db.relationship('MessageType',backref='providertransactionrequest') 
    processed = db.Column(db.Boolean(), default=False)   




