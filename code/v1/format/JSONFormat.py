import json

from format.OutputFormat import OutputFormat
from query.Result import Result


class JSONFormat(OutputFormat):
    def format_impl(self, result: Result):
        return json.dumps(result.items, indent=2, sort_keys=False, default=vars)
