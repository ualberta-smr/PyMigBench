import json

from format.OutputFormat import OutputFormat
from query.Result import Result


class JSONFormat(OutputFormat):
    def format(self, result: Result):
        return json.dumps(result, indent=2, sort_keys=False, default=vars)
