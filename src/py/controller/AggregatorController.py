from service.Aggregator import Aggregator
from entity.Panel import Panel
from dto.PanelCountData import PanelCountData
from dto.PanelStatisticsData import PanelStatisticsData
from utils.Wrapper import Wrapper

class AggregatorController:
    def __init__(self, aggregator : Aggregator) -> None:
        self.aggregator = aggregator
        pass

    def get_full_panel_data_by_id(self, data : Wrapper[int]) -> Wrapper[Panel]:
        id = data.get_wrapped()
        result : Wrapper[Panel] = Wrapper()
        if id is not None:
            try:
                result.set_wrapped(self.aggregator.get_panel_with_name_by_id(id))
            except Exception as e:
                result.add_exception(str(e))
        else:
            result.add_exception("Missing ID!!!")
        return result
    
    def get_all_full_panels(self) -> Wrapper[list[Panel]]:
        result : Wrapper[list[Panel]] = Wrapper()
        try:
           result.set_wrapped(self.aggregator.get_all_panels_with_names())
        except Exception as e:
            result.add_exception(str(e))
        return result
    
    def get_distinct_panel_counts(self) -> Wrapper[list[PanelCountData]]:
        result : Wrapper[list[PanelCountData]] = Wrapper()
        try:
            result.set_wrapped(self.aggregator.get_panel_count())
        except Exception as e:
            result.add_exception(str(e))
        return result
    
    def get_panel_stats(self) -> Wrapper[list[PanelStatisticsData]]:
        result : Wrapper[list[PanelStatisticsData]] = Wrapper()
        try:
            result.set_wrapped(self.aggregator.get_panel_statistics())
        except Exception as e:
            result.add_exception(str(e))
        return result
