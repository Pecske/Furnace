from typing import Any

class Attribute:
    def __init__(self, name : str, attr_type : Any = None, auto_increment : bool = False, not_null : bool = False, primary_key : bool = False, foreign_key : bool = False, referenced_table :str = str(), unique : bool = False) -> None:
        self.name = name
        self.attr_type = attr_type
        self.auto_increment = auto_increment
        self.not_null = not_null
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.unique = unique
        self.referenced_table = referenced_table
        pass

    def get_name(self) -> str:
        return self.name
    
    def set_name(self, value : str) -> None:
        self.name = value
        pass

    def get_attr_type(self) -> Any:
        return self.attr_type
    
    def set_attr_type(self, value : Any) -> None:
        self.attr_type = value
        pass

    def get_auto_increment(self) -> bool:
        return self.auto_increment
    
    def set_auto_increment(self, value : bool) -> None:
        self.auto_increment = value
    
    def is_not_null(self) -> bool:
        return self.not_null
    
    def set_not_null(self, value : bool) -> None:
        self.not_null = value
    
    def is_primary_key(self) -> bool:
        return self.primary_key
    
    def set_primary_key(self, value : bool) -> None:
        self.primary_key = value
    
    def is_foreign_key(self) -> bool:
        return self.foreign_key
    
    def set_foreign_key(self, value : bool) -> None:
        self.foreign_key = value
    
    def get_referenced_table(self) -> str:
        return self.referenced_table
    
    def set_referenced_table(self, value : str) -> None:
        self.referenced_table = value

    def is_unique(self) -> bool:
        return self.unique
    
    def set_unique(self, value : bool) -> None:
        self.unique = value

    def __eq__(self, value: object) -> bool:
        if type(value) is Attribute:
            if self.get_name() == value.get_name():
                return True 
        return False
    
    def __hash__(self) -> int:
        return hash(self.name) * 6