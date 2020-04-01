import os
from flask import make_response
from flask_restful import Resource

class Health(Resource):
    def get(self):
        return make_response({
            'status': 'success',
            'message': 'pong!',
            'container_id': os.uname()[1]
        }, 200)