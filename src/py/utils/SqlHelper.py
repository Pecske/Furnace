from utils.QueryDescriptor import QueryDescriptor
from utils.TableDescriptor import TableDescriptor
from utils.Attribute import Attribute
from typing import Type, Any

class SqlHelper:

    SEPARATOR = ","
    AND = "AND"
    INTEGER = "INTEGER"
    TEXT = "TEXT"

    def __init__(self) -> None:
        pass

    @staticmethod
    def __convert_type(type : Type[Any]) -> str:
        if type == int:
            return SqlHelper.INTEGER
        else:
            return SqlHelper.TEXT


    @staticmethod
    def __add_columns_from_attributes(attributes : list[Attribute], table_name:str | None = None)-> str:
        column_str = str()
        if table_name is not None:
            for attribute in attributes:
                column_str += f"{table_name}.{attribute.get_name()}{SqlHelper.SEPARATOR}"
        else:
            for attribute in attributes:
                column_str += f"{attribute.get_name()}{SqlHelper.SEPARATOR}"
        clean_column_length = len(column_str) - len(SqlHelper.SEPARATOR)
        return column_str[:clean_column_length]

    @staticmethod
    def __get_inner_join_statement(from_table : str, to_table : str, fk_pk_dict : dict[str,str]) -> str:
        connection_str = str()
        for foreign_key, primary_key in fk_pk_dict.items():
            connection_str += f"{from_table}.{foreign_key} = {to_table}.{primary_key} {SqlHelper.AND} "
            
        clean_connection_length = len(connection_str) - len(SqlHelper.AND) - 1
        return f"INNER JOIN {to_table} ON {connection_str[:clean_connection_length]} "
    
    @staticmethod
    def __get_where_statement(table_column_dict : dict[str,list[str]]) -> str:
        script = str()
        if len(table_column_dict) > 0:
            script = "WHERE "
            for table_name, column_names in table_column_dict.items():
                for column_name in column_names:
                    script += f"{table_name}.{column_name} = ? {SqlHelper.AND} "
            clean_script_length = len(script) - len(SqlHelper.AND) - 1
            script = script[:clean_script_length]
        return script
    
    @staticmethod
    def __get_foreign_key_references(attributes: list[Attribute], connections : dict[TableDescriptor,dict[str,str]]) -> str:
        script = str()
        for attribute in attributes:
            foreign_keys = str()
            references = str()
            for table, fk_pk in connections.items():
                if attribute.get_referenced_table() == table.get_table_name():
                    for fk, pk in fk_pk.items():
                        foreign_keys += f"{fk}{SqlHelper.SEPARATOR}"
                        references += f"{pk}{SqlHelper.SEPARATOR}"
                    clean_foreign_length = len(foreign_keys) - len(SqlHelper.SEPARATOR)
                    clean_reference_length = len(references) - len(SqlHelper.SEPARATOR)
                    script += f"FOREIGN KEY ({foreign_keys[:clean_foreign_length]}) REFERENCES {attribute.get_referenced_table()}({references[:clean_reference_length]}){SqlHelper.SEPARATOR}"
        clean_script_length = len(script) - len(SqlHelper.SEPARATOR)
        return script[:clean_script_length]

    
    @staticmethod
    def create_table(query : QueryDescriptor) -> str:
        table = query.get_table()
        attributes = table.get_attributes()
        foreign_keys : set[Attribute] = set()
        columns = str()
        primary_key = str()
        not_null = str()
        unique = str()
        for attribute in attributes:
            if attribute.is_primary_key():
                primary_key += f"{attribute.get_name()}{SqlHelper.SEPARATOR}"
            if attribute.is_foreign_key() and len(table.get_connections()) > 0:
                foreign_keys.add(attribute)
            if attribute.is_not_null():
                not_null = "NOT NULL "
            if attribute.is_unique():
                unique = "UNIQUE "
            columns += f"{attribute.get_name()} {SqlHelper.__convert_type(attribute.get_attr_type())}{not_null}{unique}{SqlHelper.SEPARATOR}"

        clean_colum_length = len(columns) - len(SqlHelper.SEPARATOR)
        clean_primary_length = len(primary_key) - len(SqlHelper.SEPARATOR)
        foreign_key_script = SqlHelper.__get_foreign_key_references(attributes,table.get_connections())

        return f"CREATE TABLE IF NOT EXISTS {table.get_table_name()}({columns[:clean_colum_length]}, PRIMARY KEY({primary_key[:clean_primary_length]}) {foreign_key_script})"
        
    @staticmethod
    def create_select(query : QueryDescriptor) -> str:
        table = query.get_table()
        columns = SqlHelper.__add_columns_from_attributes(table.get_attributes(),table.get_table_name())
        join_statement = str()
        if len(table.get_connections()) > 0:
            for foreign_table, connection in table.get_connections().items():
                columns += f"{SqlHelper.SEPARATOR}{SqlHelper.__add_columns_from_attributes(foreign_table.get_attributes(),foreign_table.get_table_name())}"
                join_statement += SqlHelper.__get_inner_join_statement(table.get_table_name(),foreign_table.get_table_name(),connection)
        script = f"SELECT {columns} FROM {table.get_table_name()} {join_statement} {SqlHelper.__get_where_statement(query.get_params())}"
        return script

    @staticmethod
    def create_insert_statement(query : QueryDescriptor, with_values : bool = True) -> str:
        table = query.get_table()
        attributes = table.get_attributes()
        columns = SqlHelper.__add_columns_from_attributes(attributes)
        params_script = str()
        if with_values:
            params = str()
            counter = 0
            while counter < len(query.get_params()):
                params += f"?,"
                counter += 1
            params_length = len(params)            
            params_script += f"VALUES({params[:params_length- 1]})"
        script = f"INSERT INTO {table.get_table_name()}({columns}) {params_script}"
        return script

    @staticmethod
    def create_update_statement_by_id(query : QueryDescriptor) -> str:
        table = query.get_table()
        columns = str()
        for attribute in table.get_attributes():
            columns += f"{attribute} = ?,"
        
        columns_length = len(columns)
        script = f"UPDATE {table.get_table_name()} SET {columns[:columns_length - 1]} {SqlHelper.__get_where_statement(query.get_params())}"

        return script  

    @staticmethod
    def create_delete_statement_by_id(query : QueryDescriptor) -> str:
        table = query.get_table()
        return f"DELETE FROM {table.get_table_name()} {SqlHelper.__get_where_statement(query.get_params())}"