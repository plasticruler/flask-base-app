# -*- coding: utf-8 -*-
from app import create_app, db, mail
from app.models import *
from app.crypto.models import *
from app.crypto.queries import *
from flask_mail import Message
from flask_migrate import Migrate
import os
import json
from sqlalchemy import desc
import click
from app.utils import DownloadURL
from app.provider_tracking import PTR
import codecs
import sys
import urlparse
import datetime
import itertools

app = create_app(os.getenv('FLASK_CONFIG') or 'dev')
migrate = Migrate(app,db)
COIN_FILENAME = 'coins.json'

@app.cli.command('download-data')
@click.option('--messagetype')
def download_data(messagetype):
    dps = DataProviderSourceUrl.query.filter_by(is_deleted=False,messagetype_id=messagetype).order_by('dataprovider_id')
    for dp in dps:
        ptr = PTR(messagetype_id=dp.messagetype_id, url=dp.url, logger=app.logger)         
        u = DownloadURL(dp.url,ptr,logger=app.logger)
        u() #execute and save using in data request record

@app.cli.command('download-coin-data')
def download_coindata():    
    app.logger.info("Downloading coin data to file {}.".format(COIN_FILENAME))
    coins_url = 'https://www.cryptocompare.com/api/data/coinlist/'    
    data = DownloadURL(coins_url)
    data = data()['content']    
    with open(COIN_FILENAME,'w') as f:
        f.write(data)
    app.logger.info("Data downloaded and written to '{}'".format(COIN_FILENAME))

@app.cli.command('load-coins')
def populate_coin_type_data():    
    if not os.path.isfile(COIN_FILENAME):
        app.logger.error('{} file not found. Have you run job download-coin-data ?'.format(COIN_FILENAME))
        return
    app.logger.info("Reprocessing the {} file.".format(COIN_FILENAME))
    coin_social_data_url = "https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={}"    
    with open(COIN_FILENAME) as json_data:
        data = json.load(json_data) 
        count = len(data["Data"])
        i = 0
        for d in data["Data"]:           
            i += 1
            ci = CryptoInstrument()            
            symbol = unicode(data["Data"][d]["Symbol"])
            if CryptoInstrument.query.filter(CryptoInstrument.symbol==symbol).count()>0:
                app.logger.debug("Updating coin {}".format(symbol))
                ci = CryptoInstrument.query.filter(CryptoInstrument.symbol==symbol).one()            
            
            ci.name = unicode(data["Data"][d]["CoinName"])
            ci.symbol = symbol
            ci.note = unicode(data["Data"][d]["FullName"])
            ci.foreign_id= int(data["Data"][d]["Id"])
            ci.active = True                
            
            coin_social_data = DownloadURL(coin_social_data_url.format(ci.foreign_id))()            
            coin_social_data = json.loads(coin_social_data['content'])
            coin_social_data = coin_social_data["Data"]["General"]
            ci.image_url = "https://www.cryptocompare.com{}".format(coin_social_data["ImageUrl"])
            ci.algorithm = unicode(coin_social_data["Algorithm"])
            ci.twitter_handle = unicode(coin_social_data["Twitter"])
            ci.note = unicode(coin_social_data["Description"])
            ci.website_ahref_tag = unicode(coin_social_data["Website"])        
            db.session.add(ci)
            db.session.commit()
            app.logger.debug("At {} of {} coins.".format(i,count))         
            
    app.logger.info('Procesing of {} file completed.'.format(COIN_FILENAME))

@app.cli.command('load-download-urls')
def set_instruments_for_tracking():
    app.logger.info("Reset track_price on tracked instruments.")
    codes = ['ETH','BCH','BTG','EOS','LTC','NMC','DASH','ZEC','XRP','BTC','IOT','XLM','TRX','ICX','XMR','TRX']
    for c in codes:
        app.logger.debug('Looking for coin {}'.format(c))
        ci = CryptoInstrument.query.filter(CryptoInstrument.symbol==c).first()
        ci.track_price = True        
        app.logger.info("Enable price tracking for '{}'".format(c))
        db.session.add(ci)
        app.logger.info('Creating tracking urls for {}'.format(c))        
        intervals = {5:'hour',6:'day'}
        for k,v in intervals.items():                         
            msg_type = MessageType.query.get(k) #hourly
            dpsu = DataProviderSourceUrl(auto_added=True)
            dpsu.messagetype_id = msg_type.id
            dpsu.auth_method = -1
            dpsu.url = 'https://min-api.cryptocompare.com/data/histo{}?fsym={}&tsym=USD&limit=480&e=CCCAGG'.format(v,c)
            dpsu.description = "cryptocompare {} for {}".format(v,c)
            app.logger.info('Create tracking url {} '.format(dpsu.url))   
            if not DataProviderSourceUrl.query.filter(DataProviderSourceUrl.url==dpsu.url).first()==None:
                app.logger.info('Not adding {}'.format(dpsu.url))
                continue       
            db.session.add(dpsu)      
        db.session.commit()
    app.logger.info('Tracking urls creation completed.')      

