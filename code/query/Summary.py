from core.Constants import DataTypeKeys, DataTypeName
from query.Query import Query
from query.Result import Result, ResultDisplayOption


class Summary(Query):
    def run(self):
        result = {}
        for dt in DataTypeKeys:
            result[DataTypeName[dt]] = len(self.db.get_list(dt))

        return Result([result], ResultDisplayOption.DATA_ONLY)
