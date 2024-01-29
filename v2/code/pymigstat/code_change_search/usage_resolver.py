import ast
from ast import *

from utils.utils import update_dict_list, get_all_names, flatten

API = Name | Attribute


def line_range(node: AST):
    return range(node.lineno, node.end_lineno + 1)


class UsageResolver:
    def __init__(self, code: str, path: str = ""):
        self.code = code
        self.path = path
        self._imports: list[GenericImport] = []
        self._api_nodes: list[API] = []
        self._alias_to_importname: dict[str, str] = {}
        self._alias_index: dict[str, list[str]] = {}
        self._name_cache: dict[AST, str] = {}

        root = parse(self.code, self.path)
        self._build_index(root)

    def get_full_name(self, expression: expr):
        assert isinstance(expression, Name | Call | Attribute | Subscript), f"unexpectedly got {type(expression)}"
        if expression not in self._name_cache:
            exp = expression.func if isinstance(expression, Call) else expression
            self._name_cache[expression] = unparse(exp)

        return self._name_cache[expression]

    def get_name_sequence(self, expression: expr):
        name = self.get_full_name(expression)
        return list(reversed(list(get_all_names(name))))

    def find_used_lines(self, import_names: list[str]) -> set[int]:
        used_lines = []
        for import_name in import_names:
            used_lines += self.find_used_lines_for_one_import_name(import_name)
        return set(flatten(used_lines))

    def find_used_lines_for_one_import_name(self, import_name: str):
        imports = [imp for imp in self._imports if imp.resolves(import_name)]
        lines = [line_range(imp.statement) for imp in imports]
        apis = [imp.alias for imp in imports]
        for api in apis:
            lines += self.find_used_lines_for_api(api)
        return lines

    def find_used_lines_for_api(self, api_name: str):
        lines = []
        lines += [line_range(node) for node in self._api_nodes if self.get_full_name(node) == api_name]

        aliases = self.get_aliases(api_name)
        for al in aliases:
            lines += self.find_used_lines_for_api(al)

        return lines

    def _build_index(self, node: AST):
        if isinstance(node, Import | ImportFrom):
            self._index_import(node)
        elif isinstance(node, API):
            self._api_nodes.append(node)
        elif isinstance(node, Assign):
            self._index_assignment(node)

        for child in iter_child_nodes(node):
            self._build_index(child)

    def _index_import(self, node: AST):
        if isinstance(node, Import):
            g_imports = GenericImport.from_import(node)
        elif isinstance(node, ImportFrom):
            g_imports = GenericImport.from_import_from(node)
        else:
            return
        for gi in g_imports:
            parts = gi.import_name.split(".")
            if parts[0] in self._alias_to_importname:
                parts[0] = self._alias_to_importname[parts[0]]
                gi.import_name = ".".join(parts)
            if gi.import_name != gi.alias:
                self._alias_to_importname[gi.alias] = gi.import_name

        self._imports += g_imports

    def _index_assignment(self, node: Assign):
        for target in node.targets:
            if isinstance(target, Tuple | ast.List):
                continue  # TODO: fix this
            qn = self.get_full_name(target)
            variable = self.get_variable(node.value)
            if not variable or qn == variable.id:
                continue
            update_dict_list(self._alias_index, variable.id, [qn])

    def get_variable(self, node: expr):
        if isinstance(node, Name):
            return node
        if isinstance(node, Attribute):
            return self.get_variable(node.value)
        if isinstance(node, Call):
            return self.get_variable(node.func)

    def get_aliases(self, api: str):
        return set(self._alias_index.get(api, []))


class GenericImport:
    """
    There are several ways to import modules in python.
    The ast library provides different representation of each types of import statement.
    This class encapsulates all import types into one generic type to simplify other parts of the code.
    """

    def __init__(self, import_name: str, api_name: str, alias: str, statement: Import | ImportFrom):
        self.import_name = import_name or "."
        self.api_name = api_name
        self.alias = alias or api_name
        self.statement = statement

    @classmethod
    def from_import(cls, statement: Import):
        return [cls(name.name, name.name, name.asname, statement) for name in statement.names]

    @classmethod
    def from_import_from(cls, statement: ImportFrom):
        return [cls(statement.module, name.name, name.asname, statement) for name in statement.names]

    def resolves(self, import_name):
        # the or is for imports like from a.b import c.
        return self.import_name == import_name or self.import_name.startswith(f"{import_name}.")

    def __repr__(self):
        return f"from {self.import_name} import {self.api_name} as {self.alias}"
