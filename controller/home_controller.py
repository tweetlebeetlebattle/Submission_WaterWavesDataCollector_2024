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
    # from service.service_gif import MeteoGifService
    # service = MeteoGifService()
    # data = service.fetch_gif_data()

    # from service.service_HTML import MeteoHTMLService
    # service = MeteoHTMLService()
    # data = service.fetch_meteo_data()

    from service.service_GSio import GSioService
    service = GSioService()
    data = service.fetch_weather_for_all_locations()

    return jsonify(data)

