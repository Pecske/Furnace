from table.TableBase import TableBase
from utils.QueryDescriptor import QueryDescriptor
from utils.TableDescriptor import TableDescriptor
from utils.Attribute import Attribute
from table.PanelNameTable import PanelNameTable

class PanelTable(TableBase):
    TABLE = "Panel"
    PANEL_NAME_ID = "PanelNameID"
    TIME = "Time"
    VALUE = "Value"

    ATTRIBUTES : list[Attribute] = [
        Attribute(TableBase.ID,int,auto_increment= True,primary_key= True),
        Attribute(PANEL_NAME_ID,int, foreign_key=True, referenced_table= PanelNameTable.TABLE),
        Attribute(TIME,str),
        Attribute(VALUE, int)
    ]

    @staticmethod
    def get_all_attributes() -> list[Attribute]:
        return PanelTable.ATTRIBUTES

    @staticmethod
    def get_attribute_names() -> list[str]:
        names : list[str] = list()
        for attribute in PanelNameTable.ATTRIBUTES:
            names.append(attribute.get_name())
        return names

    @staticmethod
    def create_table() -> QueryDescriptor:
        panel_name_table = TableDescriptor(PanelNameTable.TABLE,PanelNameTable.get_all_attributes())
        foreign_key_ref = {panel_name_table:{PanelTable.PANEL_NAME_ID:TableBase.ID}}
        params = {PanelTable.TABLE:PanelTable.get_attribute_names()}
        return QueryDescriptor(TableDescriptor(PanelTable.TABLE,PanelTable.get_all_attributes(),foreign_key_ref),params)
    
    @staticmethod
    def get_insert() -> QueryDescriptor:
        params = {PanelTable.TABLE:[PanelTable.PANEL_NAME_ID,PanelTable.TIME,PanelTable.VALUE]}
        columns : list[Attribute] = list()
        for attribute in PanelTable.ATTRIBUTES:
            if attribute.get_name() is not TableBase.ID:
                columns.append(attribute)
        return QueryDescriptor(TableDescriptor(PanelTable.TABLE,columns),params)

    @staticmethod
    def get_update() -> QueryDescriptor:
        columns : list[Attribute] = list()
        for attribute in PanelTable.ATTRIBUTES:
            if attribute.primary_key is False:
                columns.append(attribute)
        panel_table = TableDescriptor(PanelTable.TABLE,columns)
        where = {PanelTable.TABLE:[TableBase.ID]}
        return QueryDescriptor(panel_table,where)
    
    @staticmethod
    def get_select_by_id() -> QueryDescriptor:
        panel_name_table = TableDescriptor(PanelNameTable.TABLE,PanelNameTable.get_all_attributes())
        join = {panel_name_table:{PanelTable.PANEL_NAME_ID:TableBase.ID}}
        panel_table = TableDescriptor(PanelTable.TABLE,PanelTable.get_all_attributes(),join)
        params = {PanelTable.TABLE:[TableBase.ID]}
        return QueryDescriptor(panel_table,params)
        
    @staticmethod
    def get_select_all() -> QueryDescriptor:
        panel_name_table = TableDescriptor(PanelNameTable.TABLE,PanelNameTable.get_all_attributes())
        join = {panel_name_table:{PanelTable.PANEL_NAME_ID:TableBase.ID}}
        panel_table = TableDescriptor(PanelTable.TABLE,PanelTable.get_all_attributes(),join)
        return QueryDescriptor(panel_table) 

    @staticmethod
    def get_delete_by_id() -> QueryDescriptor:
        panel_table = TableDescriptor(PanelTable.TABLE)
        where = {PanelTable.TABLE:[TableBase.ID]}
        return QueryDescriptor(panel_table,where)  