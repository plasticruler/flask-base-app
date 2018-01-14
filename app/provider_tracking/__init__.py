
from app.crypto.models import ProviderTransactionRequest
from app import db
import logging

class PTR(object):
    def __init__(self,dataprovider_id, messagetype_id, url,dataprovidersourceurl_id, app=None):
        self.dataprovider_id = dataprovider_id
        self.messagetype_id = messagetype_id
        self.dataprovidersourceurl_id = dataprovidersourceurl_id
        self.url = url
        self.app = app
    def save(self,content):
        ptr = ProviderTransactionRequest()
        ptr.url = self.url
        ptr.content = content.decode('utf8')
        ptr.message_type_id = self.messagetype_id
        ptr.dataprovider_id = self.dataprovider_id          
        ptr.dataprovidersourceurl_id = self.dataprovidersourceurl_id
        if self.app:
            self.app.logger.debug('Saving ptr record for {}'.format(self.url))
        db.session.add(ptr)
        db.session.commit()      
        