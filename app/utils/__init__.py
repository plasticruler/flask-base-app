#download a web page the db as a provider track request

import requests

class DownloadURL(object):
    def __init__(self, url, ptr=None, params = None, headers=None,logger=None):
        self.url = url
        self.params = params
        self.headers = headers or {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'}
        self.ptr = ptr        
        self.logger=logger
    def __call__(self, *args, **kwargs):
        if 'url' in kwargs:            
            self.url = kwargs['url']
        if 'params' in kwargs:
            self.params = kwargs['params']
        if 'headers' in kwargs:
            self.headers = kwargs['headers']     
        if self.logger:
            self.logger.debug("Downloading {}".format(self.url))
        content =  requests.get(self.url, params=self.params, headers=self.headers)
        content = content.text.encode('utf-8')
        if self.ptr:
            self.ptr.save(content)
        return {'url':self.url,'content':content}
        