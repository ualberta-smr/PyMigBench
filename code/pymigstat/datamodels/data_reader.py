from pathlib import Path

from config import config
from csv_helper import read_csv


def read_csv_in_tuple_set(path: Path):
    raw_csv = read_csv(path)
    tuples = {tuple(p.strip().lower() for p in r) for r in raw_csv if r[0]}
    return tuples


def read_unfiltered_migbench_migs():
    return read_csv_in_tuple_set(config.data_dir / "migbench_migs.csv")


def read_unfiltered_salm_migs():
    return read_csv_in_tuple_set(config.data_dir / "salm_migs.csv")


def read_analogous_lib_results():
    return read_csv(config.data_dir / "gpt4_analogous.csv")
