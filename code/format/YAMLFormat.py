import yaml

from core.to_dict import to_dict
from format.OutputFormat import OutputFormat
from query.Result import Result


class YAMLFormat(OutputFormat):
    def format(self, result: Result):
        return yaml.safe_dump(to_dict(result), sort_keys=False)