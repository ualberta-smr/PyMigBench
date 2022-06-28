from db.Db import Db
from query.Detail import Detail
from query.Listing import Listing
from query.Summarization import Summarization


def build_query(db: Db, query_name: str, filters: list[str]):
    if not query_name:
        return None
    query_name = query_name.lower()
    if query_name.startswith("l"):
        return Listing(db, filters[0])
    elif query_name.startswith("s"):
        return Summarization(db, filters)
    elif query_name.startswith("d"):
        return Detail(db, filters[0], filters[1])
