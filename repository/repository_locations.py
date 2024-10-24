from app import db
from .Models import Models

class LocationsRepository:
    def __init__(self):
        pass

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
  