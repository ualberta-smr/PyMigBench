from complexity.migration_metric import MigrationMetric
from datamodels.migration import Migration


class UniqueAPIs(MigrationMetric):
    def __init__(self, exclude_imports):
        self.exclude_imports = exclude_imports

    """unique APIs"""

    def _calculate(self, migration: Migration) -> any:
        source_apis = set()
        target_apis = set()
        for cc in migration.code_changes(self.exclude_imports):
            source_apis.update(cc.source_apis)
            target_apis.update(cc.target_apis)

        source_count = len(source_apis)
        target_count = len(target_apis)
        return {"source": source_count, "target": target_count, "total": source_count + target_count}

    @classmethod
    def name(cls) -> str:
        return "UniqueAPIs"

    @classmethod
    def properties(cls) -> list[str]:
        return ["source", "target", "total"]

    @classmethod
    def key_property(cls) -> str:
        return "total"
