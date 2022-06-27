from abc import ABC, abstractmethod


class Query(ABC):

    @abstractmethod
    def run(self):
        pass
