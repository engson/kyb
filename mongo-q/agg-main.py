import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.int64 import Int64
import bson

import json
from pathlib import Path
import pathlib
import datetime
import dateutil.parser

client = MongoClient('localhost', 27017)

db = client['test_db']
books = db.books
authors = db.authors
cities = db.cities

def init_db(refresh=False):

    def clear_collections():
        books.remove({})
        authors.remove({})
        cities.remove({})

    if(refresh):
        clear_collections()

    file = Path.cwd() / 'mongo-q/data/data.json'

    if not file.exists():
        print(f"{file} does not exist")
    else:
        b_c = books.count_documents(filter={})
        a_c = authors.count_documents(filter={})
        c_c = cities.count_documents(filter={})

        if(b_c == 0 or a_c == 0 or c_c == 0):
            # We need to clear the database, and replace all the data
            clear_collections()

            #ts = time.time()
            #isodate = datetime.datetime.fromtimestamp(ts, None)

            books.create_index("_id")
            authors.create_index("_id")
            cities.create_index("_id")

            with file.open() as json_file:
                data = json.load(json_file)
                print("cities")
                for c in data["cities"]:
                    print(c)
                    cities.insert_one(c)
                print("Books")
                for b in data["books"]: # _id, data_written, no_of_books_sold, city
                    print(b)
                    date_written = b.get("date_written")
                    b.update({"date_written":dateutil.parser.parse(date_written)}) # update field as DateTime object
                    b.update({"no_of_books_sold":int(b.get("no_of_books_sold"))})
                    books.insert_one(b)
                print("authors")
                for a in data["authors"]:
                    print(a)
                    authors.insert_one(a)
                
        else:
            print(f"Collections are filled with data. books:{b_c} authors:{a_c} cities:{c_c}" )


def aggregate_books():
    print(books)

    startDate = datetime.datetime(2009, 11, 12, 12)

    books.aggregate([
    ])

if __name__ == "__main__": # Only ran when this is main module (not imported)
    init_db(True)
    aggregate_books()