import csv
from pathlib import Path


def read_csv(path: Path) -> list[list[str]]:
    try:
        with open(path, newline='', encoding="utf8") as f:
            reader = csv.reader(f)
            return list(reader)[1:]  # skip header
    except UnicodeDecodeError:
        with open(path, newline='', encoding="latin-1") as f:
            reader = csv.reader(f)
            return list(reader)[1:]  # skip header


def write_csv(path: Path, rows: list[list[any]], append=False):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    mode = 'a' if append else 'w'
    with open(path, newline='', encoding="utf8", mode=mode) as f:
        writer = csv.writer(f)
        writer.writerows(rows)
