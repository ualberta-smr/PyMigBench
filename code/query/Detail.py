from db.Db import Db
from query.Query import Query


class Detail(Query):
    def __init__(self, db: Db, filters: list[str]):
        self.db = db
        self.type = filters[0]
        self.id = filters[1]

    def run(self):
        item = self.db.get_item(self.type, self.id)
        if not item:
            print("No items found")
        else:
            print(item.get_raw_content())
