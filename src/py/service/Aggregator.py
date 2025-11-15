from entity.Panel import Panel
from entity.PanelName import PanelName
from utils.SqlExecutor import SqlExecutor
from utils.SQLMapper import SQLMapper
from dateutil import parser


class Aggregator:
    def __init__(self, db_name: str) -> None:
        self.executor = SqlExecutor(db_name)  
        pass

    def get_panel_with_name_by_id(self, id: int) -> Panel:
        script = f"SELECT Panel.ID, Panel.PanelNameID,Panel.Time,Panel.Value, PanelName.Name FROM Panel INNER JOIN PanelName on Panel.PanelNameID = PanelName.id WHERE Panel.ID = {id}"
        results = self.executor.execute_select(script)
        return SQLMapper.map_row_to_panel(results[0])
