from db.Db import DataItem
from query.Query import ListQuery


class Listing(ListQuery):
    def format_item(self, item: DataItem):
        return item["id"]
