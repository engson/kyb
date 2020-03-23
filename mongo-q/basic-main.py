import datetime
import pprint

import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['test_database']
print(db.name)

post = {"author": "Mike","text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()}

c_posts = db.posts # select posts collection in test_database
print(c_posts)

post_id = c_posts.insert_one(post).inserted_id

print(post_id)
print(db.list_collection_names())
pprint.pprint(c_posts.find_one())


print(c_posts.find_one({"author": "Mike"}))

pprint.pprint(c_posts.find_one({"_id": post_id}))

post_id_as_str = str(post_id)
print(c_posts.find_one({"_id": post_id_as_str}) ) # Mone

from bson.objectid import ObjectId

def get(post_id):
    # Convert from string to ObjectId:
    document = client.db.collection.find_one({'_id': ObjectId(post_id)})
    return document

new_posts = [{"author": "Mike","text": "Another Post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()},
    {"author": "Eliot","text": "My first blog post!",
    "title":"MongoDB is fun",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()}]

result = c_posts.insert_many(new_posts)
print(result.inserted_ids)

for post in c_posts.find():
    pprint.pprint(post)

print(c_posts.count_documents(filter={}))
print(c_posts.count_documents(filter={"author":"Mike"}))

# Find only documents date greater than a specific datetime.
d = datetime.datetime(2009, 11, 12, 12)
for post in c_posts.find({"date":{"$gt":d}}).sort("author"):
    pprint.pprint(post)

# Indexing

result = db.profiles.create_index([('user_id', pymongo.ASCENDING)],unique=True)
print(sorted(list(db.profiles.index_information())))
user_profiles = [
    {'user_id': 211, 'name': 'Luke'},{'user_id': 212, 'name': 'Ziltoid'}
]
try:
    result = db.profiles.insert_many(user_profiles)
except pymongo.errors.BulkWriteError as e:
    print("Id is already present is Database:",e)

new_profile = {'user_id':213,"name":"Drew"}
duplicate_profile = {'user_id':213,"name":"Tommy"}
try:
    result = db.profiles.insert_one(new_profile)
    result = db.profiles.insert_one(duplicate_profile)
except pymongo.errors.DuplicateKeyError as e: 
    print(e)