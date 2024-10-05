import requests
from bs4 import BeautifulSoup

def fetchMeteoData(url = 'http://varna.meteo.bg/'):
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    rows = soup.find_all('tr')

    meteo_data = []

    for row in rows[2:]:
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