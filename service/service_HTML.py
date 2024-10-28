import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

class MeteoHTMLService:
    def __init__(self):
        from repository.repository_HTML import HTMLDataRepository
        from repository.repository_HTML import DailyHTMLReadingRepository
        from service.service_utils import ServiceUtils
        self.service_utils = ServiceUtils()
        self.url = os.getenv("HTML_url")  
        self.html_data_repo = HTMLDataRepository()
        self.daily_html_reading_repo = DailyHTMLReadingRepository()

    def insert_html_data(self, wave_read, wave_unit_id, temp_read, temp_unit_id, date, location_id):
        return self.html_data_repo.insert_data(wave_read, wave_unit_id, temp_read, temp_unit_id, date, location_id)

    def get_all_html_data(self):
        return self.html_data_repo.read_all_data()

    def delete_all_html_data(self):
        return self.html_data_repo.delete_all_data()

    def insert_daily_html_reading(self, daily_wave_max, daily_wave_min, daily_wave_avg, wave_unit_id,
                                  daily_temp_max, daily_temp_min, daily_temp_avg, temp_unit_id,
                                  date, location_id):
        return self.daily_html_reading_repo.insert_data(
            daily_wave_max, daily_wave_min, daily_wave_avg, wave_unit_id,
            daily_temp_max, daily_temp_min, daily_temp_avg, temp_unit_id,
            date, location_id
        )

    def get_all_daily_html_readings(self):
        return self.daily_html_reading_repo.read_all_data()

    def delete_all_daily_html_readings(self):
        return self.daily_html_reading_repo.delete_all_data()

    def fetch_meteo_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            print("Request successful!")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            tables = soup.find_all('table')
            print(f"Number of tables found: {len(tables)}\n")
            
            table_6_data = []
            
            # Check if Table 6 exists
            if len(tables) >= 6:
                # Select Table 6 (index 5 as indexing starts from 0)
                table_6 = tables[5]
                
                # Find all rows in Table 6 and process rows 3 to 8
                rows = table_6.find_all('tr')
                for row_index in range(2, 8):  # Rows 3 to 8 (0-indexed, so 2 to 7)
                    row = rows[row_index]
                    cells = row.find_all('td')
                    cell_data = [cell.text.strip() for cell in cells if cell.text.strip()]
                    
                    if len(cell_data) == 3:
                        # Parse wave height and temperature, handling missing temperature
                        wave_height = int(cell_data[1].split()[0])  # Extract the number before 'бала'
                        try:
                            water_temp = int(cell_data[2].split()[0])  # Extract the number before '°C'
                        except ValueError:
                            water_temp = None  # Set to None if temperature is missing
                            
                        data_entry = {
                            'location': cell_data[0],
                            'waveHeightInBala': wave_height,
                            'waterTempInC': water_temp
                        }
                        
                        table_6_data.append(data_entry)
            return table_6_data
        else:
            print(f"Request failed with status code: {response.status_code}")
            self.service_utils.insert_data_fetching_log(f"HTML Request failed with status code: {response.status_code}")
