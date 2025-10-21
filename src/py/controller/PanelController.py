from service.PanelService import PanelService
from service.PanelNameService import PanelNameService
from entity.Panel import Panel
from utils.Wrapper import Wrapper

class PanelController:

    def __init__(self, panel_service : PanelService, panel_name_service : PanelNameService) -> None:
        self.panel_service = panel_service
        self.panel_name_service = panel_name_service

    def create_table(self) -> Wrapper[Panel]:
        result : Wrapper[Panel] = Wrapper()
        try:
            self.panel_name_service.create_table()
            self.panel_service.create_table()
        except Exception as e:
            result.add_exception(str(e))        
        return result
    
    def save_batch(self, data:Wrapper[list[Panel]]) -> Wrapper[list[Panel]]:
        result : Wrapper[list[Panel]] = Wrapper()
        panels = data.get_wrapped()
        if panels is not None:
            try:
                self.panel_service.save_batch(panels)
            except Exception as e:
                result.add_exception(str(e))
        else:
            result.add_exception("Missing Batch Data!!!")
        return result
    
    def save_or_update(self, data : Wrapper[Panel]) -> Wrapper[Panel]:
        panel = data.get_wrapped()
        result : Wrapper[Panel] = Wrapper()
        if panel is not None:
            try:
                saved_name = self.panel_name_service.save_or_update(panel.get_panel_name())
                panel.set_panel_name(saved_name)
                saved_panel = self.panel_service.save_or_update(panel)
                result.set_wrapped(saved_panel)
            except Exception as e:
                result.add_exception(str(e))
        else:
            result.add_exception("Missing Panel Data!!!")
        return result
    
    def select_by_id(self, data : Wrapper[int]) -> Wrapper[Panel]:
        id = data.get_wrapped()
        result : Wrapper[Panel] = Wrapper()
        if id is not None:
            try:
               found = self.panel_service.get_by_id(id)
               result.set_wrapped(found)
            except Exception as e:
                result.add_exception(str(e))
        else:
            result.add_exception("Missing Panel ID!!!")
        return result
    
    def select_all(self) -> Wrapper[list[Panel]]:
        result : Wrapper[list[Panel]] = Wrapper()
        try:
            panels = self.panel_service.get_all()
            result.set_wrapped(panels)
        except Exception as e:
            result.add_exception(str(e))
        return result
    
    def delete_by_id(self, data : Wrapper[int]) -> Wrapper[Panel]:
        id = data.get_wrapped()
        result : Wrapper[Panel] = Wrapper()
        if id is not None:
            try:
                self.panel_service.delete_by_id(id)
            except Exception as e:
                result.add_exception(str(e))
        else:
            result.add_exception("Missing Panel ID!!!")
        return result
        
