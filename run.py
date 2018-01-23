# -*- coding: utf-8 -*-
from app import create_app, db
from app.models import *
from app.crypto.models import *
from flask_migrate import Migrate
import os
import json
from celery import Celery
import click
from app.utils import DownloadURL
from app.provider_tracking import PTR
import codecs
import sys
import urlparse

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app,db)
COIN_FILENAME = 'coins.json'

@app.cli.command('download-data')
def download():
    dps = DataProviderSourceUrl.query.filter(DataProvider.is_active==True).order_by('dataprovider_id')
    for dp in dps:
        ptr = PTR(messagetype_id=dp.messagetype_id, url=dp.url, logger=app.logger)         
        u = DownloadURL(dp.url,ptr,logger=app.logger)
        u() #execute and save using in data request record

@app.cli.command('download-coin-data')
def downloadcoindata():    
    app.logger.info("Downloading coin data to file {}.".format(COIN_FILENAME))
    coins_url = 'https://www.cryptocompare.com/api/data/coinlist/'    
    data = DownloadURL(coins_url)
    data = data()['content']    
    with open(COIN_FILENAME,'w') as f:
        f.write(data)
    app.logger.info("Data downloaded and written to '{}'".format(coin_file))

@app.cli.command('load-coins')
def populatecointypedata():    
    app.logger.info("Reprocessing the {} file.".format(COIN_FILENAME))
    coin_social_data_url = "https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={}"    
    with open(COIN_FILENAME) as json_data:
        data = json.load(json_data) 
        count = len(data["Data"])
        i = 0
        for d in data["Data"]:
            #print data["Data"][d]
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
              
            #print "Getting social data for {} at {}".format(ci.symbol, coin_social_data_url.format(ci.foreign_id))
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
            #app.logger.info("Added coin {} ({}) {} of {}.".format(unicode(ci.name),unicode(ci.symbol), i,count))

@app.cli.command('set-instruments-for-price-tracking')
def setinstrumentfortracking():
    app.logger.info("Reset track_price on tracked instruments.")
    codes = ['ETH','BCH','BTG','EOS','LTC','NMC','DASH','ZEC','XRP','BTC','IOT','XLM','TRX','ICX','XMR','TRX']
    for c in codes:
        app.logger.debug('Looking for coin {}'.format(c))
        ci = CryptoInstrument.query.filter(CryptoInstrument.symbol==c).first()
        ci.track_price = True        
        app.logger.info("Enable price tracking for '{}'".format(c))
        db.session.add(ci)
    app.logger.debug("Instrument price tracking commiting...")
    db.session.commit()
    app.logger.debug("All records committed.")
    

@app.cli.command('get-latest-prices')
def getlatestpricemarkinactive():    
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
        print data

@app.cli.command('process-data')
def processdata():
    app.logger.info("Processing downloaded price data.")
    unprocessedptrs = ProviderTransactionRequest.query.filter(ProviderTransactionRequest.processed==False)     
    for ptr in unprocessedptrs:  
        if ptr.messagetype_id ==4:            
            params = urlparse.parse_qs(urlparse.urlparse(unicode(ptr.url)).query)
            price_obj = json.loads(ptr.content)                       
            for c in params['tsyms'][0].split(','): #each currency
                price = CryptoInstrumentPrice()
                instrument = CryptoInstrument.query.filter(CryptoInstrument.symbol==params['fsym'][0]).one()
                price.cryptoinstrument_id = instrument.id
                price.currency_id = Currency.query.filter(Currency.code==c).one()
                price.dataprovider_id = ptr.messagetype.dataprovider_id
                price.interval=1
                price.price = float(price_obj[c])                
                price.retreived_datetime = ptr.created_on
                print price
                #db.session.add(price)
            #ptr.processed = True
            #db.session.add(ptr)
            #db.session.commit()            
        continue
        if ptr.messagetype.name == 'market depth' and ptr.dataprovider.name.strip()=='Ice3x':
            data = json.loads(ptr.content)            
            if not data["errors"]:
                data = getmarketsummaryice3x(data,'eth/zar')
                o.created_on
                for d in data:
                    print d
                    cip = CryptoInstrumentPrice()
                    cip.price = d["last_price"]                    
                    c = Currency.query.filter(Currency.code=='ZAR').first()                 
                    cip.currency=c                    
            else:
                raise Exception('Error in json.')
    app.logger.info("Found {} records".format(unprocessedptrs.count()))
    app.logger.info("Data processed")

def getmarketsummaryice3x(content, pair):        
    data = content["response"]["entities"]
    return [x for x in data if str(x['pair_name'])==pair]

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User': User,'Expense':Expense, 'ExpenseType':ExpenseType, \
            'CryptoExchange':CryptoExchange, 'ProviderTransactionRequest':ProviderTransactionRequest, \
            'DataProviderSourceUrl':DataProviderSourceUrl, 'DataProvider':DataProvider}