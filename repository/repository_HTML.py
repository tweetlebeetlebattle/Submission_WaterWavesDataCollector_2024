from flask import current_app
from .Models.Models import HTMLData, DailyHTMLReading
from app import db

class HTMLDataRepository:
    def insert_data(self, wave_read, wave_unit_id, temp_read, temp_unit_id, date, location_id):
        try:
            new_html_data = HTMLData(
                WaveRead=wave_read,
                WaveUnitId=wave_unit_id,
                TempRead=temp_read,
                TempUnitId=temp_unit_id,
                Date=date,
                LocationId=location_id
            )
            
            db.session.add(new_html_data)
            db.session.commit()

            return new_html_data
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            return None

    def read_all_data(self):
        try:
            data = db.session.query(HTMLData).all()
            return data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def delete_all_data(self):
        try:
            db.session.query(HTMLData).delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            return False

class DailyHTMLReadingRepository:
    def insert_data(self, daily_wave_max, daily_wave_min, daily_wave_avg, wave_unit_id, 
                    daily_temp_max, daily_temp_min, daily_temp_avg, temp_unit_id, date, location_id):
        try:
            new_daily_html_reading = DailyHTMLReading(
                DailyWaveMax=daily_wave_max,
                DailyWaveMin=daily_wave_min,
                DailyWaveAvg=daily_wave_avg,
                WaveUnitId=wave_unit_id,
                DailyTempMax=daily_temp_max,
                DailyTempMin=daily_temp_min,
                DailyTempAvg=daily_temp_avg,
                TempUnitId=temp_unit_id,
                Date=date,
                LocationId=location_id
            )
            
            db.session.add(new_daily_html_reading)
            db.session.commit()

            return new_daily_html_reading
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            return None

    def read_all_data(self):
        try:
            data = db.session.query(DailyHTMLReading).all()
            return data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
