from typing import Any
from entity.EntityBase import EntityBase
from table.TableBase import TableBase
from table.PanelNameTable import PanelNameTable

class PanelName(EntityBase):
    def __init__(self, name : str | None = None, id: int = 0):
        self.name = name
        super().__init__(id)
    
    def get_name(self)-> str| None:
        return self.name
    
    def set_name(self,value : str |None) -> None:
        self.name = value
    
    def _get_attribute_values(self) -> dict[str, Any]:
        result : dict[str,Any] = dict()
        result[TableBase.ID] = self.get_id()
        result[PanelNameTable.NAME] = self.get_name()        
        return result
    
    def __eq__(self, value: object) -> bool:
        if type(value) == PanelName:
            if self.get_name() == value.get_name():
                return True
        return False
    
    def __hash__(self) -> int:
        return hash(self.get_name()) * 7