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
    print("Books written by")
    pprint(list(result))

    # Cont aggregation
    # Find all books written by author from same city.


    pipeline_test = [  
        { 
            "$lookup": {
                "from": "authors",
                "localField":"author",
                "foreignField":"_id",
                "as": "ref_author",
            }
        },
        {
            "$unwind":"$ref_author"
        },
        {
            "$match": {
                "$expr": {
                    "$eq": ["$city", "$ref_author.city"]
                }
            }
        },
        {
            "$project": {
                "_id":1,
                "no_of_books_sold":1
            }

        }
    ]   

    result_test = books.aggregate(pipeline_test)
    print("Books same authors")
    pprint(list(result_test))

    # Find number of books each author have sold

    pipeline_test = [  
        {
            "$lookup": {
                "from": "authors",
                "localField":"author",
                "foreignField":"_id",
                "as": "ref_author",
            }
        },
        {
            "$unwind": "$ref_author"
        },
        {
            "$group": { 
                "_id":"$ref_author",
                "total_books_sold": {
                    "$sum": "$no_of_books_sold"
                }
            }
        },{
            "$project":{
                "total_books_sold":"$total_books_sold",
                "email":"$_id.email",
                "_id":"$_id._id"
                
            }
        }

    ]
    
    result_test = books.aggregate(pipeline_test)
    print("Books authors")
    pprint(list(result_test))


def query_books():

    # Count number of books availible.
    book_count = books.count_documents(filter={})
    print("num of books", book_count)

    # Want to find all books with specific author

    query_no_books = {
        "no_of_books_sold": {
                "$lt": 5
            }
    }

    result = books.find(query_no_books)
    print("Query_no_books:")
    pprint(list(result))


    result = books.find({}).sort([("date_written",pymongo.DESCENDING)]).limit(2)
    print("Query sort limit:")
    pprint(list(result))

    # Wrappers
    result = books.find({}).max_time_ms(1)
    print("Query wrap max time ms:")
    pprint(list(result))

    # Snapshot depricated: use hint { _id: 1} instead, 
    #   to prevent cursor from returning a document more than once. 

    # runCommand({"drop":"test"}) 


if __name__ == "__main__": # Only ran when this is main module (not imported)
    init_db()
    aggregate_books()
    #query_books()