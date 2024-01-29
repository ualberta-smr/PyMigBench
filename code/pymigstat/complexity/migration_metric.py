from abc import ABC, abstractmethod

from datamodels.migration import Migration


class SimpleMigrationMetric(ABC):
    @abstractmethod
    def calculate(self, migration: Migration) -> dict[str, any]:
        pass

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        pass


class MigrationMetric(SimpleMigrationMetric):
    def calculate(self, migration: Migration) -> dict[str, any]:
        result = self._calculate(migration)
        result.update({"mig": migration.id()})
        return result

    @abstractmethod
    def _calculate(self, migration: Migration) -> dict[str, any]:
        pass

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def properties(cls) -> list[str]:
        pass

    @classmethod
    @abstractmethod
    def key_property(cls) -> str:
        pass
