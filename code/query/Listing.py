from core.Arguments import Arguments
from db.DataItem import DataItem
from db.Db import Db
from query.Query import ListQuery


class Listing(ListQuery):
    def __init__(self, db: Db, arguments: Arguments):
        self.db = db
        self.arguments = arguments

    def apply_filter(self) -> list[DataItem]:
        return self.db.filter_list(self.arguments.data_types[0], self.arguments.filters)

    def item_to_string(self, item: DataItem, index: int):
        return item.id

