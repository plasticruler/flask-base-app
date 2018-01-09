
from app.crypto.models import ProviderTransactionRequest
from app import db
import logging

class PTR(object):
    def __init__(self,provider_id, request_type, url, app=None):
        self.provider_id = provider_id
        self.request_type = request_type
        self.url = url
        self.app = app
    def save(self,content):
        ptr = ProviderTransactionRequest()
        ptr.url = self.url
        ptr.content = content.decode('utf8')
        ptr.message_type_id = self.request_type
        ptr.provider_id = self.provider_id  
        if self.app:
            self.app.logger.debug('Saving ptr record for {}'.format(self.url))
        db.session.add(ptr)
        db.session.commit()      
        