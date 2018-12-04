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

# GET single book
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    for book in books:
        if book['isbn'] == isbn:
            return jsonify({
                "book": book
            })
        else:
            return jsonify({
                "Error": "That book does not exist."
            })

# GET /books
@app.route('/books')
def get_books():
    return jsonify({ 
        "books": books
    })

# Server running.....
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
