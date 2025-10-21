from typing import Type
from repository.RepositoryBase import RepositoryBase
from entity.PanelName import PanelName
from table.PanelNameTable import PanelNameTable

class PanelNameRepository(RepositoryBase[PanelName, PanelNameTable]):
    def __init__(self, db_name : str):
        super().__init__(db_name)
        self.cache : dict[str,PanelName] = dict()

    def _map_row_to_entity(self, row: tuple[str, ...]) -> PanelName:
        id = int(row[0])
        name = row[1]
        return PanelName(name,id)
    
    def _get_table(self) -> Type[PanelNameTable]:
        return PanelNameTable
    
    def save_batch(self, entities: list[PanelName]) -> None:
        super().save_batch(entities)
        loaded_names = self.get_all_entities()
        for panel_name in loaded_names:
            name = panel_name.get_name()
            if name is not None:
                self.cache[name] = panel_name
    
    def get_entity_from_cache_by_name(self, name : str) -> PanelName | None:
        return self.cache.get(name)