from utils.QueryDescriptor import QueryDescriptor
from utils.Attribute import Attribute
from abc import ABC, abstractmethod

class TableBase(ABC):
    ID = "ID"

    @staticmethod
    @abstractmethod
    def get_all_attributes() -> list[Attribute]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_table() -> QueryDescriptor:
        pass

    @staticmethod
    @abstractmethod
    def get_update() -> QueryDescriptor:
        pass
    
    @staticmethod
    @abstractmethod
    def get_insert() -> QueryDescriptor:
        pass
    
    @staticmethod
    @abstractmethod
    def get_select_by_id() -> QueryDescriptor:
        pass
    
    @staticmethod
    @abstractmethod
    def get_select_all() -> QueryDescriptor:
        pass
    
    @staticmethod
    @abstractmethod
    def get_delete_by_id() -> QueryDescriptor:
        pass