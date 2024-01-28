from __future__ import annotations

from dataclasses import dataclass
from os import PathLike

from datamodels.api_mapping import APIMappingSet, APIMapping
from datamodels.storage import load_data
from taxonomy.constants import IMP
from utils import Dynamic
from utils.utils import commit_url, flatten


def deserialize_line_list(ll_str: str):
    ll_str = ll_str.split(" (")[0].strip()
    if not ll_str:
        return []
    parts = ll_str.split(",")
    lines = []
    for part in parts:
        part_parts = part.split("-")
        start, end = int(part_parts[0]), int(part_parts[-1])
        lines += list(range(start, end + 1))

    return lines


def serialize_line_list(lines: list[int], append_count=True):
    if not lines:
        return "(0)" if append_count else ""
    lines = sorted(lines)
    chunks = []
    start, end = lines[0], lines[0]
    for current in lines[1:]:
        if current == end + 1:
            end = current
        else:
            # end last chunk
            chunks.append((start, end))
            start, end = current, current

    chunks.append((start, end))

    def chunk_to_str(chunk):
        if chunk[0] == chunk[1]:
            return str(chunk[0])
        return f"{chunk[0]}-{chunk[1]}"

    to_str = ",".join(chunk_to_str(c) for c in chunks)
    if append_count:
        to_str += f" ({len(lines)})"

    return to_str


@dataclass
class APIUsage:
    api: str
    api_type: str
    line: int


@dataclass
class CodeChangeInMig:
    line: str
    source_apis: list[str]
    target_apis: list[str]
    source_program_elements: list[str]
    target_program_elements: list[str]
    cardinality: str
    properties: list[str]

    def to_dict(self) -> Dynamic:
        d = dict(self.__dict__)
        return d

    def is_import(self):
        return IMP in self.source_program_elements or IMP in self.target_program_elements

    def is_addition_only(self):
        return not self.target_apis

    def is_removal_only(self):
        return not self.source_apis

    def can_have_properties(self):
        return not (self.is_import() or self.is_addition_only() or self.is_removal_only())


@dataclass
class MigrationCodeFile:
    path: str
    code_changes: list[CodeChangeInMig]
    candidate_source_lines: list[int] = None
    candidate_target_lines: list[int] = None

    def to_dict(self) -> Dynamic:
        d = dict(self.__dict__)
        d["code_changes"] = [cc.to_dict() for cc in self.code_changes]
        return d


@dataclass
class Migration:
    def __init__(self, repo: str, commit: str, source: str, target: str, files: list[MigrationCodeFile],
                 commit_url: str, domain: str):
        self.repo = repo
        self.commit = commit
        self.source = source
        self.target = target
        self.files = files
        self.commit_url: str = commit_url
        self.domain = domain
        self.errors: list[str] | None = None
        self._ccs_all: list[CodeChangeInMig] | None = None
        self._ccs_without_import: list[CodeChangeInMig] | None = None
        self.pair_id = "__".join([self.source, self.target])

    def __post_init__(self):
        self.errors = []

    def code_changes(self, include_imports=False) -> list[CodeChangeInMig]:
        if self._ccs_all is None:
            self._ccs_all = flatten(f.code_changes for f in self.files)
        if include_imports:
            return self._ccs_all

        if self._ccs_without_import is None:
            self._ccs_without_import = [cc for cc in self._ccs_all if not cc.is_import()]

        return self._ccs_without_import

    def api_mappings(self, include_imports: bool):
        mappings = APIMappingSet()
        for cc in self.code_changes(include_imports):
            mappings.merge(
                APIMapping(self.source, self.target, cc.source_apis, cc.target_apis, cc.source_program_elements,
                           cc.target_program_elements, cc.cardinality, cc.properties))

        return mappings

    def to_dict(self):
        d = dict(self.__dict__)
        d["commit_url"] = commit_url(self.repo, self.commit)
        d["files"] = [file.to_dict() for file in self.files]
        return d

    def is_import_only(self):
        return all(cc.is_import() for cc in self.code_changes())

    def id(self):
        return "__".join([self.source, self.target, self.repo, self.commit[:8]])


def migration_from_file(path: PathLike | str):
    raw: Dynamic = load_data(path)
    migration = migration_from_raw(raw)
    return migration


def migration_from_raw(data: Dynamic):
    files = [file_from_raw(raw_f) for raw_f in data["files"]]
    data["files"] = files
    return Migration(**data)


def file_from_raw(data: Dynamic):
    code_changes = flatten(code_changes_from_raw(raw_h) for raw_h in data["code_changes"])
    data["code_changes"] = code_changes
    return MigrationCodeFile(**data)


def code_changes_from_raw(data: Dynamic):
    lines = data["lines"]
    del data["lines"]
    for line in lines:
        data["line"] = line
        yield CodeChangeInMig(**data)
