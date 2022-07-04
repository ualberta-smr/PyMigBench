import json
import os.path

from core.Arguments import build_arguments
from db.Db import Db
from format.JSONFormat import JSONFormat
from query.Query import Query
from core.Factory import build_query


def main():
    args = build_arguments()
    db = Db(os.path.abspath("../data"))
    db.load()
    query: Query = build_query(db, args)
    if query:
        result = query.run()
        output = JSONFormat().format(result)
        print(output)
    else:
        print("error building the query")


if __name__ == '__main__':
    main()
