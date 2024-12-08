import arrow
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
from service.media_assets import coordinates

load_dotenv()

class GSioService:
    def __init__(self, params_list=['waveHeight', 'waterTemperature', 'windSpeed'], coords=coordinates.location_coordinate_map):
        from repository.repository_GSio import GlassStormIoDataRepository
        from repository.repository_GSio import DailyGlassStormReadingRepository
        from service.service_utils import ServiceUtils
        self.service_utils = ServiceUtils()
        self.api_key = os.getenv("glassStormIoApiKey")
        self.api_url = os.getenv("glassStormIoUrl")
        self.coords = coords
        self.params_list = params_list
        self.glass_storm_repo = GlassStormIoDataRepository()
        self.daily_glass_storm_repo = DailyGlassStormReadingRepository()

    def insert_glass_storm_data(self, wave_read, wave_unit_id, temp_read, temp_unit_id, wind_speed_read, wind_unit_id, date, location_id):
        return self.glass_storm_repo.insert_data(wave_read, wave_unit_id, temp_read, temp_unit_id, wind_speed_read, wind_unit_id, date, location_id)

    def get_all_glass_storm_data(self):
        return self.glass_storm_repo.read_all_data()

    def delete_all_glass_storm_data(self):
        return self.glass_storm_repo.delete_all_data()

    def insert_daily_glass_storm_reading(self, daily_wave_max, daily_wave_min, daily_wave_avg, wave_unit_id,
                                         daily_temp_max, daily_temp_min, daily_temp_avg, temp_unit_id,
                                         daily_wind_max, daily_wind_min, daily_wind_avg, wind_unit_id,
                                         date, location_id):
        return self.daily_glass_storm_repo.insert_data(
            daily_wave_max, daily_wave_min, daily_wave_avg, wave_unit_id,
            daily_temp_max, daily_temp_min, daily_temp_avg, temp_unit_id,
            daily_wind_max, daily_wind_min, daily_wind_avg, wind_unit_id,
            date, location_id
        )

    def get_all_daily_glass_storm_readings(self):
        return self.daily_glass_storm_repo.get_all_data()

    def delete_all_daily_glass_storm_readings(self):
        return self.daily_glass_storm_repo.delete_all_data()

    def fetch_weather_data(self, lat, lng, location):
        start = arrow.now('UTC').floor('day').shift(minutes=1)

        end = arrow.now('UTC').floor('day').shift(hours=23, minutes=59)

        try:
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

            # Check if response was successful
            if response.status_code != 200:
                print(f"Failed to fetch data for coordinates ({lat}, {lng}): {response.status_code}")
                self.service_utils.insert_data_fetching_log(f"Failed to fetch data for coordinates ({lat}, {lng}): {response.status_code}")
                return []

            data = response.json()
            weather_data_list = []

            # Process each hourly entry, ensuring data is available
            for entry in data.get("hours", []):
                time = datetime.fromisoformat(entry["time"])

                # Collect water temperature values and calculate the average
                water_temps = entry.get("waterTemperature", {})
                avg_water_temp = (sum(water_temps.values()) / len(water_temps)
                                  if water_temps else None)

                # Collect wave height values and calculate the average
                wave_heights = entry.get("waveHeight", {})
                avg_wave_height = (sum(wave_heights.values()) / len(wave_heights)
                                   if wave_heights else None)
                
                wind_speed = entry.get("windSpeed", {})
                avg_wind_speed = (sum(wind_speed.values()) / len(wind_speed)
                                   if wind_speed else None)

                # Only add entry if there's at least one valid reading
                if avg_water_temp is not None or avg_wave_height is not None or avg_wind_speed is not None:
                    weather_data_list.append({
                        "Location": location,
                        "time": time,
                        "water_temp": avg_water_temp,
                        "wave_height": avg_wave_height,
                        "wind_speed": avg_wind_speed
                    })
            
            # Log if no data was found
            if not weather_data_list:
                print(f"No data found for ({location})")

            return weather_data_list

        except Exception as e:
            print(f"Error fetching data for coordinates ({lat}, {lng}): {e}")
            return []


    def fetch_weather_for_all_locations(self):
        weather_data_by_location = {}

        for location, (lat, lng) in self.coords.items():
            print(f"Fetching weather data for {location} (Lat: {lat}, Lng: {lng})")
            weather_data = self.fetch_weather_data(lat, lng, location)
            weather_data_by_location[location] = weather_data

        return weather_data_by_location
