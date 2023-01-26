from enum import Enum

from db.Db import DataItem


class ResultDisplayOption(Enum):
    COUNT_ONLY = "count_only"
    DATA_ONLY = "data_only"
    COUNT_AND_DATA = "count_and_data"


class Result:
    def __init__(self, items: list[DataItem], display_option: ResultDisplayOption):
        self.count = len(items)
        self.items = items
        self.display_option = display_option
