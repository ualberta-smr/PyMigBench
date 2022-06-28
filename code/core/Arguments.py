import argparse
from dataclasses import dataclass


@dataclass
class Arguments:
    query: str
    filters: list[str]

    def __str__(self):
        return str(self.__dict__)


def build_arguments() -> Arguments:
    parser = argparse.ArgumentParser(description="query PyMigBench")
    parser.add_argument("query", nargs='?', default="s",
                        help="One of 'summary' or 'list'. First few letters of the options are also valid.")
    parser.add_argument("-f", "--filters", required=False, nargs='+',
                        help="Filters to the query. Please check query specific documentation")

    dict = vars(parser.parse_args())
    return Arguments(**dict)
