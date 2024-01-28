from complexity.migration_metric import MigrationMetric
from datamodels.migration import Migration


class MFileMigrationComplexity(MigrationMetric):
    """ Files count migration complexity """

    def _calculate(self, migration: Migration):
        return len(migration.files)

    @classmethod
    def name(cls):
        return "MFile"
