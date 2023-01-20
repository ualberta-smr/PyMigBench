from db.DataItem import DataItem


class Migration(DataItem):
    source: str
    target: str
    repo: str
    commit: str
    pair_id: str
    commit_message: str
    code_changes: list


class CodeChange:
    filepath: str
    lines: list[str]
