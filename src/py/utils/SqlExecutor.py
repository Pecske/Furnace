import sqlite3 as sql
from typing import Any, Type
from entity.EntityBase import EntityBase
from table.TableBase import TableBase
from utils.SqlHelper import SqlHelper
from utils.QueryDescriptor import QueryDescriptor
from collections.abc import Sequence



class SqlExecutor:
    def __init__(self, db_name : str, table: Type[TableBase]) -> None:
        self.db_name = db_name
        self.table = table
        pass

    def __get_params_from_query(self, entity : EntityBase, query : QueryDescriptor) -> list[Any]:
        params : list[Any] = list()
        query_params = query.get_params().values()
        if len(query_params) > 0:
            for query_param in query_params:
                for param in query_param:
                    param_value = entity.get_value_by_attribute(param)
                    if param is TableBase.ID and param_value == 0:
                        pass
                    else:
                        params.append(param_value)
        return params

    def __get_params_script(self, entity: EntityBase,query_params : list[str]) -> str:
        result = str()
        for query_param in query_params:
            value = entity.get_value_by_attribute(query_param)
            result += f"\"{value}\","
        return result[:len(result)-1]

    
    def create_table(self) -> int | None:  
        query = self.table.create_table()
        script = SqlHelper.create_table(query)
        return self.execute(script)

    def save_batch(self, entities : Sequence[EntityBase]) -> None:
        multi_insert = str()
        query = self.table.get_insert()
        single_insert = SqlHelper.create_insert_statement(query,False)
        for entity in entities:            
            param_script = self.__get_params_script(entity,query.get_flattened_params())
            multi_insert += single_insert + f"VALUES({param_script});"

        script = f"BEGIN TRANSACTION; {multi_insert} COMMIT TRANSACTION;"
        self.execute_batch(script)
        pass

    def save(self, entity : EntityBase) -> int | None:  
        query = self.table.get_insert()
        script = SqlHelper.create_insert_statement(query)
        return self.execute(script,self.__get_params_from_query(entity,query))
    
    def update(self, entity : EntityBase)-> int | None:  
        query = self.table.get_update()
        script = SqlHelper.create_update_statement_by_id(query)
        params = self.__get_params_from_query(entity,query)            
        return self.execute(script,params)    
    
    def get_by_id(self,id: int) -> list[Any]:  
        script = SqlHelper.create_select(self.table.get_select_by_id())
        return self.execute_select(script,[id])
    
    def get_all(self) -> list[Any]:  
        script = SqlHelper.create_select(self.table.get_select_all())
        return self.execute_select(script)
    
    def delete_by_id(self,id : int) -> None:
        script = SqlHelper.create_delete_statement_by_id(self.table.get_delete_by_id())
        self.execute(script,[id])
    
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
    
    def execute_batch(self, script : str) -> int | None:        
        try:
            results : int | None = None
            connection = sql.connect(self.db_name, timeout= 30)
            with connection:
                executed = connection.executescript(script)                 
            connection.close()
            return results
        except Exception as e:
            raise Exception(str(e))

    