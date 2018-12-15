from flask import Flask, request, redirect, Response, json, jsonify

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
# TODO fix all responses.
# Function to check validity of book object.
def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

# Function to check valid PUT object data.
def validPUTData(PUTObject):
    if ("name" in PUTObject and "price" in PUTObject):
        return True
    else: 
        return False

# Function to check valid PATH object data.
def validPATCHData(PATCHObject):
    if ("name" in PATCHObject or "price" in PATCHObject):
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
    for idx, book in enumerate(books):
        if book['isbn'] == isbn:
            return jsonify({
                "book": book
            })
        elif (idx + 1) == len(books):
            return jsonify({
                "Error": "That book does not exist.",
                "input_isbn": isbn,
                "book_isbn": book['isbn']
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
        # Set response parameters.
        response = Response(
                    "New Book Added!", 
                    status=201, 
                    mimetype='application/json')
        # Set response headers.
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response
    else: 
        # Create invalid book message.
        invalidBookOjbectErrorMsg = {
            "Error": "Invalid book format.",
            "helpString": "Book data should be in format of {'name': '<string>','price': '<int>','isbn': '<string>'}"
        }
        # Set error response.
        response = Response(
            json.dumps(invalidBookOjbectErrorMsg),
            status=400,
            mimetype='application/json'
        )
        return response
 
# PUT route to replace a book.
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    valid = validPUTData(request_data)
    if valid:
        book_replace = {
            'name': request_data['name'],
            'price': request_data['price'],
            'isbn': isbn
        }
        # Iterate over books list.  If a match is found replace that element in the list.
        for idx, book in enumerate(books):
            if book['isbn'] == isbn:
                del books[idx]
                books.insert(idx, book_replace)
                # Set response parameters. 204 for successful put.
                response = Response(
                            "", 
                            status=204, 
                            mimetype='application/json')
                # Set response headers.
                response.headers['Location'] = "/books/" + str(book_replace['isbn'])
                return response
            elif (idx + 1) == len(books): 
                # Create invalid book isbn message.
                invalidBookIsbnErrorMsg = {
                    "Error": "That book doesn't exist.  Please check the isbn.",
                    "helpString": "Verify that the isbn number exists.",
                }
                # Set error response.
                response = Response(
                    json.dumps(invalidBookIsbnErrorMsg),
                    status=400,
                    mimetype='application/json'
                )
                return response
    else:
        # Create invalid book message.
        invalidBookOjbectErrorMsg = {
            "Error": "Invalid book update format.",
            "helpString": "Book data should be in format of {'name': '<string>','price': '<int>'}"
        }
        # Set error response.
        response = Response(
            json.dumps(invalidBookOjbectErrorMsg),
            status=400,
            mimetype='application/json'
        )
        return response

# PATCH route to update fields in books data.
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    # Dictionary object to hold data to be updated.
    updated_book = {}
    # Checking which fields of data need to be updated.
    if("name" in request_data):
        updated_book['name'] = request_data['name']
    if("price" in request_data):
        updated_book['price'] = request_data['price']
    valid = validPATCHData(updated_book)
    if valid:
        for idx, book in enumerate(books):
            if book['isbn'] == isbn:
                book.update(updated_book)
                # Set response parameters. 204 for successful patch.
                response = Response(
                            "", 
                            status=204, 
                            mimetype='application/json')
                # Set response headers.
                response.headers['Location'] = "/books/" + str(isbn)
                return response
            elif (idx + 1) == len(books): 
                # Create invalid book isbn message.
                invalidBookIsbnErrorMsg = {
                    "Error": "That book doesn't exist.  Please check the isbn.",
                    "helpString": "Verify that the isbn number exists.",
                }
                # Set error response.
                response = Response(
                    json.dumps(invalidBookIsbnErrorMsg),
                    status=400,
                    mimetype='application/json'
                )
                return response
    else:
        # Create invalid book message.
        invalidBookOjbectErrorMsg = {
            "Error": "Invalid book update format.",
            "helpString": "Book data should be in format of {'name': '<string>'},{'price': '<int>'}, {'name': '<string>','price': '<int>'}"
        }
        # Set error response.
        response = Response(
            json.dumps(invalidBookOjbectErrorMsg),
            status=400,
            mimetype='application/json'
        )
        return response

# Server running.....
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
