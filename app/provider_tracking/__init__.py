
from app.crypto.models import ProviderTransactionRequest
from app import db

class PTR(object):
    def __init__(self, messagetype_id, url, logger=None):        
        self.messagetype_id = messagetype_id        
        self.url = url
        self.logger = logger
    def save(self,content):
        ptr = ProviderTransactionRequest()
        ptr.url = self.url
        ptr.content = content.decode('utf8')
        ptr.messagetype_id = self.messagetype_id    
        ptr.processed = False       
        if self.logger:
            self.logger.debug('Saving ptr record for {}'.format(self.url))
        db.session.add(ptr)
        db.session.commit()      
        