@app.cli.command('get-latest-prices')
def get_latest_price_mark_inactive():    
    app.logger.info("Getting the instantaneous prices for tracked instruments using cryptocompare api.")
    base_url = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=USD,ZAR"    
    cryptos = [(x.id, x.symbol) for x in CryptoInstrument.query.filter(CryptoInstrument.track_price)]  
    #cryptos = [(1315,'BTC')]  
    m = MessageType.query.filter(MessageType.name=='cryptocompare-instant-price').one()    
    for c in cryptos:
        url = base_url.format(c[1])
        ptr = PTR(m.id, url, app.logger)       
        data = DownloadURL(url,logger=app.logger,ptr=ptr)        
        data = data()["content"]
        data = json.loads(data)
        if 'Response' in data:
            if data["Response"]=="Error":
                coin = CryptoInstrument.query.get(c[0])
                coin.track_price=False
                db.session.add(coin)
                db.session.commit()
                app.logger.info("No price so setting price tracking off for coin {}".format(coin))
        

@app.cli.command('print-last-ptr')
def print_last_ptr():
    ptr = ProviderTransactionRequest.query.order_by(desc('id')).first().created_on
    send_email(str(ptr),"Last PTR statistic")
    app.logger.info(ptr)    

@app.cli.command('last-prices')
@click.option('--symbol')
@click.option('--interval')
@click.option('--limit',default=10)
def get_last_prices(symbol, interval,limit):
    coin = CryptoInstrument.query.filter_by(symbol=symbol).first()
    m = []
    if coin is None:
        app.logger.error('No such coin found ({})'.format(symbol))
        send_email("Invalid coin requested {}".format(symbol),mailsubject="Error")
        return        
    records = GetLastCoinPrices(coin.id, interval, limit)
    for i in records: #price_close
        m.append(str(i))
        app.logger.info(i)
    content = "\n".join(m)    
    rising = any(earlier.price_close >= later.price_close for earlier,later in itertools.izip(records,records[1:]))    
    s = "Last {} prices email - {} (RISING: {})".format(interval, symbol, rising)
    app.logger.info(s)
    send_email(content, mailsubject=s)

def send_email(message, mailsubject="No subject needed", recipients=None):
    if recipients is None:
        recipients = app.config['ADMINS']
    app.logger.info('Sending email')
    msg = Message(body=message,recipients=recipients, subject=app.config['APP_NAME'] + mailsubject)
    mail.send(msg)
    app.logger.info('Sent.')

