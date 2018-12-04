from flask import Flask, request, redirect, jsonify

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

# Function to check validity of book object.
def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

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

# POST /books - add a new book.
@app.route('/books', methods=['POST'])
def add_book():
    book_data = request.get_json()
    # Check if valid.
    valid = validBookObject(book_data)
    if valid:
        # If valid only use revelant data.
        new_book = {
            "name": book_data['name'],
            "price": book_data['price'],
            "isbn": book_data['isbn']
        }
        books.append(new_book)
        #return redirect("http://localhost:5000/books", code=302)
        return jsonify({
            "New Book": new_book
        })
    else: 
        return jsonify({
            "Error": "Invalid book format."
        })

    
# Server running.....
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
