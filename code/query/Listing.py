from db.Db import Db
from query.Query import Query


class Listing(Query):
    def __init__(self, db: Db, filters: list[str]):
        self.db = db
        self.type_key = filters[0]

    def run(self):
        list = self.db.get_list(self.type_key)
        for i, item in enumerate(list, start=1):
            print(f"{i} {item.id}")
