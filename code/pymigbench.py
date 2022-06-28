import os.path
import argparse

from db.Db import Db
from query.Listing import Listing
from query.Query import Query
from query.Summarization import Summarization


def get_args():
    parser = argparse.ArgumentParser(description="query PyMigBench")
    parser.add_argument("--summary", nargs='+', required=False,
                        help="summaries of data. use 'all' to print all data. "
                             "Or pass one or more of 'lp', 'mg' and 'cc'")
    parser.add_argument("--list", required=False, help="list ids of all items of a data type")
    return parser.parse_args()


def main():
    args = get_args()
    print(args)
    db = Db(os.path.abspath("../data"))
    db.load()
    query: Query = None
    if args.summary:
        query = Summarization(db, args.summary)
    elif args.list:
        query = Listing(db, args.list)

    if query:
        query.run()


if __name__ == '__main__':
    main()
