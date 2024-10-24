import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

class MeteoHTMLService:
    def __init__(self):
        self.url = os.getenv("HTML_url")  

    def record_meteo_data():
        return;

    def fetch_meteo_data(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve data: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        
        meteo_data = []
        for row in rows[2:]:  # Skip the first two rows (headers)
            cells = row.find_all('td')
            if len(cells) >= 4:
                location = cells[1].text.strip()
                wave_height = cells[2].text.strip()
                water_temp = cells[3].text.strip()
                
                meteo_data.append({
                    'Location': location,
                    'Wave Height': wave_height,
                    'Water Temperature': water_temp
                })
        
        return meteo_data

