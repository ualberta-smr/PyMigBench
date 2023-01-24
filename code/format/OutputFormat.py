from abc import ABC, abstractmethod

from query.Result import Result


class OutputFormat(ABC):
    def format(self, result: Result):
        count = f"{result.count} items returned"
        output = f"{count}\n\n{self.format_impl(result)}\n{count}\n"
        return output

    @abstractmethod
    def format_impl(self, result: Result):
        pass