@app.cli.command('process-data')
def process_data():
    app.logger.info("Processing downloaded price data.")
    unprocessedptrs = ProviderTransactionRequest.query.filter(ProviderTransactionRequest.processed==False)     
    for ptr in unprocessedptrs:  
        app.logger.info('Processing {}'.format(ptr))
        if ptr.messagetype_id ==4:   #instant price       
            params = urlparse.parse_qs(urlparse.urlparse(unicode(ptr.url)).query)
            price_obj = json.loads(ptr.content)                       
            for c in params['tsyms'][0].split(','): #each currency
                price = CryptoInstrumentPrice()                
                instrument = CryptoInstrument.query.filter(CryptoInstrument.symbol==params['fsym'][0]).one()                
                price.cryptoinstrument_id = instrument.id                
                price.currency_id = Currency.query.filter(Currency.symbol==c).one().id
                price.dataprovider_id = ptr.messagetype.dataprovider_id
                price.interval=1                
                price.price = float(price_obj[c])                
                price.retreived_datetime = ptr.created_on                                              
                db.session.add(price)               
            ptr.processed = True
            db.session.add(ptr)
            db.session.commit() 
        
        if ptr.messagetype_id==5: #hourly
            params = urlparse.parse_qs(urlparse.urlparse(unicode(ptr.url)).query)
            data = json.loads(ptr.content)
            data = data["Data"]
            for d in data:         
                price = CryptoInstrumentPrice()
                instrument = CryptoInstrument.query.filter(CryptoInstrument.symbol==params['fsym'][0]).one()                
                price.cryptoinstrument_id = instrument.id                
                price.currency_id = Currency.query.filter(Currency.symbol==params['tsym'][0]).one().id
                price.dataprovider_id = ptr.messagetype.dataprovider_id
                price.interval=2                   
                price.price = float(d["close"])                
                price.retreived_datetime =  datetime.datetime.fromtimestamp(d["time"]) 
                
                market_data = CryptoInstrumentPriceMarketData(price)
                market_data.volume_from = int(d["volumefrom"])
                market_data.volume_to = int(d["volumeto"])
                market_data.price_open = float(d["open"])
                market_data.price_close = float(d["close"])
                market_data.price_low = float(d["low"])
                market_data.price_high = float(d["high"])
                if (CryptoInstrumentPriceMarketData.query.filter(
                    CryptoInstrumentPriceMarketData.retreived_datetime==market_data.retreived_datetime,
                    CryptoInstrumentPriceMarketData.cryptoinstrument_id==market_data.cryptoinstrument_id,
                    CryptoInstrumentPriceMarketData.interval==price.interval).first() is None):
                    db.session.add(market_data)                    
                    app.logger.info("Record added {}".format(market_data))  
                                                        
            ptr.processed = True
            db.session.add(ptr)
            db.session.commit()
        
        if ptr.messagetype_id==6: #daily
            params = urlparse.parse_qs(urlparse.urlparse(unicode(ptr.url)).query)
            data = json.loads(ptr.content)
            data = data["Data"]
            for d in data:         
                price = CryptoInstrumentPrice()
                instrument = CryptoInstrument.query.filter(CryptoInstrument.symbol==params['fsym'][0]).one()                
                price.cryptoinstrument_id = instrument.id                
                price.currency_id = Currency.query.filter(Currency.symbol==params['tsym'][0]).one().id
                price.dataprovider_id = ptr.messagetype.dataprovider_id
                price.interval=3                  
                price.price = float(d["close"])                
                price.retreived_datetime =  datetime.datetime.fromtimestamp(d["time"])                         
                
                market_data = CryptoInstrumentPriceMarketData(price)
                market_data.volume_from = int(d["volumefrom"])
                market_data.volume_to = int(d["volumeto"])
                market_data.price_open = float(d["open"])
                market_data.price_close = float(d["close"])
                market_data.price_low = float(d["low"])
                market_data.price_high = float(d["high"])
                if (CryptoInstrumentPriceMarketData.query.filter(
                    CryptoInstrumentPriceMarketData.retreived_datetime==market_data.retreived_datetime,
                    CryptoInstrumentPriceMarketData.cryptoinstrument_id==market_data.cryptoinstrument_id,
                    CryptoInstrumentPriceMarketData.interval==price.interval).first() is None):
                    db.session.add(market_data)                    
                    app.logger.debug("Record added {}".format(market_data))                                  
            ptr.processed = True
            db.session.add(ptr)
            db.session.commit()                 
        continue
        if ptr.messagetype.name == 'market depth' and ptr.dataprovider.name.strip()=='Ice3x':
            data = json.loads(ptr.content)            
            if not data["errors"]:
                data = get_market_summary_ice3x(data,'eth/zar')
                o.created_on
                for d in data:                    
                    cip = CryptoInstrumentPrice()
                    cip.price = d["last_price"]                    
                    c = Currency.query.filter(Currency.symbol=='ZAR').first()                 
                    cip.currency=c                    
            else:
                raise Exception('Error in json.') 
    app.logger.info("Data processed")

def get_market_summary_ice3x(content, pair):        
    data = content["response"]["entities"]
    return [x for x in data if str(x['pair_name'])==pair]


@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User': User,'Expense':Expense, 'ExpenseType':ExpenseType, \
            'CryptoExchange':CryptoExchange, 'CryptoInstrument':CryptoInstrument,'ProviderTransactionRequest':ProviderTransactionRequest, \
            'DataProviderSourceUrl':DataProviderSourceUrl, 'DataProvider':DataProvider, 'CryptoInstrumentPriceMarketData':CryptoInstrumentPriceMarketData}

if __name__=='__main__':
    app.run()
