from db.Db import Db
from query.Listing import Listing
from query.Summarization import Summarization


def build_query(db: Db, query_name: str, args):
    if not query_name:
        return None
    query_name = query_name.lower()
    if query_name.startswith("l"):
        return Listing(db, args[0])
    elif query_name.startswith("s"):
        return Summarization(db, args)
