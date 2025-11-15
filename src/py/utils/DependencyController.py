from typing import TypeVar, Type, Any
from repository.PanelRepository import PanelRepository
from repository.PanelNameRepository import PanelNameRepository
from repository.PortionRepository import PortionRepository
from service.PanelService import PanelService
from service.PanelNameService import PanelNameService
from service.PortionService import PortionService
from controller.PanelController import PanelController
from controller.PanelNameController import PanelNameController
from controller.PortionController import PortionController
from utils.FileReader import FileReader

T = TypeVar("T")

class DependencyController:

    _instance = None

    def __init__(self) -> None:
        self.dependencies = dict()
        self.class_dict = {
            PanelRepository : (self.__get_panel_repo,True),
            PanelNameRepository : (self.__get_panel_name_repo,True),
            PanelService : (self.__get_panel_service,True),
            PanelNameService: (self.__get_panel_name_service,True),
            PanelController : (self.__get_panel_controller,True),
            PanelNameController : (self.__get_panel_name_controller, True),
            FileReader : (self.__get_file_reader,False),
            PortionController : (self.__get_portion_controller,True),
        }
        pass

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DependencyController()
        return cls._instance
    
    def build(self, instance_name : Type[T], params : Any | None = None) -> T:        
        if instance_name in self.class_dict:
            builder_has_param = self.class_dict.get(instance_name)
            if builder_has_param is not None:
                if params is not None and len(builder_has_param) > 1 and builder_has_param[1]:
                    parametered_dependency = builder_has_param[0](params)
                    if parametered_dependency is not None:
                        return parametered_dependency
                    else:
                        raise Exception("Class can't be built!!!")
                else:
                    parameterless_dependency = builder_has_param[0]()
                    if parameterless_dependency is not None:
                        return parameterless_dependency
                    else:
                        raise Exception("Class can't be built!!!")
            else:
                raise Exception("No Builder for this Class!!!")
        else:
            raise Exception("Invalid Class!!!")

    
    def __get_panel_repo(self, db_name: str) -> PanelRepository:
        if PanelRepository not in self.dependencies:
            self.dependencies[PanelRepository] = PanelRepository(db_name)
        return self.dependencies[PanelRepository]        

    def __get_panel_name_repo(self, db_name : str) -> PanelNameRepository:
        if PanelNameRepository not in self.dependencies:
            self.dependencies[PanelNameRepository] = PanelNameRepository(db_name)
        return self.dependencies[PanelNameRepository]
    
    def __get_portion_repo(self, db_name : str) -> PortionRepository:
        if PortionRepository not in self.dependencies:
            self.dependencies[PortionRepository] = PortionRepository(db_name)
        return self.dependencies[PortionRepository]
    
    def __get_panel_service(self, db_name:str) -> PanelService:
        if PanelService not in self.dependencies:
            self.dependencies[PanelService] = PanelService(self.__get_panel_repo(db_name))
        return self.dependencies[PanelService]
    
    def __get_panel_name_service(self, db_name: str) -> PanelNameService:
        if PanelNameService not in self.dependencies:
            self.dependencies[PanelNameService] = PanelNameService(self.__get_panel_name_repo(db_name))
        return self.dependencies[PanelNameService]
    
    def __get_portion_service(self,db_name : str) -> PortionService:
        if PortionService not in self.dependencies:
            self.dependencies[PortionService] = PortionService(self.__get_portion_repo(db_name))
        return self.dependencies[PortionService]
    
    def __get_panel_controller(self,db_name : str) -> PanelController:
        if PanelController not in self.dependencies:
            self.dependencies[PanelController] = PanelController(self.__get_panel_service(db_name),self.__get_panel_name_service(db_name))
        return self.dependencies[PanelController]
    
    def __get_panel_name_controller(self,db_name : str) -> PanelNameController:
        if PanelNameController not in self.dependencies:
            self.dependencies[PanelNameController] = PanelNameController(self.__get_panel_name_service(db_name))
        return self.dependencies[PanelNameController]
    
    def __get_portion_controller(self,db_name : str) -> PortionController:
        if PortionController not in self.dependencies:
            self.dependencies[PortionController] = PortionController(self.__get_portion_service(db_name))
        return self.dependencies[PortionController]
    
    def __get_file_reader(self) -> FileReader:
        if FileReader not in self.dependencies:
            self.dependencies[FileReader] = FileReader()
        return self.dependencies[FileReader]