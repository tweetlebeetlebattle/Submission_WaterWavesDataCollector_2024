from datetime import datetime, timedelta

class SharedService:
    def __init__(self):
        from service.service_gif import MeteoGifService
        from service.service_GSio import GSioService
        from service.service_HTML import MeteoHTMLService
        from service.service_utils import ServiceUtils
        self.serv_HTML = MeteoHTMLService()
        self.serv_GSio = GSioService()
        self.serv_gif = MeteoGifService()
        self.serv_utils = ServiceUtils()

    def record_HTML_data(self):
        meteo_data = self.serv_HTML.fetch_meteo_data()
        
        wave_unit_id = self.serv_utils.get_unit_id_by_name("Метра")
        temp_unit_id = self.serv_utils.get_unit_id_by_name("°C")
        date = datetime.now().date()

        for data in meteo_data:
            location_name = data['location']
            wave_height_in_bala = data['waveHeightInBala']
            water_temp = data['waterTempInC']

            location_name = data['location'].strip()
            location_id = self.serv_utils.get_location_id_by_name(location_name)
            
            wave_read = self.serv_utils.transform_bala_to_meters(wave_height_in_bala)

            print("Wave Height (meters):", wave_read)
            print("Wave Unit ID:", wave_unit_id)
            print("Water Temperature:", water_temp)
            print("Temperature Unit ID:", temp_unit_id)
            print("Date:", date)
            print("Location ID:", location_id)
            print("Location name:", location_name)
            print()
            self.serv_HTML.insert_html_data(
                wave_read, wave_unit_id, water_temp, temp_unit_id, date, location_id
            )
    
    def record_gif_data(self):
        gif_data = self.serv_gif.fetch_gif_data()
        wave_unit_id = self.serv_utils.get_unit_id_by_name("Метра")

        for data in gif_data:
            frame_id = data['id']
            location_name = data['location']
            wave_read = data['index']  
            location_id = self.serv_utils.get_location_id_by_name(location_name)

            if 0 <= frame_id <= 8:
                date = datetime.now().date()
            elif 9 <= frame_id <= 16:
                date = (datetime.now() + timedelta(days=1)).date()
            elif 17 <= frame_id <= 24:
                date = (datetime.now() + timedelta(days=2)).date()
            else:
                print(f"Skipping frame with ID {frame_id} as it falls outside the specified range.")
                continue

            print("Frame ID:", frame_id)
            print("Wave Height (from GIF):", wave_read)
            print("Wave Unit ID:", wave_unit_id)
            print("Date:", date)
            print("Location ID:", location_id)
            print("Location name:", location_name)
            print()

            self.serv_gif.insert_gif_data(wave_read, wave_unit_id, date, location_id)

    def record_GSio_data(self):
        wave_unit_id = self.serv_utils.get_unit_id_by_name("Метра")
        temp_unit_id = self.serv_utils.get_unit_id_by_name("°C")
        wind_speed_unit_id = self.serv_utils.get_unit_id_by_name("м/с")
        
        all_location_data = self.serv_GSio.fetch_weather_for_all_locations()

        for location, weather_data_list in all_location_data.items():
            location_id = self.serv_utils.get_location_id_by_name(location)
            
            for data in weather_data_list:
                date = data['time'].date()
                wave_read = data.get('wave_height')
                temp_read = data.get('water_temp')
                wind_speed_read = data.get('wind_speed')

                print("Location:", location)
                print("Date:", date)
                print("Wave Height (meters):", wave_read)
                print("Wave Unit ID:", wave_unit_id)
                print("Water Temperature:", temp_read)
                print("Temperature Unit ID:", temp_unit_id)
                print("Wind Speed:", wind_speed_read)
                print("Wind Speed Unit ID:", wind_speed_unit_id)
                print("Location ID:", location_id)
                print()

                self.serv_GSio.insert_glass_storm_data(
                    wave_read, wave_unit_id, temp_read, temp_unit_id, 
                    wind_speed_read, wind_speed_unit_id, date, location_id
                )

    def get_all_html_data(self):
        return self.serv_HTML.get_all_html_data()
    
    def get_all_glass_storm_data(self):
        return self.serv_GSio.get_all_glass_storm_data()
    
    def get_all_gif_data(self):
        return self.serv_gif.get_all_gif_data()
    
    def delete_all_html_data(self):
        return self.serv_HTML.delete_all_html_data()
    
    def delete_all_glass_storm_data(self):
        return self.serv_GSio.delete_all_glass_storm_data()
    
    def delete_all_gif_data(self):
        return self.serv_gif.delete_all_gif_data()
    
    def insert_daily_gif_reading(self):
        # Initialize a dictionary to hold data aggregated by (location_id, date)
        daily_data = {}
        
        # Fetch all GIF data for aggregation
        all_gif_data = self.serv_gif.get_all_gif_data()
        
        for data in all_gif_data:
            location_id = data['LocationId']  # Updated key
            date = data['Date']  # Updated key
            wave_height = data['WaveRead']  # Updated key
            wave_unit_id = data['WaveUnitId']  # Updated key

            # Ensure the location_id and date are not None
            if location_id is not None and date is not None and wave_height is not None:
                key = (location_id, date)

                if key not in daily_data:
                    daily_data[key] = {
                        'wave_heights': [],
                        'wave_unit_id': wave_unit_id  # Store wave unit ID
                    }
                
                daily_data[key]['wave_heights'].append(wave_height)
        
        # Now process each location's daily data for min, max, and average
        for (location_id, date), values in daily_data.items():
            wave_heights = values['wave_heights']
            
            daily_wave_max = max(wave_heights)
            daily_wave_min = min(wave_heights)
            daily_wave_avg = sum(wave_heights) / len(wave_heights)
            wave_unit_id = values['wave_unit_id']
            
            # Insert the daily reading into the database
            self.serv_gif.insert_daily_gif_reading(
                daily_wave_max, daily_wave_min, daily_wave_avg, 
                wave_unit_id, date, location_id
            )

    def insert_daily_glass_storm_reading(self):
        # Initialize a dictionary to hold data aggregated by (location_id, date)
        daily_data = {}
        
        # Fetch all Glass Storm data for aggregation
        all_glass_storm_data = self.serv_GSio.get_all_glass_storm_data()
        
        for data in all_glass_storm_data:
            location_id = data['location_id']
            date = data['date']
            wave_height = data['wave_height']
            temp = data['water_temp']
            wind_speed = data['wind_speed']
            
            key = (location_id, date)
            
            if key not in daily_data:
                daily_data[key] = {
                    'wave_heights': [],
                    'temps': [],
                    'wind_speeds': [],
                    'wave_unit_id': data['wave_unit_id'],
                    'temp_unit_id': data['temp_unit_id'],
                    'wind_unit_id': data['wind_unit_id']
                }
            
            daily_data[key]['wave_heights'].append(wave_height)
            daily_data[key]['temps'].append(temp)
            daily_data[key]['wind_speeds'].append(wind_speed)
        
        # Now process each location's daily data for min, max, and average
        for (location_id, date), values in daily_data.items():
            wave_heights = values['wave_heights']
            temps = values['temps']
            wind_speeds = values['wind_speeds']
            
            daily_wave_max = max(wave_heights)
            daily_wave_min = min(wave_heights)
            daily_wave_avg = sum(wave_heights) / len(wave_heights)
            
            daily_temp_max = max(temps)
            daily_temp_min = min(temps)
            daily_temp_avg = sum(temps) / len(temps)
            
            daily_wind_max = max(wind_speeds)
            daily_wind_min = min(wind_speeds)
            daily_wind_avg = sum(wind_speeds) / len(wind_speeds)

            wave_unit_id = values['wave_unit_id']
            temp_unit_id = values['temp_unit_id']
            wind_unit_id = values['wind_unit_id']
            
            # Insert the daily reading into the database
            self.serv_GSio.insert_daily_glass_storm_reading(
                daily_wave_max, daily_wave_min, daily_wave_avg, 
                wave_unit_id, daily_temp_max, daily_temp_min, daily_temp_avg, 
                temp_unit_id, daily_wind_max, daily_wind_min, daily_wind_avg, 
                wind_unit_id, date, location_id
            )

    def insert_daily_html_reading(self):
        # Initialize a dictionary to hold data aggregated by (location_id, date)
        daily_data = {}

        # Fetch all HTML data for aggregation
        all_html_data = self.serv_HTML.get_all_html_data()

        for data in all_html_data:
            # Use the correct keys from the response
            location_id = data.get('LocationId')  # Updated key
            date = data.get('Date')  # Updated key
            wave_height = data.get('WaveRead')  # Updated key
            temp = data.get('TempRead')  # Updated key

            # Ensure values are not None before processing
            if location_id is not None and date is not None and wave_height is not None:
                key = (location_id, date)

                if key not in daily_data:
                    daily_data[key] = {
                        'wave_heights': [],
                        'temps': [],
                        'wave_unit_id': data.get('WaveUnitId'),  # Updated key
                        'temp_unit_id': data.get('TempUnitId')   # Updated key
                    }

                daily_data[key]['wave_heights'].append(wave_height)
                
                # Only append temperature if it's not None
                if temp is not None:
                    daily_data[key]['temps'].append(temp)

        # Now process each location's daily data for min, max, and average
        for (location_id, date), values in daily_data.items():
            wave_heights = values['wave_heights']
            temps = values['temps']

            daily_wave_max = max(wave_heights)
            daily_wave_min = min(wave_heights)
            daily_wave_avg = sum(wave_heights) / len(wave_heights)

            # Calculate average only if temps list is not empty
            if temps:
                daily_temp_max = max(temps)
                daily_temp_min = min(temps)
                daily_temp_avg = sum(temps) / len(temps)
            else:
                # Handle case when no temperature data is available
                daily_temp_max = daily_temp_min = daily_temp_avg = None

            wave_unit_id = values['wave_unit_id']
            temp_unit_id = values['temp_unit_id']

            # Insert the daily reading into the database
            self.serv_HTML.insert_daily_html_reading(
                daily_wave_max, daily_wave_min, daily_wave_avg, 
                wave_unit_id, daily_temp_max, daily_temp_min, daily_temp_avg, 
                temp_unit_id, date, location_id
            )

    def fetch_save_all_data(self):
        try:
            self.record_gif_data()
            self.record_GSio_data()
            self.record_HTML_data()

            self.insert_daily_html_reading()
            self.insert_daily_gif_reading()
            self.insert_daily_glass_storm_reading()
        
        
            self.delete_all_html_data()
            self.delete_all_glass_storm_data()
            self.delete_all_gif_data()
            return 1;
        except Exception as e:
            print(e)
            return 0;
