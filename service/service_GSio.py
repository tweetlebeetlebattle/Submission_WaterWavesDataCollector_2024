import arrow
import os
from dotenv import load_dotenv
import requests
import matplotlib.pyplot as plt
from datetime import datetime
from service.media_assets import coordinates

load_dotenv()

class GSioService:
    def __init__(self, params_list = ['waveHeight', 'waterTemperature'], coords = coordinates.location_coordinate_map):
        self.api_key = os.getenv("glassStormIoApiKey")  # 
        self.api_url = os.getenv("glassStormIoUrl") 
        self.coords = coords
        self.params_list = params_list

    def fetch_weather_data(self, lat, lng):
        start = arrow.now('UTC').floor('day')
        end = arrow.now('UTC').shift(days=1).floor('day')

        response = requests.get(
            self.api_url, 
            params={
                'lat': lat,
                'lng': lng,
                'params': ','.join(self.params_list),
                'start': start.timestamp(),
                'end': end.timestamp()
            },
            headers={
                'Authorization': self.api_key  
            }
        )

        data = response.json()
        return data

    def fetch_weather_for_all_locations(self):
        """Fetch weather data for all locations in the coordinates map."""
        weather_data_by_location = {}

        for location, (lat, lng) in self.coords.items():
            print(f"Fetching weather data for {location} (Lat: {lat}, Lng: {lng})")
            weather_data = self.fetch_weather_data(lat, lng)
            weather_data_by_location[location] = weather_data

        return weather_data_by_location

   