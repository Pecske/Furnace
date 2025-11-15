import sqlite3 as sql
from typing import Any



class SqlExecutor:
    def __init__(self, db_name : str) -> None:
        self.db_name = db_name
        pass

    def execute_select(self, script : str, params : list[Any] | None = None) -> list[Any]:
        try:
            results : list[Any]  = list()
            connection = sql.connect(self.db_name)
            with connection:
                if params is None:
                   executed = connection.execute(script)
                else:
                    executed = connection.execute(script,params)
                results = executed.fetchall()                      
            connection.close()
            return results
        except Exception as e:
            raise Exception(str(e))

    def execute(self, script : str, params : list[Any]| None = None) -> int | None:        
        try:
            results : int | None = None
            connection = sql.connect(self.db_name)
            with connection:
                if params is None:
                   executed = connection.execute(script)
                else:
                    executed = connection.execute(script,params)
                results = executed.lastrowid                      
            connection.close()
            return results
        except Exception as e:
            raise Exception(str(e))
    
    def execute_batch(self, script : str) -> list[Any]:        
        try:
            results : list[Any] | None = list()
            connection = sql.connect(self.db_name, timeout= 30)
            with connection:
                executed = connection.executescript(script)
            results = executed.fetchall()                 
            connection.close()
            return results
        except Exception as e:
            raise Exception(str(e))

    