from app import db
from .Models import Units

class UnitsRepository:
    def __init__(self):
        pass

    def get_unit_id_by_name(self, unit_name):
        try:
            unit = db.session.query(Units).filter_by(UnitName=unit_name).first()
            if unit:
                return unit.UnitId
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


            