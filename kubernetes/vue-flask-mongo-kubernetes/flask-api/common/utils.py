from bson import ObjectId
from flask.json import JSONEncoder

class MongoJSONEncoder(JSONEncoder):
    """ Customize JSONEncoder to convert ObjectId -> string
    """
    def default(self, o): # pylint: disable=method-hidden
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)
