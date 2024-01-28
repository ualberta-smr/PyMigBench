import yaml

from format.OutputFormat import OutputFormat
from query.Result import Result


class YAMLFormat(OutputFormat):
    def format_impl(self, result: Result):
        return yaml.safe_dump(result.items, sort_keys=False)
