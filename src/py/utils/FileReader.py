import pandas as pd


class FileReader:
    DELIMITER = ";"

    def __init__(self):
        pass

    def read_from_csv(self, path: str) -> pd.DataFrame:
        try:
            df: pd.DataFrame = pd.read_csv(path, delimiter=self.DELIMITER)
        except Exception as e:
            df: pd.DataFrame = pd.read_csv(path, delimiter=self.DELIMITER, encoding="windows-1252")
        return df.dropna()
