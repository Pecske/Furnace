from typing import Any

class ScriptDefinition:
    def __init__(self, script : str, params : tuple[Any,...] | None = None) -> None:
        self.script = script
        self.params = params
    
    def get_script(self) -> str:
        return self.script
    
    def set_script(self,value : str) -> None:
        self.script = value
    
    def get_params(self) -> tuple[Any,...] | None:
        return self.params
    
    def set_params(self, value : tuple[Any,...] | None)-> None:
        self.params = value