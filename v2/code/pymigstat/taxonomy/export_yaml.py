import ast
import shutil
import sys

import pandas as pd

from config import config
from taxonomy.combine_rounds import combine_rounds
from utils import Dynamic
from utils.utils import split_strip_sort, commit_url, split_strip
from taxonomy.constants import *

mig_keys = ["repo", "commit", "source", "target", "migration id", "domain"]


def mig_object(mig):
    obj = mig.to_dict()
    del obj["migration id"]
    obj["files"] = []
    obj["commit_url"] = commit_url(obj['repo'], obj['commit'])
    return obj


cc_hash_props = ["source_apis", "target_apis", "source_program_elements", "target_program_elements", "cardinality",
                 "properties"]

cc_props_replacement = {
    "type cast": "output transformation",
    "type transformation": "output transformation",
    "argument addition to decorated function": "parameter addition to decorated function",
    "making async": "async transformation",
    "making await": "async transformation",
    "await deletion": "async transformation"
}

cc_pe_replacement = {
    "function object": "function reference",
    "attribute access": "attribute",
    "class object": "type",
}


def process_one_api(api):
    api = api.strip()
    if api.startswith("import "):
        parsed: ast.Import = ast.parse(api).body[0]
        processed = [name.name for name in parsed.names]
    elif api.startswith("from "):
        parsed: ast.ImportFrom = ast.parse(api).body[0]
        processed = [parsed.module + "." + name.name for name in parsed.names]
    else:
        api = api.split(".")[-1].replace("(", "").replace(")", "")
        processed = [api]
    return processed


def process_apis(apis_string: str):
    apis = split_strip(apis_string)
    all_processed = []
    for api in apis:
        all_processed += process_one_api(api)
    return all_processed


def replace_all(text: str, replacements: dict[str, str]):
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def build_cc_obj(raw_cc: pd.Series) -> Dynamic:
    s_pes: str = replace_all(raw_cc["source program elements"], cc_pe_replacement)
    t_pes: str = replace_all(raw_cc["target program elements"], cc_pe_replacement)
    props: str = replace_all(raw_cc["properties"], cc_props_replacement)

    cardinality = raw_cc["cardinality"]
    if s_pes == "import" or t_pes == "import":
        props = ""
        cardinality = "not applicable"

    if props == "no properties":
        props = ""

    if s_pes == "no program element":
        s_pes = ""
    if t_pes == "no program element":
        t_pes = ""

    return {
        "source_apis": process_apis(raw_cc["source APIs"]),
        "target_apis": process_apis(raw_cc["target APIs"]),
        "source_program_elements": split_strip(s_pes),
        "target_program_elements": split_strip(t_pes),
        "cardinality": cardinality,
        "properties": split_strip_sort(props),
        "lines": raw_cc["lines"]
    }


def cardinality_part(length: int):
    if length == 0:
        return "zero"
    if length == 1:
        return "one"
    return "many"


def validate_line(cc_obj: Dynamic):
    line_str: str = cc_obj["lines"]
    if not line_str:
        raise ValueError("No lines in code changes. " + line_str)
    line_parts = line_str.split(";")
    for part in line_parts:
        part = part.strip()
        card = cc_obj["cardinality"]

        if len(part.split(":")) != 2:
            raise ValueError(f"invalid line spec: {part} for cardinality {card}. " + line_str)

        if card == ONE_TO_ZERO:
            if part[-1] != ":":
                raise ValueError(f"cardinality is {ONE_TO_ZERO} but line does not end with :. " + line_str)
        elif card == ZERO_TO_ONE:
            if part[0] != ":":
                raise ValueError(f"cardinality is {ZERO_TO_ONE} but line does not start with :. " + line_str)


def validate_cc_obj(cc_obj: Dynamic):
    validate_line(cc_obj)

    source_apis = cc_obj["source_apis"]
    target_apis = cc_obj["target_apis"]

    cc_desc = ';'.join(source_apis) + "->" + ';'.join(target_apis) + " : " + cc_obj["lines"]

    source_pes: list[str] = cc_obj["source_program_elements"]
    target_pes: list[str] = cc_obj["target_program_elements"]

    all_pes = set(source_pes + target_pes)
    if not all_pes:
        raise ValueError("no source and target program elements." + cc_desc)

    if not all_pes.issubset(ALL_PES):
        raise ValueError(f"some program elements are misspelled. {all_pes}. {cc_desc}")

    is_import = IMP in all_pes
    assigned_card = cc_obj["cardinality"]
    if not is_import:
        if not assigned_card:
            raise ValueError("no cardinality. " + cc_desc)
        derived_card = cardinality_part(len(source_apis)) + "-to-" + cardinality_part(len(target_apis))
        if derived_card != assigned_card:
            raise ValueError(f"expected {derived_card}, assigned {assigned_card}. {cc_desc}")

        if len(source_apis) != len(source_pes):
            raise ValueError("number of source APIs and source PEs are not same. " + cc_desc)
        if len(target_apis) != len(target_pes):
            raise ValueError("number of target APIs and target PEs are not same. " + cc_desc)

    properties = set(cc_obj["properties"])
    if not properties.issubset(ALL_PROPS):
        raise ValueError(f"some properties are misspelled. {properties}. {cc_desc}")

    if not is_import and "zero" not in assigned_card:
        has_element_name_change = ENC in properties
        if source_apis != target_apis and not has_element_name_change:
            raise ValueError(f"expected {ENC}, but is not assigned. {cc_desc}")
        if source_apis == target_apis and has_element_name_change:
            raise ValueError(f"did not expect {ENC}, but is assigned. {cc_desc}")


