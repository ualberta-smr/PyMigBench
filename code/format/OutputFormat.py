from abc import ABC, abstractmethod

from query.Result import Result


class OutputFormat(ABC):
    @abstractmethod
    def format(self, result: Result):
        pass
