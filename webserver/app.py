from flask import Flask



app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == 'main':
    app.run(debug=True)