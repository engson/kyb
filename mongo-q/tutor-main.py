from pymongo import MongoClient
from bson.objectid import ObjectId
import pymongo
import bson

from bson.code import Code

import json
from pathlib import Path
import pathlib
import datetime
import dateutil.parser

from pprint import pprint

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

    def get_counts():
        b_c = books.count_documents(filter={})
        a_c = authors.count_documents(filter={})
        c_c = cities.count_documents(filter={})
        return b_c, a_c, c_c

    if(refresh):
        clear_collections()

    file = Path.cwd() / 'mongo-q/data/data.json'

    if not file.exists():
        print(f"{file} does not exist")
    else:
        b_c, a_c, c_c = get_counts()

        if not (b_c == 0 or a_c == 0 or c_c == 0):
            print(f"Collections are filled with data: books:{b_c} authors:{a_c} city:{c_c}" )
        else:
            # We need to clear the database, and replace all the data
            clear_collections()

            books.create_index("_id")
            authors.create_index("_id")
            cities.create_index("_id")

            with file.open() as json_file: 
                data = json.load(json_file)
                
                # End result length
                num_cities = len(data["cities"])
                num_books = len(data["books"])
                num_authors = len(data["authors"])

                for city in data["cities"]:
                    cities.insert_one(city)

                for author in data["authors"]:
                    #Update author city reference
                    city_id = db.cities.find_one({"name": author.get("city")}).get("_id")
                    author.update({"city":city_id})

                    authors.insert_one(author)

                for book in data["books"]:
                    date_written = book.get("date_written")
                    book.update({"date_written":dateutil.parser.parse(date_written)}) # update field as DateTime object
                    # Update city field with Id reference.
                    city_id = db.cities.find_one({"name": book.get("city")}).get("_id")
                    book.update({"city":city_id})
                    # Update author field with Id reference.
                    author_id = db.authors.find_one({"email": book.get("author")}).get("_id")
                    book.update({"author":author_id})

                    books.insert_one(book)

                num_books = len(data["books"])
                num_authors = len(data["authors"])
                num_cities = len(data["cities"])
                
                book_c, authors_c, cities_c = get_counts()
                if(num_books != book_c or num_authors != authors_c or num_cities != cities_c):
                    raise ValueError("Wrong number of documents in collections")

                

def aggregate_books():

    startDate = datetime.datetime(2019, 1, 1, 23, 59) # 2019-01-01 23:59:00
    endDate = datetime.datetime(2019, 10, 1, 23, 59) # 2019-06-01 23:59:00

    pipeline = [
        {   # Filter documents that are outside of date range
            "$match": { 
                "date_written" : {
                    "$gte": startDate,
                    "$lt": endDate
                }
            }
        },
        {   # Groups input documents by the specified _id expression 
            #  and for each distinct grouping
            "$group": { 
                "_id":"$city",
                "total_books_written": {
                    "$sum": "$no_of_books_sold"
                }
            }
        },{ # Performs a left outer join to an unsharded collection in the same database 
            #  to filter in documents from the “joined” collection for processing.
            "$lookup": {
                "from": "cities",
                "localField":"_id",
                "foreignField":"_id",
                "as": "refcity",
            }
        },{ # Deconstructs an array field from the input documents to output a document for each element.
            "$unwind":"$refcity"
        },
        {
            "$project": { # Project document in this format,
                "_id":0,
                "total_books_written": "$total_books_written",
                "city":"$refcity.name"
            }
        },
        {
            # Sort on decending on total_books_written tag
            "$sort": {
                "total_books_written":pymongo.DESCENDING
            }
        },
        {
            "$limit": 3
        }
    ]

    result = books.aggregate(pipeline)

    pprint(list(result))

def query_books():

    


    pass

if __name__ == "__main__": # Only ran when this is main module (not imported)
    init_db(True)
    aggregate_books()