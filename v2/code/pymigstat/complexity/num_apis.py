from complexity.migration_metric import MigrationMetric
from datamodels.migration import Migration


class NumAPIs(MigrationMetric):
    """ Total APIs involved in a migration"""

    def __init__(self, exclude_imports):
        self.exclude_imports = exclude_imports

    def _calculate(self, migration: Migration):
        source = 0
        target = 0
        for cc in migration.code_changes(self.exclude_imports):
            source += len(cc.source_apis)
            target += len(cc.target_apis)
        return {"source": source, "target": target, "total": source + target}

    @classmethod
    def name(cls):
        return "NumAPIs"

    @classmethod
    def properties(cls) -> list[str]:
        return ["source", "target", "total"]

    @classmethod
    def key_property(cls) -> str:
        return "total"
