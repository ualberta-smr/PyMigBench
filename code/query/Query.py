from abc import ABC, abstractmethod

from db.DataItem import DataItem


class Query(ABC):
    @abstractmethod
    def run(self):
        pass


class ListQuery(Query):
    def run(self):
        items = self.apply_filter()
        print(f" {len(items)} results found:")
        for i, item in enumerate(items, start=1):
            item_string = self.item_to_string(item, i)
            print(item_string)

        print(f" {len(items)} results found:")

    @abstractmethod
    def apply_filter(self) -> list[DataItem]:
        pass

    @abstractmethod
    def item_to_string(self, item: DataItem, index: int) -> str:
        pass
