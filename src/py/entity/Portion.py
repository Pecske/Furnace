from typing import Any
from entity.EntityBase import EntityBase
from datetime import datetime
from table.TableBase import TableBase
from table.PortionTable import PortionTable

class Portion(EntityBase):

    def __init__(self, start : datetime, end : datetime, time : int, portion_time : int, id: int = 0):
        self.start = start
        self.end = end
        self.time = time
        self.portion_time = portion_time
        super().__init__(id)
    
    def get_start(self) -> datetime:
        return self.start
    
    def set_start(self, value : datetime) -> None:
        self.start = value
    
    def get_end(self) -> datetime:
        return self.end
    
    def set_end(self,value:datetime) -> None:
        self.end = value
    
    def get_time(self) -> int:
        return self.time
    
    def set_time(self,value: int) -> None:
        self.time = value

    def get_portion_time(self) -> int:
        return self.portion_time
    
    def set_portion_time(self,value : int) -> None:
        self.portion_time = value
    
    def _get_attribute_values(self) -> dict[str, Any]:
        result : dict[str,Any] = dict()
        result[TableBase.ID] = self.get_id()
        result[PortionTable.START] = self.get_start()
        result[PortionTable.END] = self.get_end()
        result[PortionTable.TIME] = self.get_time()
        result[PortionTable.PORTION_TIME] = self.get_portion_time()
        return result