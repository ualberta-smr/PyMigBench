from core.Arguments import Arguments
from db.Db import Db
from query.Query import Query


class Detail(Query):
    def __init__(self, db: Db, arguments: Arguments):
        self.db = db
        self.arguments = arguments

    def run(self):
        item = self.db.get_item(self.arguments.data_types[0], self.arguments.filters["id"])
        if not item:
            print("No items found")
        else:
            print(item.get_raw_content())
