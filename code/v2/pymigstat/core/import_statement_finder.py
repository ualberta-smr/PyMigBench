import ast
from os import PathLike
from pathlib import Path

from tools import ExternalTool
from utils import Dynamic
from utils.utils import get_all_names


def import_info(import_name: str, object_name: str | None, line: int, statement: str):
    # for `from xyz import a,b,c`, there will be three imports: xyz.a, xyz.b, xyz.c.
    #   the first part is import_name, the second part is object_name
    #   import_name is same for all imports in such a statements
    #   the id should be import_name.object_name@from_line
    # for `import p, q, r, there will be three imports: p, q and r
    #   there is no object_name in this case
    #   the id should be import_name@from_line
    # id should match with the id that is returned when finding unused imports

    import_name = import_name.strip()
    if object_name:
        object_name = object_name.strip()
        id = f"{import_name}.{object_name}@{line}"
    else:
        id = f"{import_name}@{line}"

    return {
        "id": id,
        "import_name": import_name,
        "object_name": object_name,
        "line": line,
        "statement": statement,
        "all_possible_import_names": set(get_all_names(import_name)),
    }


def parse_unused_import_line(line: str) -> str:
    parts = line.split(':')
    line = int(parts[1])
    name_start = parts[3].find("'")
    name_end = parts[3].find("'", name_start + 1)
    name = parts[3][name_start + 1:name_end - 1]

    return f"{name}@{line}"


class ImportStatementFinder:
    def __init__(self, repo_path: Path, file_path_in_repo: PathLike):
        self.repo_path = repo_path
        self.file_path_in_repo = file_path_in_repo

    def find_all_imports(self) -> list[Dynamic]:
        filepath = (self.repo_path / self.file_path_in_repo)
        if not filepath.exists():
            raise FileNotFoundError(f"The file {self.file_path_in_repo} was not found")

        code = filepath.read_text("utf8")
        root = ast.parse(code, filename=str(self.file_path_in_repo))

        imports = []
        for node in ast.walk(root):
            if isinstance(node, ast.Import):
                statement = ast.get_source_segment(code, node, padded=True)
                imports += [import_info(import_name.name, None, node.lineno, statement) for import_name in node.names]
            elif isinstance(node, ast.ImportFrom):
                statement = ast.get_source_segment(code, node, padded=True)
                imports += [import_info(node.module or ".", object_name.name, node.lineno, statement) for object_name in
                            node.names]

        return imports

    def find_unused_import(self):
        flake8 = ExternalTool("flake8")
        results = flake8.run("--filename", str(self.file_path_in_repo), "--select", "F401").splitlines(keepends=False)
        return [parse_unused_import_line(line) for line in results]
