import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from database.mongo import configure_mongodb

"""API object"""
api = Api()
"""CORS object"""
cors = CORS()

def create_app(**config):
    """ Create application.
        app = create_app() # app can be used as WSGI application
        app.run() # Or you can run as a simple web server
    """
    app = Flask(__name__, static_folder=None)

    configure_app(app)
    configure_logging(app)
    configure_cors(app)
    configure_mongodb(app)
    configure_api(app)
    
    return app

def configure_app(app):
    """ Configure application. """
    from common.utils import MongoJSONEncoder
    app.json_encoder = MongoJSONEncoder

    app.config['LOG_LEVEL'] = 'DEBUG'

    app.config['MONGO_HOST'] = os.environ.get('MONGO_HOST', 'localhost')
    app.config['MONGO_PORT'] = os.environ.get('MONGO_PORT', '27017')
    app.config['MONGO_DB'] = os.environ.get('MONGO_DB', 'flask_api')

    app.config['MONGO_URI'] = "mongodb://{}:{}/{}".format(
        app.config['MONGO_HOST'],
        app.config['MONGO_PORT'],
        app.config['MONGO_DB']
    )

def configure_logging(app):
    """ Configure logging.
        Call ``logging.basicConfig()`` with the level ``LOG_LEVEL`` of application.
    """
    logging.basicConfig(level=getattr(logging, app.config['LOG_LEVEL']))

def configure_cors(app):
    """ Configure Cross Origin Resource Sharing.
        Uses `Flask-CORS <https://flask-cors.readthedocs.io/>`_
    """
    cors.init_app(app)

def configure_api(app):
    """ Configure API Endpoints. """
    from resources.health import Health
    from resources.posts import Posts, Post 

    api.add_resource(Health, '/api/ping')
    api.add_resource(Posts, '/api/posts')
    api.add_resource(Post, '/api/posts/<ObjectId:post_id>')
    api.init_app(app)
    
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
