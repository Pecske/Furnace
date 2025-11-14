from entity.Panel import Panel
from entity.PanelName import PanelName
from utils.SqlExecutor import SqlExecutor
from dateutil import parser


class Aggregator:
    def __init__(self, db_name: str) -> None:
        self.executor = SqlExecutor(db_name)  
        pass

    def _map_row_to_panel(self, row: tuple[str, ...]) -> Panel:
        id = int(row[0])
        panel_name_id = int(row[1])
        time = parser.parse(row[2])
        value = int(row[3])
        panel_name = row[4]
        
        return Panel(PanelName(panel_name,panel_name_id),time,value,id)

    def get_panel_with_name_by_id(self, id: int) -> Panel:
        script = f"SELECT Panel.ID, Panel.PanelNameID,Panel.Time,Panel.Value, PanelName.Name FROM Panel INNER JOIN PanelName on Panel.PanelNameID = PanelName.id WHERE Panel.ID = {id}"
        results = self.executor.execute_select(script)
        return self._map_row_to_panel(results[0])
