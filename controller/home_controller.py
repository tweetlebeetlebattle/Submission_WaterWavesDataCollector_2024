from flask import Blueprint, jsonify
from test import testing
home_controller = Blueprint('home', __name__)

@home_controller.route('/')
def home():
    return jsonify(message="Welcome to the Flask Backend!")

@home_controller.route('/api/data')
def get_data():
    from repository.repository_gif import GifDataRepository
    repository = GifDataRepository()  
    data = repository.read_all_data() 
    return jsonify(data)

@home_controller.route('/test')
def test():
    # from repository.repository_locations import LocationsRepository
    # repository = LocationsRepository()
    # data = repository.get_location_id_by_name("Бургас");
    # return jsonify(data)
    from service.service_gif import MeteoGifService
    service = MeteoGifService()
    data = service.fetch_gif_data()
    return jsonify(data)

