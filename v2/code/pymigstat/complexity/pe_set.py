from complexity.migration_metric import MigrationMetric, SimpleMigrationMetric
from datamodels.migration import Migration
from taxonomy.constants import short_name
from utils.utils import flatten


class PESet(SimpleMigrationMetric):
    def calculate(self, migration: Migration):
        all_pe = [cc.source_program_elements for cc in migration.code_changes(False)]
        all_pe += [cc.target_program_elements for cc in migration.code_changes(False)]
        all_pe = set(flatten(all_pe))
        if "no program element" in all_pe:
            all_pe.remove("no program element")

        all_pe = {short_name(pe) for pe in all_pe}
        return tuple(sorted(all_pe))

    @classmethod
    def name(cls) -> str:
        return "PESet"
