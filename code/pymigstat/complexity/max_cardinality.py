from typing import Iterator

from complexity.migration_metric import SimpleMigrationMetric
from datamodels.migration import Migration
from taxonomy.constants import *


class MaxCardinality(SimpleMigrationMetric):

    def calculate(self, migration: Migration):
        if migration.is_import_only():
            return None

        cardinalities = [cc.cardinality for cc in migration.code_changes() if not cc.is_import()]
        max_card = max_cardinality(cardinalities)
        return max_card

    @classmethod
    def name(cls) -> str:
        return "MaxCardinality"


_orders = {
    ZERO_TO_ONE: 0,
    ONE_TO_ZERO: 0,
    ONE_TO_ONE: 1,
    ONE_TO_MANY: 2,
    MANY_TO_ONE: 2,
    MANY_TO_MANY: 3
}
_reverse_order = ["zero-to-one or one-to-zero", "one-to-one", "one-to-many or many-to-one", "many-to-many"]


def max_cardinality(cardinalities: Iterator[str]):
    max_order = max(_orders[cardinality] for cardinality in cardinalities)
    return _reverse_order[max_order]
