from flask import Flask
from flask_restful import Resource, Api

from crypto import bp

api = Api(bp)

class HelloWorld(Resource):
    def get(self):
        return {'hello':'world'}

api.add_resource(HelloWorld,'/')