from flask import Blueprint, jsonify
from test import testing

home_controller = Blueprint('home', __name__)

@home_controller.route('/')
def home():
    return jsonify(message="Welcome to the Flask Backend!")

@home_controller.route('/api/data')
def get_data():
    data = {
        "name": "Flask Backend",
        "version": "1.0",
        "status": "Running"
    }
    return jsonify(data)

@home_controller.route('/test')
def test():
    message = testing()
    return jsonify(message), 404