def merge_code_changes(ccs: pd.DataFrame):
    hashed_ccs = {}
    ccs = [cc for _, cc in ccs.iterrows()]
    ccs.sort(key=lambda cc: cc["lines"])
    for cc in ccs:
        cc_obj = build_cc_obj(cc)
        validate_cc_obj(cc_obj)

        hash = "$$".join(";".join(cc_obj[p]) for p in cc_hash_props)
        this_lines = split_strip_sort(cc["lines"])
        if hash not in hashed_ccs:
            cc_obj["lines"] = this_lines
            hashed_ccs[hash] = cc_obj
        else:
            old_obj = hashed_ccs[hash]
            old_obj["lines"] += this_lines

    result_ccs = list(hashed_ccs.values())
    return result_ccs


def export_one_migration(mig_id: str, mig: Dynamic, mig_ccs):
    file_paths = set(mig_ccs["file path"])
    for fp in sorted(file_paths):
        file_ccs = mig_ccs[mig_ccs["file path"] == fp]
        try:
            merged_ccs = merge_code_changes(file_ccs)
        except SyntaxError as e:
            print("error in fig " + mig_id)
            raise e

        if not merged_ccs:
            raise ValueError("no code changes")
        file = {
            "path": fp,
            "code_changes": merged_ccs
        }
        mig["files"].append(file)

    content = serialize_migration(mig)
    config.mig_yaml_dir.joinpath(mig_id.replace("/", "@") + ".yaml").write_text(content, "utf8")
    return True


def export_yaml():
    export_migs_yaml()


def export_migs_yaml():
    if config.mig_yaml_dir.exists():
        shutil.rmtree(config.mig_yaml_dir)
        config.mig_yaml_dir.mkdir()
    data = combine_rounds(False, False)
    # data = data[data["flag"].str.len() == 0]
    migrations = {mig["migration id"]: mig_object(mig) for _, mig in data[mig_keys].drop_duplicates().iterrows()}

    flagged_count = 0
    error_count = 0
    exported_count = 0
    for mig_id, mig in migrations.items():
        all_mig_ccs = data[data["migration id"] == mig_id]
        unflagged_ccs = all_mig_ccs[all_mig_ccs["flag"].str.len() == 0]
        if unflagged_ccs.empty:
            flagged_count += 1
            continue
        try:
            export_one_migration(mig_id, mig, unflagged_ccs)
            exported_count += 1
        except ValueError as e:
            error_count += 1
            print("error exporting migration " + mig_id, file=sys.stderr)
            print(e, file=sys.stderr)
            print("", file=sys.stderr)

    total_migs = len(migrations)
    print(f"{total_migs} migrations in total")
    print(f"{flagged_count} flagged")
    print(f"{error_count} error")
    assert exported_count == total_migs - (flagged_count + error_count)
    print(exported_count, "of", total_migs, "exported.")

    files_count = sum(1 for _ in config.mig_yaml_dir.glob("*.yaml"))
    assert files_count == exported_count


def serialize_migration(mig: Dynamic):
    lines = []
    lines += [f"{prop}: {mig[prop]}" for prop in ["repo", "commit", "source", "target", "commit_url", "domain"]]
    lines.append("files:")
    for file in mig["files"]:
        lines.append(f'- path: "{file["path"]}"')
        lines.append(f"  code_changes:")
        for cc in file["code_changes"]:
            lines.append(f"  - lines: {serialize_list(cc['lines'])}")
            lines.append(f"    cardinality: {cc['cardinality']}")
            lines += [f"    {prop}: {serialize_list(cc[prop])}" for prop in
                      ["source_program_elements", "target_program_elements", "properties"]]
            lines += [f"    {prop}: {serialize_list(cc[prop])}" for prop in ["source_apis", "target_apis"]]

    lines += [""]
    as_str = "\n".join(lines)
    return as_str


def serialize_list(items: list):
    items = [item for item in items if item]
    items = [serialize_item(item) for item in items if item]
    return "[" + ", ".join(items) + "]"


special_chars = set("{}[]&*#?|-<>=!%@:`,")
single_quote = "'"
double_quote = '"'


def serialize_item(item: str):
    if item in {"off", "Off"} or not special_chars.isdisjoint(item):
        return f'"{item.replace(double_quote, single_quote)}"'
    return item


if __name__ == '__main__':
    export_yaml()
