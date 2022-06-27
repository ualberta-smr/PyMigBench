import os.path
import argparse

from db.Db import Db
from query.Summarize import Summarization


def get_args():
    parser = argparse.ArgumentParser(description="query PyMigBench")
    parser.add_argument("--summary", nargs='+', required=False, default="all",
                        help="summaries of data. use 'all' to print all data. "
                             "Or pass one or more of 'lp', 'mg' and 'cc'")
    return parser.parse_args()


def main():
    args = get_args()
    print(args)
    db = Db(os.path.abspath("../data"))
    db.load()

    if args.summary:
        summarize = Summarization(db, args.summary)
        summarize.run()


if __name__ == '__main__':
    main()
