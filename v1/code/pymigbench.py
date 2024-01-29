import os.path

from core.Arguments import build_arguments, Arguments
from core.Factory import build_query, build_output_format
from db.Db import Db
from query.Query import Query


def run_query(args: Arguments):
    db = Db(os.path.abspath("../data"))
    db.load()
    query: Query = build_query(db, args)
    if query:
        result = query.run()
        format = build_output_format(args.output_format)
        output = format.format(result)
        print(output)
    else:
        print("error building the query")


if __name__ == '__main__':
    run_query(build_arguments())
