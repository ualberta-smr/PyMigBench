from abc import ABC


class DataItem(ABC):
    id: str
    _raw_content: dict[str]

    def get_raw_content(self):
        return self._raw_content
