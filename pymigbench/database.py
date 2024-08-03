from pathlib import Path

import yaml

from pymigbench.migration import Migration
from pymigbench.migration_file import MigrationFile
from pymigbench.parsers import parse_migration
from pymigbench.types import Dynamic


class Database:
    """
    A readonly database to access migration related data.
    """

    def __init__(self, migs: list[Migration]):
        self._migs = migs
        self._files = [file for mig in migs for file in mig.files]
        self._ccs = [cc for mig in migs for cc in mig.code_changes()]
        self._mig_index = {mig.id(): mig for mig in migs}
        self._file_index = {file.id(): file for file in self._files}
        self._cc_index = {cc.id(): cc for cc in self._ccs}

    def migs(self) -> list[Migration]:
        return self._migs

    def files(self) -> list[MigrationFile]:
        return self._files

    def code_changes(self):
        return self._ccs

    def mig(self, id: str) -> Migration:
        if id in self._mig_index:
            raise ValueError(f"migration {id} not found")
        return self._mig_index[id]

    def file(self, id: str):
        if id in self._file_index:
            raise ValueError(f"file {id} not found")
        return self._file_index[id]

    def code_change(self, id: str):
        if id in self._cc_index:
            raise ValueError(f"code change {id} not found")
        return self._cc_index[id]

    @staticmethod
    def load_from_dir(mig_dir: Path):
        def mig_from_file(path: Path):
            raw: Dynamic = yaml.unsafe_load(path.read_text("utf8"))
            migration = parse_migration(raw)
            return migration

        mig_files = mig_dir.glob("*.yaml")
        migs = [mig_from_file(mf) for mf in mig_files]
        return Database(migs)
