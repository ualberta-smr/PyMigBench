from pymigbench.code_change import CodeChange
from pymigbench.constants import ProgramElement, Cardinality, Property
from pymigbench.line_replacement import LineReplacement
from pymigbench.migration import Migration
from pymigbench.migration_file import MigrationFile
from pymigbench.types import Dynamic


def parse_code_change(data: Dynamic):
    line = LineReplacement.from_expression(data["line"])
    source_pes = [ProgramElement(pe) for pe in data["source_program_elements"]]
    target_pes = [ProgramElement(pe) for pe in data["target_program_elements"]]
    cardinality = Cardinality(data["cardinality"])
    props = [Property(pe) for pe in data["properties"]]
    return CodeChange(line, data["source_apis"], data["target_apis"], source_pes, target_pes, cardinality, props)


def parse_migration_file(data: Dynamic):
    ccs = [parse_code_change(raw_cc) for raw_cc in data["code_changes"]]
    return MigrationFile(data["path"], ccs)


def parse_migration(data: Dynamic):
    files = [parse_migration_file(raw_f) for raw_f in data["files"]]
    mig = Migration(data["repo"], data["commit"], data["source"], data["target"], files, data["domain"])
    for file in mig.files:
        file.mig = mig
    return mig
