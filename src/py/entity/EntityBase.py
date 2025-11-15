from abc import ABC


class EntityBase(ABC):

    def __init__(self, id: int):
        super().__init__()
        self.id = id

    def get_id(self) -> int:
        return self.id

    def set_id(self, value: int) -> None:
        self.id = value
