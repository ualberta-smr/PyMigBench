from os import PathLike
from pathlib import Path

import yaml

from config import config
from utils import Dynamic


def load_data(*paths: str | PathLike) -> Dynamic:
    path = Path(*paths)
    data = yaml.safe_load(path.read_text("utf8"))
    return data


def save_data(data: Dynamic, header: str = "", *paths: str | PathLike):
    path = Path(*paths)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = yaml.safe_dump(data, sort_keys=False)
    if header:
        header_lines = header.splitlines(keepends=True)
        header = "# ".join(header_lines)
        header = "# " + header
        content = header + "\n\n" + content

    path.write_text(content, "utf8")


def load_data_list(file_pattern: str):
    """
    Read a list of YAML files
    :param file_pattern: the pattern within the data directory. Specifying the data directory may cause error.
    :return:
    """
    paths = config.data_dir.glob(file_pattern)
    return [load_data(p) for p in paths]
