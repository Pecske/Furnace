from abc import abstractmethod
from entity.EntityBase import EntityBase
from typing import TypeVar, Generic, Type
from table.TableBase import TableBase
from utils.SqlExecutor import SqlExecutor

T = TypeVar("T", bound= EntityBase)
U = TypeVar("U", bound= TableBase)

class RepositoryBase(Generic[T,U]):
    def __init__(self, db_name : str):
        super().__init__()
        self.executor = SqlExecutor(db_name,self._get_table())
    
    def create_table(self) -> None:
        self.executor.create_table()
    
    def save_batch(self, entities : list[T]) -> None:
        self.executor.save_batch(entities)
    
    def save_or_update(self, entity : T) -> T:
        entity_id = entity.get_id()
        if entity_id > 0:
            return self._update(entity)
        else:
            return self._save(entity)
    
    def _save(self, entity : T) -> T:
        result = self.executor.save(entity)
        if result is not None:
            entity.set_id(result)
        return entity 
    
    def _update(self, entity : T )-> T:           
        result = self.executor.update(entity)
        if result is not None:
            entity.set_id(result)
        return entity
    
    def get_entity_by_id(self,id: int) -> T:
        query_results = self.executor.get_by_id(id)
        return self._map_row_to_entity(query_results[0])    
    
    def get_all_entities(self) -> list[T]:
        query_results = self.executor.get_all()
        results : list[T] = list()
        for item in query_results:
            results.append(self._map_row_to_entity(item))
        return results    
    
    def delete_by_id(self,id : int) -> None:
        self.executor.delete_by_id(id)
    
    @abstractmethod
    def _map_row_to_entity(self, row : tuple[str,...]) -> T:
        raise NotImplementedError
    
    @abstractmethod
    def _get_table(self) -> Type[U]:
        raise NotImplementedError
