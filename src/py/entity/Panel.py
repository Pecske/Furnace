from entity.EntityBase import EntityBase
from entity.PanelName import PanelName
from datetime import datetime
from typing import Any
from table.TableBase import TableBase
from table.PanelTable import PanelTable


class Panel(EntityBase):

    def __init__(self,panel_name : PanelName, time : datetime, value : float, id: int = 0):
        self.panel_name_id = panel_name
        self.time = time
        self.value = value
        super().__init__(id)

    def get_panel_name(self) -> PanelName:
        return self.panel_name_id
    
    def set_panel_name(self, value : PanelName) -> None:
        self.panel_name_id = value
    
    def get_time(self) -> datetime:
        return self.time
    
    def set_time(self, value : datetime) -> None:
        self.time = value
    
    def get_value(self) -> float:
        return self.value
    
    def set_value(self, value : float) -> None:
        self.value = value
    
    def _get_attribute_values(self) -> dict[str, Any]:
        result : dict[str,Any] = dict()
        result[TableBase.ID] = self.get_id()
        result[PanelTable.PANEL_NAME_ID] = self.get_panel_name().get_id()
        result[PanelTable.TIME] = self.get_time()
        result[PanelTable.VALUE] = self.get_value()        
        return result