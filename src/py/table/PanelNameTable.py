from table.TableBase import TableBase
from utils.QueryDescriptor import QueryDescriptor
from utils.TableDescriptor import TableDescriptor
from utils.Attribute import Attribute

class PanelNameTable(TableBase):
    TABLE = "PanelName"
    NAME = "Name"

    ATTRIBUTES : list[Attribute] = [
        Attribute(TableBase.ID,int,auto_increment= True,primary_key= True),
        Attribute(NAME,str,unique=True, not_null=True)
    ]
    
    @staticmethod
    def get_all_attributes() -> list[Attribute]:
        return PanelNameTable.ATTRIBUTES
    
    @staticmethod
    def get_attribute_names() -> list[str]:
        names : list[str] = list()
        for attribute in PanelNameTable.ATTRIBUTES:
            names.append(attribute.get_name())
        return names
    
    @staticmethod
    def create_table() -> QueryDescriptor:
        params = {PanelNameTable.TABLE:PanelNameTable.get_attribute_names()}
        return QueryDescriptor(TableDescriptor(PanelNameTable.TABLE,PanelNameTable.get_all_attributes()),params)

    @staticmethod
    def get_insert() -> QueryDescriptor:
        params = {PanelNameTable.TABLE:[PanelNameTable.NAME]}
        columns : list[Attribute] = list()
        for attribute in PanelNameTable.ATTRIBUTES:
            if attribute.get_name() is not TableBase.ID:
                columns.append(attribute)
        return QueryDescriptor(TableDescriptor(PanelNameTable.TABLE,columns),params)

    @staticmethod
    def get_update() -> QueryDescriptor:
        columns : list[Attribute] = list()
        where_columns : list[str] = list()
        for attribute in PanelNameTable.ATTRIBUTES:
            if attribute.primary_key is False:
                columns.append(attribute)
            else:
                where_columns.append(attribute.get_name())
        table = TableDescriptor(PanelNameTable.TABLE,columns)
        params = {PanelNameTable.TABLE:where_columns}
        return QueryDescriptor(table,params)
    
    @staticmethod
    def get_select_by_id() -> QueryDescriptor:
        where = {PanelNameTable.TABLE:[TableBase.ID]}
        return QueryDescriptor(TableDescriptor(PanelNameTable.TABLE,PanelNameTable.get_all_attributes()),where)
    
    @staticmethod
    def get_select_all() -> QueryDescriptor:
        return QueryDescriptor(TableDescriptor(PanelNameTable.TABLE,PanelNameTable.get_all_attributes())) 
    
    @staticmethod
    def get_delete_by_id() -> QueryDescriptor:
        table = TableDescriptor(PanelNameTable.TABLE)
        where = {PanelNameTable.TABLE:[TableBase.ID]}
        return QueryDescriptor(table,where)  
