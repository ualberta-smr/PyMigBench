from query.Query import Query
from query.Result import Result, ResultDisplayOption


class Count(Query):
    def run(self):
        if self.arguments.data_type is None:
            raise ValueError("Please provide a datatype for count.")

        result = self.apply_filter()

        return Result(result, ResultDisplayOption.COUNT_ONLY)
