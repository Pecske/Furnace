import os

from controller.PanelController import PanelController
from controller.PanelNameController import PanelNameController
from controller.PortionController import PortionController
from controller.AggregatorController import AggregatorController
from entity.PanelName import PanelName
from entity.Panel import Panel
from entity.Portion import Portion
from dto.PanelCountData import PanelCountData
from dto.PanelStatisticsData import PanelStatisticsData
from utils.FileReader import FileReader
from datetime import datetime
from dateutil import parser
from utils.Wrapper import Wrapper
from typing import Any
from utils.DependencyController import DependencyController
import pandas as pd
import concurrent.futures
import numpy as np
import threading
import time


class Menu:
    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    DB_NAME = os.path.join(BASE_DIR, "data", "Furnace.db")
    ADAG_PATH = os.path.join(BASE_DIR, "data", "Adagok.csv")
    PANEL_PATH = os.path.join(BASE_DIR, "data", "Hutopanelek.csv")
    CONCURRENT_AMOUNT = 10

    LOCK = threading.Lock()

    def __init__(self) -> None:
        self.dependency = DependencyController.get_instance()
        self.filereader = self.dependency.build(FileReader)
        self.panel_controller = self.dependency.build(PanelController, Menu.DB_NAME)
        self.name_controller = self.dependency.build(PanelNameController, Menu.DB_NAME)
        self.portion_controller = self.dependency.build(PortionController, Menu.DB_NAME)
        self.aggregator = self.dependency.build(AggregatorController, Menu.DB_NAME)
        pass

    def __map_panel_from_data(
        self,
        panel_names: list[PanelName],
        data: np.ndarray[tuple[Any, ...], np.dtype[Any]],
    ) -> list[Panel]:
        panels: list[Panel] = list()
        name_index = 0
        time: datetime = datetime.now()
        value: float = 0
        while name_index < len(panel_names):
            time = parser.parse(data[2 * name_index])
            new_value = str(data[(2 * name_index) + 1]).replace(",", ".")
            value = float(new_value)
            panels.append(Panel(panel_names[name_index], time, value))
            name_index += 1
        return panels
    
    def __map_portion_from_data(self,data : np.ndarray[tuple[Any,...],np.dtype[Any]]) -> Portion:
        start : datetime = parser.parse(" ".join((data[1],data[2])))
        end : datetime = parser.parse(" ".join((data[3],data[4])))
        time : int = int(data[5])
        portion_time : int = int(data[6])
        return Portion(start,end,time,portion_time)


    def __save_panel_name_batch(self, data: pd.DataFrame) -> list[PanelName] | None:
        column_names = data.axes[1]
        counter = 0
        column_length = len(column_names)
        panel_names: list[PanelName] = list()
        while counter < column_length:
            name = str(column_names[counter]).split(" [")[0]
            new_name = PanelName(name)
            if new_name not in panel_names:
                panel_names.append(PanelName(name))
            counter += 1

        saved_data = self.name_controller.save_batch(Wrapper(panel_names))
        return saved_data.get_wrapped()

    def __save_panel_batch(
        self, saved_names: list[PanelName], data: pd.DataFrame
    ) -> None:
        data_numpy = data.to_numpy()
        split_amount = int(len(data_numpy) / Menu.CONCURRENT_AMOUNT)
        split_datas = list()
        panels: list[Panel] = list()
        for amount in range(Menu.CONCURRENT_AMOUNT):
            from_amount = 0 if amount == 0 else amount * split_amount
            to_amount = (amount + 1) * split_amount
            split_datas.extend(data_numpy[from_amount:to_amount])
        if len(data_numpy) % split_amount > 0:
            split_datas.extend(data_numpy[split_amount * Menu.CONCURRENT_AMOUNT :])

        with concurrent.futures.ThreadPoolExecutor() as executor:
            try:
                futures: list[concurrent.futures.Future] = list()
                for split_data in split_datas:
                    futures.append(
                        executor.submit(
                            self.__map_panel_from_data, saved_names, split_data
                        )
                    )

                for future in concurrent.futures.as_completed(futures):
                    panels.extend(future.result())
                saved_panels = self.panel_controller.save_batch(Wrapper(panels))
                if len(saved_panels.get_exceptions()) > 0:
                    print(saved_panels.get_exceptions())
            except Exception as e:
                print(str(e))
    
    def __save_portion_batch(self, data : pd.DataFrame) -> list[Portion] | None:
        data_numpy = data.to_numpy()
        portions : list[Portion] = list()
        for single_data in data_numpy:
           portions.append(self.__map_portion_from_data(single_data))
        saved_portions = self.portion_controller.save_batch(Wrapper(portions))
        if len(saved_portions.get_exceptions()) > 0:
            print(saved_portions.get_exceptions())

        return saved_portions.get_wrapped()
    
    def __print_all_counts(self) -> None:
        result = self.aggregator.get_distinct_panel_counts()
        panel_counts = result.get_wrapped()
        if panel_counts is not None:
            title_str = "-------Panel Value Counts-------"
            for panel in panel_counts:
                print(f"{panel}\n")
            end_str = str()
            for c in title_str:
                end_str += "-"
            print(end_str)
        else:
            print(result.get_exceptions())
        
    def __print_panel_stats(self) -> None:
        result = self.aggregator.get_panel_stats()
        panel_stats = result.get_wrapped()
        if panel_stats is not None:
            title_str = "-------Panel Statistics-------"
            print(title_str)
            for panel in panel_stats:                
                print(f"{panel}\n")
            end_str = str()
            for c in title_str:
                end_str += "-"
            print(end_str)
        else:
            print(result.get_exceptions())

    def create_table(self) -> None:
        self.panel_controller.create_table()
        self.portion_controller.create_table()
        print("Table Creation Finished!!!")

    def import_panels(self) -> None:
        data = self.filereader.read_from_csv(Menu.PANEL_PATH)
        name_start_time = time.time()
        saved_names = self.__save_panel_name_batch(data)
        name_end_time = time.time()
        if saved_names is not None:
            print(
                f"Panel name import finished without errors in: {name_end_time-name_start_time}!!!"
            )
            start_time = time.time()
            self.__save_panel_batch(saved_names, data)
            end_time = time.time()
            print(f"Import Finished in: {end_time-start_time}!!!")
        else:
            print("Panel Name Save Error!!!")
    
    def import_portions(self) -> None:
        data = self.filereader.read_from_csv(Menu.ADAG_PATH)
        start_time = time.time()
        saved_portions = self.__save_portion_batch(data)
        end_time = time.time()
        if saved_portions is not None:
            print(f"Portion import finished without errors is: {end_time-start_time}!!!")
        else:
            print("Portion Batch Save Error!!!")

    def show(self) -> None:
        self.__print_all_counts()
        self.__print_panel_stats()
        

