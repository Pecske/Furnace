from service.PortionService import PortionService
from entity.Portion import Portion
from utils.Wrapper import Wrapper

class PortionController:

    def __init__(self, portion_service : PortionService) -> None:
        self.portion_service = portion_service

    def create_table(self) -> Wrapper[Portion]:
        result : Wrapper[Portion] = Wrapper()
        try:
            self.portion_service.create_table()
        except Exception as e:
            result.add_exception(str(e))        
        return result
    
    def save_batch(self, data:Wrapper[list[Portion]]) -> Wrapper[list[Portion]]:
        result : Wrapper[list[Portion]] = Wrapper()
        portions = data.get_wrapped()
        if portions is not None:
            try:
                self.portion_service.save_batch(portions)
            except Exception as e:
                result.add_exception(str(e))
        else:
            result.add_exception("Missing Batch Data!!!")
        return result
    
    def save_or_update(self, data : Wrapper[Portion]) -> Wrapper[Portion]:
        portion = data.get_wrapped()
        result : Wrapper[Portion] = Wrapper()
        if portion is not None:
            try:
                saved_portion = self.portion_service.save_or_update(portion)
                result.set_wrapped(saved_portion)
            except Exception as e:
                result.add_exception(str(e))
        else:
            result.add_exception("Missing Portion Data!!!")
        return result
    
    def select_by_id(self, data : Wrapper[int]) -> Wrapper[Portion]:
        id = data.get_wrapped()
        result : Wrapper[Portion] = Wrapper()
        if id is not None:
            try:
               found = self.portion_service.get_by_id(id)
               result.set_wrapped(found)
            except Exception as e:
                result.add_exception(str(e))
        else:
            result.add_exception("Missing Portion ID!!!")
        return result
    
    def select_all(self) -> Wrapper[list[Portion]]:
        result : Wrapper[list[Portion]] = Wrapper()
        try:
            portions = self.portion_service.get_all()
            result.set_wrapped(portions)
        except Exception as e:
            result.add_exception(str(e))
        return result
    
    def delete_by_id(self, data : Wrapper[int]) -> Wrapper[Portion]:
        id = data.get_wrapped()
        result : Wrapper[Portion] = Wrapper()
        if id is not None:
            try:
                self.portion_service.delete_by_id(id)
            except Exception as e:
                result.add_exception(str(e))
        else:
            result.add_exception("Missing Portion ID!!!")
        return result
        
