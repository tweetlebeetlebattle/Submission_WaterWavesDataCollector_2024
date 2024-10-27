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

    # from service.service_GSio import GSioService
    # service = GSioService()
    # data = service.fetch_weather_for_all_locations()

    # return jsonify(data)

    # from service.service_utils import ServiceUtils
    # service = ServiceUtils()
    # return jsonify(service.get_location_id_by_name("Еминe"))

    from service.service_shared import SharedService
    service = SharedService()
    # service.record_gif_data()
    # service.record_GSio_data()
    # service.record_HTML_data()
    
    # print(service.get_all_html_data())
    # print(service.get_all_gif_data())
    # print(service.get_all_glass_storm_data())

    # service.delete_all_html_data()
    # service.delete_all_glass_storm_data()
    # service.delete_all_gif_data()

    # service.insert_daily_html_reading()
    service.insert_daily_gif_reading()
    # service.insert_daily_glass_storm_reading()

    return jsonify(1)
