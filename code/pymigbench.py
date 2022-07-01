import json
import os.path

from core.Arguments import build_arguments
from db.Db import Db
from query.Query import Query
from query.QueryFactory import build_query


def main():
    args = build_arguments()
    db = Db(os.path.abspath("../data"))
    db.load()
    query: Query = build_query(db, args)
    if query:
        result = query.run()
        output = json.dumps(result, indent=2, sort_keys=False, default=vars)
        print(output)
    else:
        print("error building the query")


if __name__ == '__main__':
    main()
