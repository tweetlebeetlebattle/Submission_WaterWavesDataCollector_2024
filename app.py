from flask import Flask, jsonify
from test import testing
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask Backend!")

@app.route('/api/data')
def get_data():
    data = {
        "name": "Flask Backend",
        "version": "1.0",
        "status": "Running"
    }
    return jsonify(data)

@app.route('/test')
def test():
    message = testing()
    return jsonify(message), 404


if __name__ == '__main__':
    app.run(debug=True)
