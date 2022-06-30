import json

from core.Arguments import Arguments
from db.DataItem import DataItem
from db.Db import Db
from query.Query import ListQuery


class Detail(ListQuery):
    def __init__(self, db: Db, arguments: Arguments):
        self.db = db
        self.arguments = arguments

    def apply_filter(self) -> list[DataItem]:
        return self.db.filter_list(self.arguments.data_types[0], self.arguments.filters)

    def item_to_string(self, item: DataItem, item_number: int):
        out = f"== item {item_number} ==\n"
        out += json.dumps(item.__dict__, indent=2, sort_keys=False)
        return out
