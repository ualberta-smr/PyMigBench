import requests

from config import Config
from csv_helper import read_csv, write_csv


class PyPICache:
    def __init__(self, config: Config):
        self._cache_path = config.data_dir / "pypi_cache.csv"
        if not self._cache_path.exists():
            write_csv(self._cache_path, [["lib", "is in pypi"]])
        rows = read_csv(self._cache_path)
        self.map = {r[0]: r[1] == "True" for r in rows}

    def is_in_pypi(self, lib_name: str):
        if lib_name not in self.map:
            pypi_info = requests.get(f"https://pypi.org/pypi/{lib_name}")
            is_in = pypi_info.status_code == 200
            self.map[lib_name] = is_in
            write_csv(self._cache_path, [[lib_name, is_in]], True)

        return self.map[lib_name]
