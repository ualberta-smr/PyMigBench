from db.Db import Db
from query.Query import Query


class Detail(Query):
    def __init__(self, db: Db, type: str, id: str):
        self.db = db
        self.type = type
        self.id = id

    def run(self):
        item = self.db.get_item(self.type, self.id)
        if not item:
            print("No items found")
        else:
            print(item.get_raw_content())
