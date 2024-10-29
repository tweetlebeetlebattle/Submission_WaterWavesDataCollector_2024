from flask import Blueprint, jsonify
home_controller = Blueprint('home', __name__)

@home_controller.route('/')
def home():
    return jsonify(message="Welcome to the Flask Backend!")

@home_controller.route('/api/data')
def fetch_save_data():
    from service.service_shared import SharedService
    service = SharedService()
    return jsonify(service.fetch_save_all_data())

