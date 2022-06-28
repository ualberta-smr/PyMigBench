from db.Db import Db
from query.Query import Query


class Listing(Query):
    def __init__(self, db: Db, options: str):
        self.db = db
        self.options = options

    def run(self):
        key = self.options
        list = self.db.get_list(key)
        for i, item in enumerate(list, start=1):
            print(f"{i} {item.id}")
