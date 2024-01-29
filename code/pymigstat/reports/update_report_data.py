from pathlib import Path

import yaml

from config import config
from latex.utils import to_macro_name


def _build_def_macro(key: str, value: any):
    return "\\def" + key + "{" + str(value) + "\\xspace}"


_yaml_data_path = (config.paper_dir / "results-data.yaml").resolve().absolute()
_tex_data_path = (config.paper_dir / "results-data.tex").resolve().absolute()


def update_report_data(new_data: dict[str, any]):
    new_data = {to_macro_name(k): v for k, v in new_data.items()}
    all_data = {}
    if _yaml_data_path.exists():
        all_data: dict = yaml.safe_load(_yaml_data_path.read_text("utf8"))

    all_data = all_data or {}
    all_data.update(new_data)
    print("writing to " + str(_yaml_data_path))
    _yaml_data_path.write_text(yaml.safe_dump(all_data, sort_keys=False), "utf8")

    all_defs = "\n".join(_build_def_macro(key, value) for key, value in all_data.items())
    print("writing to " + str(_tex_data_path))
    _tex_data_path.write_text(all_defs, encoding="utf8")


def clean_report_data():
    _yaml_data_path.unlink(True)
    _tex_data_path.unlink(True)


def percent(numerator, denominator, escape_latex=True):
    p = 100 * numerator / denominator
    return format_percent(p, escape_latex)


def format_percent(value, escape_latex=True):
    decimals = 1 if value < 1 else 0
    percent_sign = "\\%" if escape_latex else "%"
    return ("{0:." + str(decimals) + "f}").format(value) + percent_sign
