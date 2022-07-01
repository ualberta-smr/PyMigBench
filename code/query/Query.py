from abc import ABC, abstractmethod

from core.Arguments import Arguments
from db.DataItem import DataItem
from db.Db import Db
from query.Result import Result


class Query(ABC):
    def __init__(self, db: Db, arguments: Arguments):
        self.db = db
        self.arguments = arguments

    @abstractmethod
    def run(self) -> Result:
        pass


class ListQuery(Query):
    def run(self) -> Result:
        items = self.db.filter_list(self.arguments.data_types[0], self.arguments.filters)
        formatted_items = [self.format_item(item) for item in items]
        return Result(formatted_items)

    @abstractmethod
    def format_item(self, item: DataItem) -> object:
        pass
