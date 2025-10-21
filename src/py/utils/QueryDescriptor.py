from utils.TableDescriptor import TableDescriptor
import itertools

class QueryDescriptor:
    def __init__(self,table : TableDescriptor, params : dict[str,list[str]] = dict()) -> None:
        self.table = table
        self.params = params
        pass

    def get_table(self) -> TableDescriptor:
        return self.table
    
    def set_table(self, value : TableDescriptor) -> None:
        self.table = value

    def get_params(self) -> dict[str,list[str]] :
        return self.params
    
    def set_params(self, value : dict[str,list[str]] ):
        self.params = value
    
    def get_flattened_params(self) -> list[str]:
        return list(itertools.chain.from_iterable(self.params.values()))
