from core.Constants import DataTypeKeys, DataTypeName
from query.Query import Query
from query.Result import Result


class Count(Query):
    def run(self):
        data_types = self.arguments.data_types

        if not data_types or "all" in data_types:
            data_types = DataTypeKeys

        result = {}
        for dt in data_types:
            result[DataTypeName[dt]] = len(self.db.get_list(dt))

        return Result([result])
