from entity.Panel import Panel
from dto.PanelCountData import PanelCountData
from dto.PanelStatisticsData import PanelStatisticsData
from utils.SqlExecutor import SqlExecutor
from utils.SQLMapper import SQLMapper


class Aggregator:
    def __init__(self, db_name: str) -> None:
        self.executor = SqlExecutor(db_name)
        pass

    def get_panel_with_name_by_id(self, id: int) -> Panel:
        script = f"SELECT Panel.ID, Panel.PanelNameID,Panel.Time,Panel.Value, PanelName.Name FROM Panel INNER JOIN PanelName on Panel.PanelNameID = PanelName.id WHERE Panel.ID = {id}"
        results = self.executor.execute_select(script)
        return SQLMapper.map_row_to_panel(results[0])

    def get_all_panels_with_names(self) -> list[Panel]:
        script = f"SELECT Panel.ID, Panel.PanelNameID,Panel.Time,Panel.Value, PanelName.Name FROM Panel INNER JOIN PanelName on Panel.PanelNameID = PanelName.id"
        results = self.executor.execute_select(script)
        panels: list[Panel] = list()
        for result in results:
            panels.append(SQLMapper.map_row_to_panel(result))

        return panels

    def get_panel_count(self) -> list[PanelCountData]:
        script = f'SELECT PanelName.Name, count(PanelNameID) as "NumberOfValues" from Panel INNER JOIN PanelName on Panel.PanelNameID = PanelName.ID GROUP By PanelNameID'
        results = self.executor.execute_select(script)
        panel_counts: list[PanelCountData] = list()
        for result in results:
            panel_counts.append(SQLMapper.map_row_to_panel_count(result))

        return panel_counts

    def get_panel_statistics(self) -> list[PanelStatisticsData]:
        script = f'BEGIN TRANSACTION; DROP TABLE IF EXISTS AllStats; CREATE TABLE IF NOT EXISTS AllStats("PanelName" TEXT UNIQUE,"Min" INTEGER, "Max" INTEGER, "Avg" INTEGER, "NameID" INTEGER); INSERT INTO AllStats(PanelName,Min,Max,Avg,NameID) Select "All" as "PanelName", min(value) as "Min", max(value) as "Max",avg(value) as "Avg", 0 as "NameID" from Panel; DROP TABLE IF EXISTS DistinctStats; CREATE TABLE IF NOT EXISTS DistinctStats("PanelName" TEXT UNIQUE,"Min" INTEGER, "Max" INTEGER, "Avg" INTEGER, "NameID" INTEGER); INSERT INTO DistinctStats(PanelName,Min,Max,Avg,NameID) SELECT PanelName.Name, min(Panel.Value) as "Min", max(Panel.value) as "Max", avg(Panel.Value) as "Avg", Panel.PanelNameID FROM Panel INNER JOIN PanelName on Panel.PanelNameID = PanelName.ID GROUP BY PanelNameID; COMMIT TRANSACTION;'
        self.executor.execute_batch(script)
        select_script = f"SELECT NameID, PanelName,Min,Max,Avg FROM AllStats UNION SELECT NameID, PanelName,Min,Max,Avg FROM DistinctStats ORDER BY NameID;"
        results = self.executor.execute_select(select_script)
        panel_stats: list[PanelStatisticsData] = list()
        for result in results:
            panel_stats.append(SQLMapper.map_row_to_panel_statistics(result))

        return panel_stats
