from flask import flask

app = Flask(__name__)
print(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

app.run(port=5000)
