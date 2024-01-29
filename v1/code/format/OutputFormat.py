from abc import ABC, abstractmethod

from query.Result import Result, ResultDisplayOption


class OutputFormat(ABC):
    def format(self, result: Result):
        count = f"{result.count} items"
        if result.display_option == ResultDisplayOption.COUNT_ONLY:
            return count
        if result.display_option == ResultDisplayOption.DATA_ONLY:
            return self.format_impl(result)
        if result.display_option == ResultDisplayOption.COUNT_AND_DATA:
            return f"{count}\n{self.format_impl(result)}\n{count}\n"

    @abstractmethod
    def format_impl(self, result: Result):
        pass
