from abc import ABC
from typing import Any, Iterable


class DataModel(ABC):
    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, dict: dict[str, Any]):
        return cls(**dict)

    @classmethod
    def to_raw_list(cls, model_list: Iterable['DataModel']):
        return [item.to_dict() for item in model_list]

    @classmethod
    def to_model_list(cls, raw_list: Iterable[dict[str, Any]]):
        return [cls.from_dict(dict) for dict in raw_list]
