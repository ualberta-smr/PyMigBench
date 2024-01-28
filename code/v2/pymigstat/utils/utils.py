import itertools
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import TypeVar, Iterator

from utils import Dynamic


def commit_url(repo: str, commit: str):
    repo = filename_to_reponame(repo)
    return f"https://github.com/{repo}/commit/{commit[:8]}"


def reponame_to_filename(repo_name: str):
    filename = repo_name.replace('/', '@')
    if filename[-1] == ".":
        filename = filename[:-1] + "$"

    return filename


def migration_file_name(mig: Dynamic):
    file_name = "__".join([mig['source'], mig['target'], reponame_to_filename(mig['repo']), mig['commit'][:8]])
    file_name += ".yaml"
    return file_name


def filename_to_reponame(filename: str):
    reponame = filename.replace('@', '/')
    if reponame[-1] == "$":
        reponame = reponame[:-1] + "."

    return reponame


def normalize_path(path: str):
    if path is None:
        return None
    return Path(path).as_posix()


def current_time_str():
    return datetime.now(timezone.utc).astimezone().isoformat(sep=" ")


def prompt_repo_name_if_needed():
    if len(sys.argv) < 1:
        val = input("Enter your a repository name. Alternatively, you could pass it as a command line argument: ")
        sys.argv.append(val)


TKey = TypeVar("TKey")
TValue = TypeVar("TValue")


def update_dict_list(dict: dict[TKey, list[TValue]], key: TKey, values: list[TValue]):
    if key not in dict:
        dict[key] = []
    dict[key] += values


def update_dict_list_multi(target: dict[TKey, list[TValue]], source: dict[TKey, list[TValue]]):
    for key, values in source.items():
        update_dict_list(target, key, values)


def get_all_names(full_name: str):
    """for a.b.c.d return (a, a.b, a.b.c and a.b.c.d)"""
    parts = full_name.split(".")
    name = parts[0]
    yield name
    for part in parts[1:]:
        name = name + "." + part
        yield name


class MutableInt:
    def __init__(self, value: int):
        self.value = value

    def increment(self):
        self.value += 1

    def __str__(self):
        return str(self.value)


def flatten(nd_items: Iterator):
    return list(itertools.chain.from_iterable(nd_items))


def flatten_unique_sort(nd_items: Iterator):
    return sorted(set(flatten(nd_items)))


def key_by(items: Iterator[Dynamic], key_prop: str):
    index = {}
    for item in items:
        key = item[key_prop]
        update_dict_list(index, key, [item])

    return index


def split_strip(content: str, sep: str = ";"):
    if content != content:  # check nan
        content = ""
    if not content:
        return []
    parts = [part.strip() for part in content.split(sep)]
    return [part for part in parts if part]


def split_strip_sort(content: str, sep: str = ";"):
    parts = split_strip(content, sep)
    return sorted(parts)


def split_strip_sort_join(content: str, sep: str = ";"):
    return (sep + " ").join(split_strip_sort(content or "", sep))


def sort_join(items, sep=", "):
    return sep.join(sorted(items))
