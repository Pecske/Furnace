from typing import Type
from repository.RepositoryBase import RepositoryBase
from entity.PanelName import PanelName
from entity.Panel import Panel
from dateutil import parser
from table.PanelTable import PanelTable

class PanelRepository(RepositoryBase[Panel,PanelTable]):    
    
    def __init__(self, db_name : str):
        super().__init__(db_name)

    def _map_row_to_entity(self, row: tuple[str, ...]) -> Panel:
        id = int(row[0])
        panel_name_id = int(row[1])
        time = parser.parse(row[2])
        value = int(row[3])
        if len(row) > 3:
            panel_name = row[4]
        else:
            panel_name = None
        return Panel(PanelName(panel_name,panel_name_id),time,value,id)
    
    def _get_table(self) -> Type[PanelTable]:
        return PanelTable