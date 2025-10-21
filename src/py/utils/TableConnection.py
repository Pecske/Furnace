class TableConnection:
    def __init__(self, foreign_table : str, fk_pk_dict : dict[str,str] ) -> None:
        self.foreign_table = foreign_table
        self.fk_pk_dict = fk_pk_dict

    def get_foreign_table(self) -> str:
        return self.foreign_table

    def set_foreign_table(self, value : str) -> None:
        self.foreign_table = value

    def get_fk_pk_dict(self) -> dict[str,str]:
        return self.fk_pk_dict

    def set_fk_pk_dict(self, value : dict[str,str]) -> None:
        self.fk_pk_dict = value 