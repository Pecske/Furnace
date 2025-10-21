from typing import Self
from utils.Attribute import Attribute

class TableDescriptor:
    def __init__(self, table_name : str, attributes_types : list[Attribute] = list(), connections : dict[Self,dict[str,str]] = dict()) -> None:
        self.table_name = table_name
        self.attributes = attributes_types
        self.connections = connections
        pass

    def get_table_name(self) -> str:
        return self.table_name
    
    def set_table_name(self, value : str) -> None:
        self.table_name = value
    
    def get_attributes(self) -> list[Attribute] :
        return self.attributes
    
    def set_attributes(self, value : list[Attribute] ) -> None:
        self.attributes = value
    
    def get_connections(self) -> dict[Self,dict[str,str]]:
        return self.connections
    
    def set_connections(self, value : dict[Self,dict[str,str]]) -> None:
        self.connections = value