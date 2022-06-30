from abc import ABC


class DataItem(ABC):
    id: str

    def __getitem__(self, property: str):
        return getattr(self, property)
