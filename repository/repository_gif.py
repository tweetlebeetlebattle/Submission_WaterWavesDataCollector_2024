from app import db
from .Models.Models import GifData, DailyGifReading

class GifDataRepository:
    def __init__(self):
        pass

    def insert_data(self, wave_read, wave_unit_id, date, location_id):
        try:
            new_gif_data = GifData(
                WaveRead=wave_read,
                WaveUnitId=wave_unit_id,
                Date=date,
                LocationId=location_id
            )
            
            db.session.add(new_gif_data)
            
            db.session.commit()

            return new_gif_data
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            return None

    def read_all_data(self):
        try:
            data = db.session.query(GifData).all()
            return data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def delete_all_data(self):
        try:
            db.session.query(GifData).delete()
            
            db.session.commit()

            return True
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            return False

class DailyGifReadingRepository:
    def __init__(self):
        pass

    def insert_data(self, daily_wave_max=None, daily_wave_min=None, daily_wave_avg=None,
                   wave_unit_id=None, date=None, location_id=None):
        try:
            new_daily_gif_reading = DailyGifReading(
                DailyWaveMax=daily_wave_max,
                DailyWaveMin=daily_wave_min,
                DailyWaveAvg=daily_wave_avg,
                WaveUnitId=wave_unit_id,
                Date=date,
                LocationId=location_id
            )

            db.session.add(new_daily_gif_reading)

            db.session.commit()

            return new_daily_gif_reading

        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while inserting data: {e}")
            return None

    def read_all_data(self):
        try:
            data = DailyGifReading.query.all()
            return data

        except Exception as e:
            print(f"An error occurred while reading data: {e}")
            return None

    def delete_all_data(self):
        try:
            num_deleted = db.session.query(DailyGifReading).delete()

            db.session.commit()

            print(f"Deleted {num_deleted} records from DailyGifReading.")
            return True

        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while deleting data: {e}")
            return False