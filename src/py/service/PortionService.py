from repository.PortionRepository import PortionRepository
from entity.Portion import Portion

class PortionService:
    def __init__(self, repo : PortionRepository) -> None:
        self.repo = repo

    def create_table(self) -> None:
        self.repo.create_table()
    
    def save_batch(self, entities : list[Portion]) -> None:
        self.repo.save_batch(entities)

    def save_or_update(self, portion : Portion) -> Portion:
        return self.repo.save_or_update(portion)

    def get_by_id(self, id : int) -> Portion:
        return self.repo.get_entity_by_id(id)
    
    def get_all(self) -> list[Portion]:
        return self.repo.get_all_entities()
    
    def delete_by_id(self, id : int) -> None:
        self.repo.delete_by_id(id)