from complexity.migration_metric import MigrationMetric
from datamodels.migration import Migration
from utils.utils import flatten


def count_total_lines(line_expression: str):
    if not line_expression:
        return 0

    total = 0
    parts = line_expression.split(",")  # 1,5-6 -> [1, 5-6]
    for part in parts:
        if "-" in part:
            start, end = part.split("-")
            total += int(end) - int(start) + 1
        else:
            total += 1

    return total


class MigLOC(MigrationMetric):
    def __init__(self, exclude_imports):
        self.exclude_imports = exclude_imports

    def _calculate(self, migration: Migration):
        lines: list[str] = [cc.line for cc in migration.code_changes(self.exclude_imports)]
        removed = 0
        added = 0
        for line_replacement_expression in lines:
            src_line_exp, tgt_line_exp = line_replacement_expression.split(":")
            removed += count_total_lines(src_line_exp)
            added += count_total_lines(tgt_line_exp)

        return {"source": removed, "target": added, "total": removed + added}

    @classmethod
    def name(cls):
        return "MigLOC"

    @classmethod
    def properties(cls) -> list[str]:
        return ["source", "target", "total"]

    @classmethod
    def key_property(cls) -> str:
        return "total"
