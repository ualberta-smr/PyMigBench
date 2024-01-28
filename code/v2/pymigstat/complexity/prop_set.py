from complexity.migration_metric import SimpleMigrationMetric
from datamodels.migration import Migration
from taxonomy.constants import short_name
from utils.utils import flatten


class PropSet(SimpleMigrationMetric):
    def calculate(self, migration: Migration):
        all_properties = flatten(cc.properties for cc in migration.code_changes(False))
        all_properties = set(all_properties)
        all_properties = {short_name(prop) for prop in all_properties}
        all_properties = sorted(all_properties)
        return tuple(all_properties)

    @classmethod
    def name(cls) -> str:
        return "PropSet"
