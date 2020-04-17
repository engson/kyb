from datetime import datetime

from flask import make_response, abort, request

#UTIL FUNCTIONS
def get_timestamp():
    return datetime.utcnow().isoformat()

def health():
    return "pong"

BOOKS = {
    "book_name_1":{
        "name":"book_name_1",
        "date_written":"2019-01-09T00:00:00.000+0000",
        "no_of_books_sold":2, 
        "city":"City-A",
        "author":"abc@live.in"
    },
    "book_name_2":{
        "name":"book_name_2",
        "date_written":"2019-02-10T00:00:00.000+0000",
        "no_of_books_sold":3, 
        "city":"City-B",
        "author":"def@live.in"
    },
    "book_name_3":{
        "name":"book_name_3",
        "date_written":"2019-03-10T04:00:00.000+0000",
        "no_of_books_sold":5, 
        "city":"City-B",
        "author":"abc@live.in"
    }
}

def read_all():
    return [BOOKS[key] for key in sorted(BOOKS.keys())]

def read_one(bookname):
    # Does the person exist in people?
    if bookname in BOOKS:
        book = BOOKS.get(bookname)
        return book
    # otherwise, nope, not found
    else:
        abort(
            404, f"Book with name {bookname} not found"
        )

def create():
    book = request.get_json()
    print(book)
    bookname = book.get("name",None)

    if bookname is not None and bookname not in BOOKS:
        BOOKS.update({
            bookname: {
                "name":bookname,
                "date_written":get_timestamp(),
                "no_of_books_sold":book.get("amount",0),
                "city":book.get("city",None),
                "author":book.get("author",None)
            }
        })
        response = make_response(BOOKS.get(bookname),201)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        abort(
            400, f"Book must have a name"
        )
        
def delete(bookname):
    if bookname in BOOKS:
        del BOOKS[bookname]
        return make_response(
            f"{bookname} successfully deleted", 200
        )
    else:
        abort(
            404, f"Book with name {bookname} not found"
        )
