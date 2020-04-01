from flask import jsonify, request, make_response
from flask_restful import Resource
from pymongo.collection import ReturnDocument

from database.mongo import mongo

class Posts(Resource):
    def get(self):
        posts_db = mongo.db.posts
        posts = list(posts_db.find())
        return make_response(jsonify(posts), 200)

    def post(self):
        post = request.get_json()
        posts_db = mongo.db.posts
        post_id = posts_db.insert(post)
        new_post = posts_db.find_one({'_id': post_id })
        return make_response(new_post, 200)
        
class Post(Resource):
    def put(self, post_id):
        post = request.get_json()
        posts_db = mongo.db.posts
        new_post = posts_db.find_one_and_replace(
            {'_id': post_id}, 
            post, 
            return_document=ReturnDocument.AFTER
        )
        if (new_post):
            return make_response(new_post, 200)
        else:
            return make_response('', 404) 
    
    def delete(self, post_id):
        posts_db = mongo.db.posts
        result = posts_db.delete_one({'_id': post_id})
        if (result.deleted_count):
            return make_response('', 204)
        else:
            return make_response('', 404)

    def get(self, post_id):
        posts_db = mongo.db.posts
        post = posts_db.find_one(post_id)
        if (post):
            return make_response(post, 200)
        else:
            return make_response('', 404)

