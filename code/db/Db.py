import fnmatch
from typing import Type
from pathlib import Path

import yaml

from core.Constants import CodeChangeKey, MigrationKey, LibPairKey
from db.CodeChange import CodeChange
from db.DataItem import DataItem
from db.LibPair import LibPair
from db.Migration import Migration


class Db:
    code_changes: dict[str, CodeChange]
    migrations: dict[str, Migration]
    lib_pairs: dict[str, LibPair]
    _mapping: dict[str, dict[str, DataItem]]

    def __init__(self, data_root: str):
        self.data_root = data_root

    def load(self):
        self.code_changes = self.load_items("codechange", CodeChange)
        self.migrations = self.load_items("migration", Migration)
        self.lib_pairs = self.load_items("libpair", LibPair)
        self._mapping = {
            CodeChangeKey: self.code_changes,
            MigrationKey: self.migrations,
            LibPairKey: self.lib_pairs,
        }

    def get_list(self, data_type: str):
        return self._mapping[data_type].values()

    def filter_list(self, data_type: str, filters: dict[str, str]):
        list = self.get_list(data_type)
        for k, v in filters.items():
            list = [item for item in list if fnmatch.fnmatch(getattr(item, k), v)]
        return list

    def get_item(self, data_type: str, id: str):
        return self._mapping[data_type][id]

    def load_items(self, data_folder, data_type):
        paths = Path(self.data_root, data_folder).glob("*.yaml")
        items = (self.load_item(p, data_type) for p in paths)
        dict = {item.id: item for item in items}
        return dict

    def load_item(self, yaml_path: Path, ctor: Type[DataItem]):
        with open(yaml_path) as f:
            content = f.read()
            obj = ctor()
            obj._raw_content = content
            dict = yaml.safe_load(content)
            obj.__dict__.update(dict)
            return obj
