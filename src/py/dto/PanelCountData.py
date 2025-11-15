class PanelCountData:
    def __init__(self, name: str, count: int) -> None:
        self.name = name
        self.count = count

    def get_name(self) -> str:
        return self.name

    def set_name(self, value: str) -> None:
        self.name = value

    def get_count(self) -> int:
        return self.count

    def set_count(self, value: int) -> None:
        self.count = value

    def __str__(self) -> str:
        return f"Name: {self.get_name()}\tNumber of Values: {self.get_count()}"
