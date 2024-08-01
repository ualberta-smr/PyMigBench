from pymigbench.constants import ProgramElement, Cardinality, Property
from pymigbench.line_replacement import LineReplacement
from pymigbench.migration_file import MigrationFile


class CodeChange:
    def __init__(self, line: LineReplacement, source_apis: list[str], target_apis: list[str],
                 source_program_elements: list[ProgramElement], target_program_elements: list[ProgramElement],
                 cardinality: Cardinality, properties: list[Property]):
        self.line = line
        self.source_apis = source_apis
        self.target_apis = target_apis
        self.source_program_elements = source_program_elements
        self.target_program_elements = target_program_elements
        self.cardinality = cardinality
        self.properties = properties
        self.index: int | None = None
        self.file: MigrationFile | None = None

    def is_import(self):
        return ProgramElement.IMP in self.source_program_elements or ProgramElement.IMP in self.target_program_elements

    def is_addition_only(self):
        return not self.target_apis

    def is_removal_only(self):
        return not self.source_apis

    def can_have_properties(self):
        return not (self.is_import() or self.is_addition_only() or self.is_removal_only())

    def id(self):
        return f"{self.file.mig.id()}__{self.file.path}__{self.line}__{self.index}"

    def id_in_file(self):
        return f"{self.line}__{self.index}"

    def __str__(self):
        return f"{self.line} {self.source_apis} -> {self.target_apis}"

    def source_api_str(self):
        return ";".join(self.source_apis)

    def target_api_str(self):
        return ";".join(self.target_apis)

    def __repr__(self):
        return str(self)
