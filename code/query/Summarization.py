from core.Constants import DataTypeName, DataTypeKeys
from db.Db import Db
from query.Query import Query


class Summarization(Query):
    def __init__(self, db: Db, options: list[str]):
        self.db = db
        self.options = options

    def run(self):
        options = self.options
        if "all" in options:
            options = DataTypeKeys

        for key in options:
            print(f"{len(self.db.mapping[key])} {DataTypeName[key]}")
