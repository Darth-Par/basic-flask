from flask import Flask, jsonify

app = Flask(__name__)

books = [
    {
        "name": "Green Eggs and Ham",
        "price": 7.99,
        "isbn": 9780
    },
    {
        "name": "The Cat In The Hat",
        "price": 3.99,
        "isbn": 9880
    }
]

# GET /
@app.route('/')
def hello_world():
    return 'Hello World!'

# GET /books
@app.route('/books')
def get_books():
    return jsonify({ 
        "books": books
    })

# Server running.....
app.run(port=5000)
