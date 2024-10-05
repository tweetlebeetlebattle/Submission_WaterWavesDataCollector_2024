

import arrow
import requests
from media_assets.coordinates import location_coordinate_map

start = arrow.now('UTC').floor('day')
end = arrow.now('UTC').shift(days=1).floor('day')
lat = 43.2141
lng = 27.9147
params_list = ['waveHeight', 'waterTemperature']
api_key = 'f6dfddca-7515-11ef-968a-0242ac130004-f6dfdeb0-7515-11ef-968a-0242ac130004'
coords = location_coordinate_map

def fetch_weather_data(lat, lng, params_list, api_key):
    start = arrow.now('UTC').floor('day')
    end = arrow.now('UTC').shift(days=1).floor('day')

    response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': lat,
            'lng': lng,
            'params': ','.join(params_list),
            'start': start.timestamp(),  
            'end': end.timestamp()       
        },
        headers={
            'Authorization': api_key
        }
    )

    data = response.json()

    return data

def fetchWeatherForAllLocations(coords, params_list, api_key):
    weather_data_by_location = {}

    # Loop through each location and its coordinates
    for location, (lat, lng) in coords.items():
        print(f"Fetching weather data for {location} (Lat: {lat}, Lng: {lng})")
        weather_data = fetch_weather_data(lat, lng, params_list, api_key)
        weather_data_by_location[location] = weather_data

    return weather_data_by_location

# times = [datetime.fromisoformat(hour['time'].replace('Z', '')) for hour in data['hours']]
# wave_heights_sg = [hour['waveHeight']['sg'] for hour in data['hours']]
# water_temps_sg = [hour['waterTemperature']['sg'] for hour in data['hours']]

# # Plotting wave heights
# plt.figure(figsize=(10, 6))
# plt.plot(times, wave_heights_sg, label='Wave Height (sg)', color='blue', marker='o')
# plt.xlabel('Time')
# plt.ylabel('Wave Height (m)')
# plt.title('Wave Height over Time')
# plt.xticks(rotation=45)
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# # Plotting water temperatures
# plt.figure(figsize=(10, 6))
# plt.plot(times, water_temps_sg, label='Water Temperature (sg)', color='red', marker='o')
# plt.xlabel('Time')
# plt.ylabel('Water Temperature (°C)')
# plt.title('Water Temperature over Time')
# plt.xticks(rotation=45)
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()