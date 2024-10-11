import arrow
import requests
import matplotlib.pyplot as plt
from datetime import datetime
from media_assets.coordinates import location_coordinate_map

class GSioService:
    def __init__(self, api_key, coords, params_list):
        self.api_key = api_key
        self.coords = coords
        self.params_list = params_list

    def fetch_weather_data(self, lat, lng):
        """Fetch weather data for a specific latitude and longitude."""
        start = arrow.now('UTC').floor('day')
        end = arrow.now('UTC').shift(days=1).floor('day')

        response = requests.get(
            'https://api.stormglass.io/v2/weather/point',
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

    def extract_time_series(self, data, param_name):
        """Extract time series data for the specified weather parameter."""
        times = [datetime.fromisoformat(hour['time'].replace('Z', '')) for hour in data['hours']]
        param_values = [hour[param_name]['sg'] for hour in data['hours']]

        return times, param_values

    def plot_wave_heights(self, times, wave_heights):
        """Plot wave heights over time."""
        plt.figure(figsize=(10, 6))
        plt.plot(times, wave_heights, label='Wave Height (sg)', color='blue', marker='o')
        plt.xlabel('Time')
        plt.ylabel('Wave Height (m)')
        plt.title('Wave Height over Time')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_water_temperatures(self, times, water_temps):
        """Plot water temperatures over time."""
        plt.figure(figsize=(10, 6))
        plt.plot(times, water_temps, label='Water Temperature (sg)', color='red', marker='o')
        plt.xlabel('Time')
        plt.ylabel('Water Temperature (°C)')
        plt.title('Water Temperature over Time')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# Usage example:
if __name__ == "__main__":
    api_key = 'f6dfddca-7515-11ef-968a-0242ac130004-f6dfdeb0-7515-11ef-968a-0242ac130004'
    coords = location_coordinate_map
    params_list = ['waveHeight', 'waterTemperature']

    # Instantiate the service
    weather_service = WeatherService(api_key, coords, params_list)

    # Fetch weather data for all locations
    weather_data_by_location = weather_service.fetch_weather_for_all_locations()

    # Example for a specific location
    location = 'Location Name'
    data = weather_data_by_location.get(location)

    if data:
        # Extract time series for wave heights and water temperatures
        times, wave_heights = weather_service.extract_time_series(data, 'waveHeight')
        _, water_temps = weather_service.extract_time_series(data, 'waterTemperature')

        # Plot the results
        weather_service.plot_wave_heights(times, wave_heights)
        weather_service.plot_water_temperatures(times, water_temps)
