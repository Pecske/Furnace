class PanelStatisticsData:
    def __init__(
        self, name: str, min: float = 0, max: float = 0, avg: float = 0, id: int = 0
    ) -> None:
        self.name = name
        self.min = min
        self.max = max
        self.avg = avg
        self.id = id
        pass

    def get_name(self) -> str:
        return self.name

    def set_name(self, value: str) -> None:
        self.name = value
        pass

    def get_min(self) -> float:
        return self.min

    def set_min(self, value: float) -> None:
        self.min = value
        pass

    def get_max(self) -> float:
        return self.max

    def set_max(self, value: float) -> None:
        self.max = value
        pass

    def get_avg(self) -> float:
        return self.avg

    def set_avg(self, value: float) -> None:
        self.avg = value
        pass

    def get_id(self) -> int:
        return self.id

    def set_id(self, value: int) -> None:
        self.id = value
        pass

    def __str__(self) -> str:
        return f"Name: {self.get_name()} - Min Value: {self.get_min()} - Max Value: {self.get_max()} - Average Value: {self.get_avg()}"
