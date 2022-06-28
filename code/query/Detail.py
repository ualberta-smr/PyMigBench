from core.Arguments import Arguments
from db.Db import Db
from query.Query import Query


class Detail(Query):
    def __init__(self, db: Db, arguments: Arguments):
        self.db = db
        self.arguments = arguments

    def run(self):
        items = self.db.filter_list(self.arguments.data_types[0], self.arguments.filters)
        if not items:
            print("No items found")
            return
        for i, item in enumerate(items, start=1):
            print(f"== item {i} ==")
            print(item.get_raw_content().strip())
            print()
