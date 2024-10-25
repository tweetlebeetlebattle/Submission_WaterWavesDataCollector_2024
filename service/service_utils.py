class ServiceUtils:
    def __init__(self):
        from repository.repository_utils import UtilsRepository
        self.repo = UtilsRepository()

    def get_location_id_by_name(self, name):
        return self.repo.get_location_id_by_name(name) 
    
    def get_unit_id_by_name(self, name):
        return self.repo.get_unit_id_by_name(name)