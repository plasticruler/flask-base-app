#download a web page the db as a provider track request

import requests

class DownloadURL(object):
    def __init__(self, url, ptr=None, params = None, headers=None):
        self.url = url
        self.params = params
        self.headers = headers
        self.ptr = ptr
        if not ptr:
            raise Exception('invalid ptr object.')
    def __call__(self, *args, **kwargs):
        if 'url' in kwargs:
            self.url = kwargs['url']
        if 'params' in kwargs:
            self.params = kwargs['params']
        if 'headers' in kwargs:
            self.headers = kwargs['headers']
        print "Downloading file at '{}'".format(self.url)
        res =  requests.get(self.url, params=self.params, headers=self.headers)
        self.ptr.save(res.text.encode('utf-8'))
        return self.url
        