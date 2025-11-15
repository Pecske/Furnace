from repository.PanelNameRepository import PanelNameRepository
from entity.PanelName import PanelName


class PanelNameService:
    def __init__(self, repo: PanelNameRepository) -> None:
        self.repo = repo

    def create_table(self) -> None:
        self.repo.create_table()

    def save_batch(self, entities: list[PanelName]) -> None:
        self.repo.save_batch(entities)

    def save_or_update(self, panel_name: PanelName) -> PanelName:
        return self.repo.save_or_update(panel_name)

    def get_by_id(self, id: int) -> PanelName:
        return self.repo.get_entity_by_id(id)

    def get_all(self) -> list[PanelName]:
        return self.repo.get_all_entities()

    def delete_by_id(self, id: int) -> None:
        self.repo.delete_by_id(id)
