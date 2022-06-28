from core.Arguments import Arguments
from db.Db import Db
from query.Query import Query


class Listing(Query):
    def __init__(self, db: Db, arguments: Arguments):
        self.db = db
        self.arguments = arguments

    def run(self):
        list = self.db.filter_list(self.arguments.data_types[0], self.arguments.filters)
        if not list:
            print("no results found")
        for i, item in enumerate(list, start=1):
            print(f"{i} {item.id}")
