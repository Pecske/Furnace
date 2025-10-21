from entity.Panel import Panel
from entity.PanelName import PanelName
from dto.PanelData import PanelData

class Mapper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def panel_data_from_panel(panel : Panel, panel_name: PanelName) -> PanelData:
        return PanelData(panel_name,panel.get_time(),panel.get_value(),panel.get_id())
    
    @staticmethod
    def panel_from_data(data: PanelData, panel_name : PanelName) -> Panel:
        return Panel(panel_name,data.get_time(),data.get_value(),data.get_id())