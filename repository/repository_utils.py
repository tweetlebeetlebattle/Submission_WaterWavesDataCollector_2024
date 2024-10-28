from app import db
from repository.Models import Models
from repository.Models.Models import DataFetchingLogs
from datetime import datetime

class UtilsRepository:
    def __init__(self):
        pass

    def get_unit_id_by_name(self, unit_name):
        try:
            unit = db.session.query(Models.Units).filter_by(UnitName=unit_name).first()
            if unit:
                return unit.UnitId
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_location_id_by_name(self, location_name):
        try:
            location = db.session.query(Models.Locations).filter_by(Name=location_name).first()

            if location:
                return location.Id
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def insert_data_fetching_log(self, log):
        
        try:
            new_log_data = DataFetchingLogs(
                StatusLog = log,
                Time = datetime.timezone.utcnow()   
            )
            
            db.session.add(new_log_data)
            
            db.session.commit()

            return new_log_data
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            return None    