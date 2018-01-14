#download a web page the db as a provider track request

import requests

class DownloadURL(object):
    def __init__(self, url, ptr=None, params = None, headers=None):
        self.url = url
        self.params = params
        self.headers = headers
        self.ptr = ptr        
    def __call__(self, *args, **kwargs):
        if 'url' in kwargs:
            self.url = kwargs['url']
        if 'params' in kwargs:
            self.params = kwargs['params']
        if 'headers' in kwargs:
            self.headers = kwargs['headers']        
        content =  requests.get(self.url, params=self.params, headers=self.headers)
        content = content.text.encode('utf-8')
        if self.ptr:
            self.ptr.save(content)
        return {'url':self.url,'content':content}
        