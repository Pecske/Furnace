from service.PanelNameService import PanelNameService
from entity.PanelName import PanelName
from utils.Wrapper import Wrapper


class PanelNameController:
    def __init__(self, panel_name_service: PanelNameService) -> None:
        self.service = panel_name_service
        pass

    def save_batch(self, data: Wrapper[list[PanelName]]) -> Wrapper[list[PanelName]]:
        result: Wrapper[list[PanelName]] = Wrapper()
        panel_names = data.get_wrapped()
        if panel_names is not None:
            try:
                self.service.save_batch(panel_names)
                result.set_wrapped(self.service.get_all())
            except Exception as e:
                result.add_exception(str(e))

        return result
