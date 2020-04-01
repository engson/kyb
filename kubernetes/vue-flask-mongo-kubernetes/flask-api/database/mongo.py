from flask_pymongo import PyMongo

"""Database object"""
mongo = PyMongo()

def configure_mongodb(app):
    """ Configure MongoDB.
        Uses `Flask-PyMongo <https://flask-pymongo.readthedocs.org/>`_
    """
    mongo.init_app(app)
