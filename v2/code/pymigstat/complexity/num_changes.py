from complexity.migration_metric import MigrationMetric
from datamodels.migration import Migration


class NumChanges(MigrationMetric):
    """total code changes in a migrations"""

    def __init__(self, exclude_imports):
        self.exclude_imports = exclude_imports

    def _calculate(self, migration: Migration):
        val = len(migration.code_changes(self.exclude_imports))
        return {"total": val}

    @classmethod
    def name(cls) -> str:
        return "NumChanges"

    @classmethod
    def properties(cls) -> list[str]:
        return ["total"]

    @classmethod
    def key_property(cls) -> str:
        return "total"
