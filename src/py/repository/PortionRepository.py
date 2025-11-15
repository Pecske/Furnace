from repository.RepositoryBase import RepositoryBase
from entity.Portion import Portion
from utils.SQLMapper import SQLMapper

class PortionRepository(RepositoryBase[Portion]):
    def __init__(self, db_name: str):
        super().__init__(db_name)
    
    def create_table(self) -> None:
        query = "CREATE TABLE IF NOT EXISTS Portion (\"ID\" INTEGER,\"Start\" TEXT,\"End\" TEXT,\"Time\" INTEGER,\"PortionTime\" INTEGER,PRIMARY KEY(\"ID\"));"
        self.executor.execute_batch(query)
    
    def save_batch(self, entities: list[Portion]) -> None:
        inserts_str = str()
        for entity in entities:
            inserts_str += f"INSERT INTO Portion(\"Start\",\"End\",\"Time\",\"PortionTime\") VALUES(\"{entity.get_start()}\",\"{entity.get_end()}\",{entity.get_time()},{entity.get_portion_time()}); "
        
        batch_script = f"BEGIN TRANSACTION; {inserts_str} COMMIT TRANSACTION;"
        self.executor.execute_batch(batch_script)

    def save(self, entity: Portion) -> Portion:
        script = f"INSERT INTO Portion(\"Start\",\"End\",\"Time\",\"PortionTime\") VALUES(\"{entity.get_start()}\",\"{entity.get_end()}\",{entity.get_time()},{entity.get_portion_time()});"
        result_id = self.executor.execute(script)
        if result_id is not None:
            entity.set_id(result_id)
        return entity
    
    def update(self, entity: Portion) -> Portion:
        script = f"UPDATE Portion SET Start = {entity.get_start()}, End = {entity.get_end()}, Time = {entity.get_time()}, PortionTime = {entity.get_portion_time()} WHERE ID = {entity.get_id()}"
        self.executor.execute(script)
        return entity

    def get_entity_by_id(self, id: int) -> Portion:
        script = f"SELECT ID,Start,End,Time,PortionTime FROM Portion WHERE ID = {id}"
        results = self.executor.execute_select(script)
        return SQLMapper.map_row_to_portion(results[0])
    
    def get_all_entities(self) -> list[Portion]:
        script = f"SELECT ID,Start,End,Time,PortionTime FROM Portion"
        results = self.executor.execute_select(script)
        found_panels : list[Portion] = list()
        for result in results:
            found_panels.append(SQLMapper.map_row_to_portion(result))
        
        return results
    
    def delete_by_id(self, id: int) -> None:
        script = f"DELETE FROM Portion where ID = {id}"
        self.executor.execute(script)