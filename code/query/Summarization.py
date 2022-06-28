from core.Constants import DataTypeName, DataTypeKeys
from db.Db import Db
from query.Query import Query


class Summarization(Query):
    def __init__(self, db: Db, filters: list[str]):
        self.db = db
        self.type_keys = filters

    def run(self):
        options = self.type_keys
        if not options or "all" in options:
            options = DataTypeKeys

        for key in options:
            print(f"{len(self.db.get_list(key))} {DataTypeName[key]}")
