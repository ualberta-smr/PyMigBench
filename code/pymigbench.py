import argparse
import os.path

from db.Db import Db
from query.Query import Query
from query.QueryFactory import build_query


def get_args():
    parser = argparse.ArgumentParser(description="query PyMigBench")
    parser.add_argument("query", nargs='?', default="s",
                        help="One of 'summary' or 'list'. First few letters of the options are also valid.")
    parser.add_argument("-f", "--filter", required=False, nargs='+',
                        help="Filters to the query. Please check query specific documentation")

    return parser.parse_args()


def main():
    args = get_args()
    db = Db(os.path.abspath("../data"))
    db.load()
    query: Query = build_query(db, args.query, args.filter)
    if query:
        query.run()
    else:
        print("error building the query")


if __name__ == '__main__':
    main()
