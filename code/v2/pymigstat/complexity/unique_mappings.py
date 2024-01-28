from complexity.migration_metric import MigrationMetric
from datamodels.migration import Migration


class UniqueMappings(MigrationMetric):

    def __init__(self, exclude_imports):
        self.exclude_imports = exclude_imports

    def _calculate(self, migration: Migration):
        val = len(migration.api_mappings(False))
        return {"total": val}

    @classmethod
    def name(cls):
        return "UniqueMappings"

    @classmethod
    def properties(cls) -> list[str]:
        return ["total"]

    @classmethod
    def key_property(cls) -> str:
        return "total"
