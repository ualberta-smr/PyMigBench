from db.DataItem import DataItem


class LibPair(DataItem):
    source: str
    target: str
    domain: str
