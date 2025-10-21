from repository.PanelRepository import PanelRepository
from entity.Panel import Panel

class PanelService:
    def __init__(self, repo : PanelRepository) -> None:
        self.repo = repo

    def create_table(self) -> None:
        self.repo.create_table()
    
    def save_batch(self, panels : list[Panel]) -> None:
        self.repo.save_batch(panels)

    def save_or_update(self, panel : Panel) -> Panel:
        return self.repo.save_or_update(panel)
        
    def get_by_id(self, id : int) -> Panel:
        return self.repo.get_entity_by_id(id)
    
    def get_all(self) -> list[Panel]:
        return self.repo.get_all_entities()
    
    def delete_by_id(self, id : int) -> None:
        self.repo.delete_by_id(id)