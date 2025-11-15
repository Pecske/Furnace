from entity.Panel import Panel
from entity.PanelName import PanelName
from entity.Portion import Portion
from dateutil import parser
from dto.PanelCountData import PanelCountData
from dto.PanelStatisticsData import PanelStatisticsData


class SQLMapper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def map_row_to_panel(row: tuple[str, ...]) -> Panel:
        id = int(row[0])
        panel_name_id = int(row[1])
        time = parser.parse(row[2])
        value = float(row[3])
        if len(row) > 4:
            panel_name = row[4]
        else:
            panel_name = None
        
        return Panel(PanelName(panel_name,panel_name_id),time,value,id)

    @staticmethod
    def map_row_to_panel_name(row: tuple[str,...]) -> PanelName:
        id = int(row[0])
        name = row[1]

        return PanelName(name,id)
    
    @staticmethod
    def map_row_to_portion(row : tuple[str,...]) -> Portion:
        id = int(row[0])
        start = parser.parse(row[1])
        end = parser.parse(row[2])
        time = int(row[3])
        portion_time = int(row[4])

        return Portion(start,end,time,portion_time,id)
    
    @staticmethod
    def map_row_to_panel_count(row: tuple[str,...]) -> PanelCountData:
        return PanelCountData(row[0],int(row[1]))
    
    @staticmethod
    def map_row_to_panel_statistics(row: tuple[str,...]) -> PanelStatisticsData:
        return PanelStatisticsData(row[0],float(row[1]),float(row[2]),float(row[3]))