from abc import ABC, abstractmethod
from typing import Any

class EntityBase(ABC):

    def __init__(self, id : int):
        super().__init__()
        self.id = id
        self.attribute_values = self._get_attribute_values()    
    
    def get_id(self) -> int:
        return self.id

    def set_id(self, value: int) -> None:
        self.id = value    
    
    def get_value_by_attribute(self,attribute : str) -> Any:
        return self.attribute_values.get(attribute)
    
    @abstractmethod
    def _get_attribute_values(self) -> dict[str,Any]:
        raise NotImplementedError  