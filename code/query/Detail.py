from db.Db import DataItem
from query.Query import ListQuery


class Detail(ListQuery):
    def format_item(self, item: DataItem):
        return item
