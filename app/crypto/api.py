from flask import Flask, Blueprint, json
from flask_restful import Resource, Api
from . import queries

bp = Blueprint('api',__name__,url_prefix='/api/1.0')
api = Api(bp)
DATE_FORMAT = '%Y%m%d-%H%M%S'
class HelloWorld(Resource):
    def get(self):
        return {'hello':'world'}

class last_ptr(Resource):
    def get(self):
        data = queries.last_ptr().created_on.strftime(DATE_FORMAT)
        return {
            'errors':[],
            'data':data
        }
class last_prices(Resource):    
    def get(self,coinid,interval=3, limit=20):
        data = queries.get_last_coin_prices(coinid,interval,limit)       
        result = []
        for d in data:
            result.append({
                'instrumement_id': d.cryptoinstrument_id,
                'closing_price':float(d.price_close),
                'retreived_datetime':d.retreived_datetime.strftime(DATE_FORMAT)
            })   
        payload = {
            'errors':[],
            'data':result
        }   
        return json.dumps(payload)

api.add_resource(HelloWorld,'/helloworld')
api.add_resource(last_prices,'/lastprices/<int:coinid>/<int:interval>/<int:limit>')
api.add_resource(last_ptr,'/lastptr')