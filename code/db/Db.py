import fnmatch
from pathlib import Path

import yaml

from core.Constants import MigrationKey, LibPairKey

DataItem = dict[str, any]


class Db:
    migrations: dict[str, DataItem]
    lib_pairs: dict[str, DataItem]
    _mapping: dict[str, dict[str, DataItem]]

    def __init__(self, data_root: str):
        self.data_root = data_root

    def load(self):
        self.migrations = self.load_items("migration")
        self.lib_pairs = self.load_items("libpair")
        self._mapping = {
            MigrationKey: self.migrations,
            LibPairKey: self.lib_pairs,
        }

    def get_list(self, data_type: str):
        return self._mapping[data_type].values()

    def filter_list(self, data_type: str, filters: dict[str, str]):
        list = self.get_list(data_type)
        for k, v in filters.items():
            list = [item for item in list if self.item_satisfies_filter(item, k, v)]
        return list

    def get_item(self, data_type: str, id: str):
        return self._mapping[data_type][id]

    def load_items(self, data_folder):
        paths = Path(self.data_root, data_folder).glob("*.yaml")
        items = (self.load_item(p) for p in paths)
        dict = {item["id"]: item for item in items}
        return dict

    @staticmethod
    def item_satisfies_filter(item: DataItem, filter_key: str, filter_value: str):
        prop = item[filter_key]
        if isinstance(prop, list):
            if not filter_value and not prop:
                return True  # If the user passes empty string and the list property is empty, consider it matching
            return any(fnmatch.fnmatch(prop_item, filter_value) for prop_item in prop)
        else:
            return fnmatch.fnmatch(prop, filter_value)
        pass

    @staticmethod
    def load_item(yaml_path: Path):
        with open(yaml_path) as f:
            content = f.read()
            dict: DataItem = yaml.safe_load(content)
            return dict
