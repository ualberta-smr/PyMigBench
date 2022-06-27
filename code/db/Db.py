from typing import Type
from pathlib import Path

import yaml

from db.CodeChange import CodeChange
from db.LibPair import LibPair
from db.Migration import Migration


class Db:
    code_changes: list[CodeChange]
    migrations: list[Migration]
    lib_pairs: list[LibPair]

    def __init__(self, data_root: str):
        self.data_root = data_root

    def load(self):
        self.code_changes = self.load_list("codechange", CodeChange)
        self.migrations = self.load_list("migration", Migration)
        self.lib_pairs = self.load_list("libpair", LibPair)

    def load_list(self, data_folder, data_type):
        paths = Path(self.data_root, data_folder).glob("*.yaml")
        items = [self.load_item(p, data_type) for p in paths]
        return items

    def load_item(self, yaml_path: Path, ctor: Type):
        with open(yaml_path) as f:
            dict = yaml.safe_load(f)
            obj = ctor()
            obj.__dict__.update(dict)
            return obj
