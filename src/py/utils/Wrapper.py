from typing import TypeVar, Generic

T = TypeVar("T")

class Wrapper(Generic[T]):
    def __init__(self, wrapped : T | None = None, exceptions : list[str] = list()) -> None:
        super().__init__()
        self.wrapped = wrapped
        self.exceptions = exceptions
    
    def get_wrapped(self) -> T | None:
        return self.wrapped
    
    def set_wrapped(self, value : T):
        self.wrapped = value

    def get_exceptions(self) -> list[str]:
        return self.exceptions
    
    def set_exceptions(self, value : list[str]) -> None:
        self.exceptions = value
    
    def add_exception(self, message : str) -> None:
        self.exceptions.append(message)