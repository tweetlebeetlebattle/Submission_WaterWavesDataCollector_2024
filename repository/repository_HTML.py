from flask import current_app
from .Models.Models import HTMLData, DailyHTMLReading, to_dict
from app import db
from datetime import datetime, date

class HTMLDataRepository:
    @staticmethod
    def insert_data(wave_read, wave_unit_id, temp_read, temp_unit_id, date_value, location_id):
        """Insert new HTMLData entry into the database."""
        try:
            date_value_converted = (
                datetime.combine(date_value, datetime.min.time())
                if isinstance(date_value, date) and not isinstance(date_value, datetime)
                else date_value
            )

            new_html_data = HTMLData(
                WaveRead=wave_read,
                WaveUnitId=wave_unit_id,
                TempRead=temp_read,
                TempUnitId=temp_unit_id,
                Date=date_value_converted,
                LocationId=location_id
            )
            
            db.session.add(new_html_data)
            db.session.commit()
            return new_html_data
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error inserting HTMLData: {e}")
            return None

    @staticmethod
    def read_all_data():
        """Read all entries from the HTMLData table."""
        try:
            data = db.session.query(HTMLData).all()
            return [to_dict(item) for item in data]
        except Exception as e:
            current_app.logger.error(f"Error reading HTMLData: {e}")
            return None

    @staticmethod
    def delete_all_data():
        """Delete all entries from the HTMLData table."""
        try:
            db.session.query(HTMLData).delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error deleting HTMLData: {e}")
            return False


class DailyHTMLReadingRepository:
    @staticmethod
    def insert_data(daily_wave_max, daily_wave_min, daily_wave_avg, wave_unit_id, 
                    daily_temp_max, daily_temp_min, daily_temp_avg, temp_unit_id, 
                    date_value, location_id):
        """Insert new DailyHTMLReading entry into the database."""
        try:
            date_value_converted = (
                datetime.combine(date_value, datetime.min.time())
                if isinstance(date_value, date) and not isinstance(date_value, datetime)
                else date_value
            )

            new_daily_html_reading = DailyHTMLReading(
                DailyWaveMax=daily_wave_max,
                DailyWaveMin=daily_wave_min,
                DailyWaveAvg=daily_wave_avg,
                WaveUnitId=wave_unit_id,
                DailyTempMax=daily_temp_max,
                DailyTempMin=daily_temp_min,
                DailyTempAvg=daily_temp_avg,
                TempUnitId=temp_unit_id,
                Date=date_value_converted,
                LocationId=location_id
            )
            
            db.session.add(new_daily_html_reading)
            db.session.commit()
            return new_daily_html_reading
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error inserting DailyHTMLReading: {e}")
            return None

    @staticmethod
    def read_all_data():
        """Read all entries from the DailyHTMLReading table."""
        try:
            data = db.session.query(DailyHTMLReading).all()
            return [to_dict(item) for item in data]
        except Exception as e:
            current_app.logger.error(f"Error reading DailyHTMLReading: {e}")
            return None
