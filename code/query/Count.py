from core.Arguments import Arguments
from core.Constants import DataTypeName, DataTypeKeys
from db.Db import Db
from query.Query import Query


class Count(Query):
    def __init__(self, db: Db, arguments: Arguments):
        self.db = db
        self.arguments = arguments

    def run(self):
        data_types = self.arguments.data_types
        if not data_types or "all" in data_types:
            data_types = DataTypeKeys

        for dt in data_types:
            print(f"{len(self.db.get_list(dt))} {DataTypeName[dt]}")
