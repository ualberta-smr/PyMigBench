from db.DataItem import DataItem


class CodeChange(DataItem):
    repo: str
    commit: str
    source: str
    target: str
    pair_id: str
    file_path: str
    program_element: str
    cardinality: str
    properties: list[str]
    source_version_line: str
    target_version_line: str
