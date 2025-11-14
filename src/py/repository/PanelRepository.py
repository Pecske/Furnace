from typing import Type
from repository.RepositoryBase import RepositoryBase
from entity.PanelName import PanelName
from entity.Panel import Panel
from dateutil import parser

class PanelRepository(RepositoryBase[Panel]):    
    
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
    
    def create_table(self) -> None:
        query = "CREATE TABLE Panel (ID	INTEGER,PanelNameID	INTEGER,Time TEXT,Value	INTEGER,PRIMARY KEY(ID),FOREIGN KEY(PanelNameID) REFERENCES PanelName(ID));"
        self.executor.execute_batch(query)
    
    def save_batch(self, entities: list[Panel]) -> None:
        inserts_str = str()
        for entity in entities:
            inserts_str += f"INSERT INTO Panel(PanelNameID,Time,Value) VALUES({entity.get_panel_name_id()},{entity.get_time()},{entity.get_value()});"
        
        batch_script = f"BEGIN TRANSACTION {inserts_str} COMMIT TRANSACTION;"
        self.executor.execute(batch_script)

    def save(self, entity: Panel) -> Panel:
        script = f"INSERT INTO Panel(PanelNameID,Time,Value) VALUES({entity.get_panel_name_id()},{entity.get_time()},{entity.get_value()});"
        result_id = self.executor.execute(script)
        if result_id is not None:
            entity.set_id(result_id)
        return entity
    
    def update(self, entity: Panel) -> Panel:
        script = f"UPDATE Panel SET PanelNameID = {entity.get_panel_name_id()},Time = {entity.get_time()},Value = {entity.get_value()} WHERE ID = {entity.get_id()}"
        self.executor.execute(script)
        return entity

    def get_entity_by_id(self, id: int) -> Panel:
        script = f"SELECT ID,PanelNameID,Time,Value FROM Panel WHERE ID = {id}"
        results = self.executor.execute_select(script)
        return self._map_row_to_entity(results[0])
    
    def get_all_entities(self) -> list[Panel]:
        script = f"SELECT ID,PanelNameID,Time,Value FROM Panel"
        results = self.executor.execute_select(script)
        found_panels : list[Panel] = list()
        for result in results:
            found_panels.append(self._map_row_to_entity(result))
        
        return results
    
    def delete_by_id(self, id: int) -> None:
        script = f"DELETE FROM Panel where ID = {id}"
        self.executor.execute(script)