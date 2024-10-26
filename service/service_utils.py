import unicodedata

class ServiceUtils:
    def __init__(self):
        from repository.repository_utils import UtilsRepository
        self.repo = UtilsRepository()

    def get_location_id_by_name(self, name):
        if(name == "Еминe"):
            name = "Емине"
        normalized_name = self.normalize_name(name)
        location_id = self.repo.get_location_id_by_name(normalized_name)
        return location_id 
    
    def get_unit_id_by_name(self, name):
        return self.repo.get_unit_id_by_name(name)
    
    def transform_bala_to_meters(self, bala):
        bala_to_meters = {
            0: 0,
            1: 0.1,
            2: 0.5,
            3: 1.25,
            4: 2.5,
            5: 4
        }
        return bala_to_meters.get(bala, 10)
    
    def normalize_name(self, name):
        name = unicodedata.normalize('NFKC', name).lower()
        name = ''.join(
            char for char in name if not unicodedata.combining(char)
        )
        return name
