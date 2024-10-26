from datetime import datetime

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
            # self.serv_HTML.insert_html_data(
            #     wave_read, wave_unit_id, water_temp, temp_unit_id, date, location_id
            # )
    
    def record_gif_data(self):
        gif_data = self.serv_gif.fetch_gif_data()

        # Assuming gif_data contains wave heights and their respective locations,
        # you'll need to process this data accordingly.
        wave_unit_id = self.serv_utils.get_unit_id_by_name("Метра")
        date = datetime.now().date()

        for data in gif_data:
            frame_id = data['id']
            location_name = data['location']
            wave_read = data['index']  # Assuming 'index' represents wave height
            
            location_id = self.serv_utils.get_location_id_by_name(location_name)

            print("Frame ID:", frame_id)
            print("Wave Height (from GIF):", wave_read)
            print("Wave Unit ID:", wave_unit_id)
            print("Date:", date)
            print("Location ID:", location_id)
            print("Location name:", location_name)
            print()

            # Uncomment to insert data into the database
            # self.serv_gif.insert_gif_data(wave_read, wave_unit_id, date, location_id)