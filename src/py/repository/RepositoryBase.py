from abc import abstractmethod
from entity.EntityBase import EntityBase
from typing import TypeVar, Generic
from utils.SqlExecutor import SqlExecutor

T = TypeVar("T", bound= EntityBase)

class RepositoryBase(Generic[T]):
    def __init__(self, db_name : str):
        super().__init__()
        self.executor = SqlExecutor(db_name)    
    
    def save_or_update(self, entity : T) -> T:
        entity_id = entity.get_id()
        if entity_id > 0:
            return self.update(entity)
        else:
            return self.save(entity)

    @abstractmethod
    def create_table(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def save_batch(self, entities : list[T]) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def save(self, entity : T) -> T:
        raise NotImplementedError 
    
    @abstractmethod
    def update(self, entity : T )-> T:           
        raise NotImplementedError
        
    @abstractmethod
    def get_entity_by_id(self,id: int) -> T:
        raise NotImplementedError   
    
    @abstractmethod
    def get_all_entities(self) -> list[T]:
        raise NotImplementedError  
    
    @abstractmethod
    def delete_by_id(self,id : int) -> None:
        raise NotImplementedError
