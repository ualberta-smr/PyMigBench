from core.Arguments import Arguments
from db.Db import Db
from format.JSONFormat import JSONFormat
from format.YAMLFormat import YAMLFormat
from query.Detail import Detail
from query.Listing import Listing
from query.Count import Count
from query.Summary import Summary


def build_query(db: Db, arguments: Arguments):
    query_name = arguments.query
    if not query_name:
        return None
    query_name = query_name.lower()
    query = None
    if query_name.startswith("l"):
        query = Listing
    elif query_name.startswith("c"):
        query = Count
    elif query_name.startswith("d"):
        query = Detail
    elif query_name.startswith("s"):
        query = Summary

    return query(db, arguments)


def build_output_format(output_format: str):
    output_format = output_format.lower()
    if output_format == "yaml":
        return YAMLFormat()
    if output_format == "json":
        return JSONFormat()
