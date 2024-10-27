from app import db
from .Models.Models import GlassStormIoData, DailyGlassStormReading,  to_dict

class GlassStormIoDataRepository:
    def __init__(self):
        pass

    def insert_data(self, wave_read, wave_unit_id, temp_read, temp_unit_id, wind_speed_read, wind_unit_id, date, location_id):
        try:
            new_glass_storm_data = GlassStormIoData(
                WaveRead=wave_read,
                WaveUnitId=wave_unit_id,
                TempRead=temp_read, 
                TempUnitId=temp_unit_id,
                WindSpeedIndex = wind_speed_read,
                WindSpeedUnitId = wind_unit_id,
                Date=date,
                LocationId=location_id
            )
            
            db.session.add(new_glass_storm_data)
            
            db.session.commit()

            return new_glass_storm_data
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            return None

    def read_all_data(self):
        try:
            data = db.session.query(GlassStormIoData).all()
            return [to_dict(item) for item in data]
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def delete_all_data(self):
        try:
            db.session.query(GlassStormIoData).delete()
            
            db.session.commit()

            return True
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            return False

class DailyGlassStormReadingRepository:
    def insert_data(self, daily_wave_max, daily_wave_min, daily_wave_avg, wave_unit_id,
                    daily_temp_max, daily_temp_min, daily_temp_avg, temp_unit_id,
                    daily_wind_max, daily_wind_min, daily_wind_avg, wind_unit_id,
                    date, location_id):
        try:
            new_reading = DailyGlassStormReading(
                DailyWaveMax=daily_wave_max,
                DailyWaveMin=daily_wave_min,
                DailyWaveAvg=daily_wave_avg,
                WaveUnitId=wave_unit_id,
                DailyTempMax=daily_temp_max,
                DailyTempMin=daily_temp_min,
                DailyTempAvg=daily_temp_avg,
                TempUnitId=temp_unit_id,
                DailyWindMax=daily_wind_max,
                DailyWindMin=daily_wind_min,
                DailyWindAvg=daily_wind_avg,
                WindUnitId=wind_unit_id,
                Date=date,
                LocationId=location_id
            )
            db.session.add(new_reading)
            db.session.commit()
            return new_reading
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            return False

    def get_all_data(self):
        try:
            return DailyGlassStormReading.query.all()
        except Exception as e:
            print(f"An error occurred: {e}")
            return False