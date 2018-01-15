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

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app,db)

@app.cli.command('download-data')
def download():
    dps = DataProviderSourceUrl.query.order_by('dataprovider_id')
    for dp in dps:
        ptr = PTR(dp.dataprovider_id, dp.messagetype_id, dp.url, dp.id, app=app)
        u = DownloadURL(dp.url,ptr)
        u()

@app.cli.command('load-coins')
def populatecointypedata():
    coins_url = 'https://www.cryptocompare.com/api/data/coinlist/'
    coin_social_data_url = "https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={}"
    #data = DownloadURL(coins_url)
    #data = data()['content']
    coin_file = 'coins.json'
    #UTF8Writer = codecs.getwriter('utf8')
    #with open(coin_file,'w') as f:
    #    f.write(data)
    with open(coin_file) as json_data:
        data = json.load(json_data) 
        count = len(data["Data"])
        i = 0
        for d in data["Data"]:
            #print data["Data"][d]
            ci = CryptoInstrument()            
            ci.name = unicode(data["Data"][d]["CoinName"])
            ci.symbol = unicode(data["Data"][d]["Symbol"])
            ci.note = unicode(data["Data"][d]["FullName"])
            ci.foreign_id= int(data["Data"][d]["Id"])
            ci.active = True
            i +=1
            if CryptoInstrument.query.filter(CryptoInstrument.symbol==ci.symbol).count()>0:
                continue      
            #print "Getting social data for {} at {}".format(ci.symbol, coin_social_data_url.format(ci.foreign_id))
            coin_social_data = DownloadURL(coin_social_data_url.format(ci.foreign_id))()            
            coin_social_data = json.loads(coin_social_data['content'])
            coin_social_data = coin_social_data["Data"]["General"]
            ci.image_url = "https://www.cryptocompare.com/{}".format(unicode(coin_social_data["ImageUrl"]))
            ci.algorithm = unicode(coin_social_data["Algorithm"])
            ci.twitter_handle = unicode(coin_social_data["Twitter"])
            ci.note = unicode(coin_social_data["Description"])
            ci.website_ahref_tag = unicode(coin_social_data["Website"])        
            db.session.add(ci)
            db.session.commit()         
            print "Added coin {} ({}) {} of {}.".format(unicode(ci.name),unicode(ci.symbol), i,count)
    

@app.cli.command('process-data')
def processdata():
    unprocessedptrs = ProviderTransactionRequest.query.filter(ProviderTransactionRequest.processed==False)
    for ptr in unprocessedptrs:
        o = ProviderTransactionRequest()   
        if ptr.dataprovidersourceurl.messagetype.name == 'market depth' and ptr.dataprovider.name.strip()=='Ice3x':
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
    print "Found {} records".format(unprocessedptrs.count())
    print "Data processed"

def getmarketsummaryice3x(content, pair):        
    data = content["response"]["entities"]
    return [x for x in data if str(x['pair_name'])==pair]

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User': User,'Expense':Expense, 'ExpenseType':ExpenseType, \
            'CryptoExchange':CryptoExchange, 'ProviderTransactionRequest':ProviderTransactionRequest, \
            'DataProviderSourceUrl':DataProviderSourceUrl, 'DataProvider':DataProvider}