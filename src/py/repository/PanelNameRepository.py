from repository.RepositoryBase import RepositoryBase
from entity.PanelName import PanelName

class PanelNameRepository(RepositoryBase[PanelName]):
    def __init__(self, db_name : str):
        super().__init__(db_name)

    def _map_row_to_entity(self, row: tuple[str, ...]) -> PanelName:
        id = int(row[0])
        name = row[1]
        return PanelName(name,id)
    
    def create_table(self) -> None:
        query = "CREATE TABLE PanelName (ID	INTEGER,Name TEXT UNIQUE,PRIMARY KEY(ID));"
        self.executor.execute_batch(query)
    
    def save_batch(self, entities: list[PanelName]) -> None:
        inserts_str = str()
        for entity in entities:
            inserts_str += f"INSERT INTO PanelName(Name) VALUES({entity.get_name()});"
        
        batch_script = f"BEGIN TRANSACTION {inserts_str} COMMIT TRANSACTION;"
        self.executor.execute(batch_script)

    def save(self, entity: PanelName) -> PanelName:
        script = f"INSERT INTO PanelName(Name) VALUES({entity.get_name()});"
        result_id = self.executor.execute(script)
        if result_id is not None:
            entity.set_id(result_id)
        return entity
    
    def update(self, entity: PanelName) -> PanelName:
        script = f"UPDATE PanelName SET Name = {entity.get_name()} WHERE ID = {entity.get_id()}"
        self.executor.execute(script)
        return entity

    def get_entity_by_id(self, id: int) -> PanelName:
        script = f"SELECT ID,Name FROM PanelName WHERE ID = {id}"
        results = self.executor.execute_select(script)
        return self._map_row_to_entity(results[0])
    
    def get_all_entities(self) -> list[PanelName]:
        script = f"SELECT ID,Name FROM PanelName"
        results = self.executor.execute_select(script)
        found_panels : list[PanelName] = list()
        for result in results:
            found_panels.append(self._map_row_to_entity(result))
        
        return results
    
    def delete_by_id(self, id: int) -> None:
        script = f"DELETE FROM PanelName where ID = {id}"
        self.executor.execute(script)