from db.Db import Db
from query.Query import Query


class Summarize(Query):
    def __init__(self, db: Db):
        self.db = db

    def run(self):
        print(f"{len(self.db.lib_pairs)} library pairs")
        print(f"{len(self.db.migrations)} migrations")
        print(f"{len(self.db.code_changes)} code changes")
