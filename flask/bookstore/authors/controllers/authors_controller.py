
from datetime import datetime

from flask import make_response, abort, request

#UTIL FUNCTIONS
def get_timestamp():
    return datetime.utcnow().isoformat()

AUTHORS = {
    "abc@live.in":{
        "fname":"Per",
        "lname":"Olav",
        "age":45,
        "city":"City-A",
        "email":"abc@live.in"
    },
    "def@live.in":{
        "fname":"Jon",
        "lname":"Olav",
        "age":67,
        "city":"City-B",
        "email":"def@live.in"
    },
    "hij@live.in":{
        "fname":"Tor",
        "lname":"Petter",
        "age":33,
        "city":"City-C",
        "email":"abc@live.in"
    }
}

def read_all_authors():
    return [AUTHORS[key] for key in sorted(AUTHORS.keys())]

def read_one(email):
    # Does the person exist in people?
    if email in AUTHORS:
        author = AUTHORS.get(email)
        return author
    # otherwise, nope, not found
    else:
        abort(
            404, f"Author with email {email} not found"
        )

def create():
    author = request.get_json()
    print("Attemtping to create:",author)
    email = author.get("email",None)

    if email is not None and email not in AUTHORS:
        AUTHORS.update({
            email: {
                "fname":author.get("fname",None),
                "lname":author.get("lname",None),
                "age":author.get("age",None),
                "city":author.get("city",None),
                "email":email,
            }
        })

        author = AUTHORS.get(email) 
        assert author is not None
        response = make_response(author,201)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        abort(
            400, f"Author must have an email"
        )
        
def delete(email):
    if email in AUTHORS:
        del AUTHORS[email]
        return make_response(
            f"{email} of author successfully deleted", 200
        )
    else:
        abort(
            404, f"Author with email {email} not found"
        )
