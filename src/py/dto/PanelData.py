from entity.PanelName import PanelName
from datetime import datetime

class PanelData:
    def __init__(self, panel_name : PanelName, time : datetime, value : int, id : int = 0) -> None:
        self.id = id
        self.panel_name = panel_name
        self.time = time
        self.value = value

    def get_id(self) -> int:
        return self.id
    
    def set_id(self, value : int) -> None:
        self.id = value
    
    def get_panel_name(self) -> PanelName:
        return self.panel_name
    
    def set_panel_name(self, value : PanelName) -> None:
        self.panel_name = value

    def get_time(self) -> datetime:
        return self.time

    def set_time(self, value : datetime) -> None: 
        self.time = value
    
    def get_value(self) -> int:
        return self.value
    
    def set_value(self, value : int) -> None:
        self.value = value