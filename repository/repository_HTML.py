from flask import current_app
from .Models.Models import HTMLData, DailyHTMLReading
from app import db
from datetime import datetime, date

class HTMLDataRepository:
    def insert_data(self, wave_read, wave_unit_id, temp_read, temp_unit_id, date_value, location_id):
        date_value_converted = None
        try:
            if isinstance(date_value, date) and not isinstance(date_value, datetime):
                date_value_converted = datetime.combine(date_value, datetime.min.time())
            else:
                date_value_converted = date_value

            # Create a new HTMLData object with the properly formatted date
            new_html_data = HTMLData(
                WaveRead=wave_read,                 # Use uppercase to match model
                WaveUnitId=wave_unit_id,           # Use uppercase to match model
                TempRead=temp_read,                 # Use uppercase to match model
                TempUnitId=temp_unit_id,            # Use uppercase to match model
                Date=date_value_converted,           # Correctly formatted datetime
                LocationId=location_id               # Use uppercase to match model
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
            return [item.to_dict() for item in data]  # Return data in dict form
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
                    daily_temp_max, daily_temp_min, daily_temp_avg, temp_unit_id, date_value, location_id):
        date_value_converted = None
        try:
            if isinstance(date_value, date) and not isinstance(date_value, datetime):
                date_value_converted = datetime.combine(date_value, datetime.min.time())
            else:
                date_value_converted = date_value

            # Create a new DailyHTMLReading object with the correctly formatted date
            new_daily_html_reading = DailyHTMLReading(
                DailyWaveMax=daily_wave_max,        # Use uppercase to match model
                DailyWaveMin=daily_wave_min,        # Use uppercase to match model
                DailyWaveAvg=daily_wave_avg,        # Use uppercase to match model
                WaveUnitId=wave_unit_id,            # Use uppercase to match model
                DailyTempMax=daily_temp_max,        # Use uppercase to match model
                DailyTempMin=daily_temp_min,        # Use uppercase to match model
                DailyTempAvg=daily_temp_avg,        # Use uppercase to match model
                TempUnitId=temp_unit_id,            # Use uppercase to match model
                Date=date_value_converted,           # Correctly formatted datetime
                LocationId=location_id               # Use uppercase to match model
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
            return [item.to_dict() for item in data]  # Return data in dict form
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
