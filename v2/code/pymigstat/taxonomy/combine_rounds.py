from pathlib import Path
import pandas as pd

from config import config
from reports.update_report_data import update_report_data

props_in_merge_files = ["id 1", "id 2", "flag", "repo", "commit", "source", "target", "domain", "file path", "lines",
                        "agreed source APIs", "agreed target APIs", "agreed source program elements",
                        "agreed target program elements", "agreed cardinality", "agreed properties"]
props_in_combined_file = ["id 1", "id 2", "flag", "repo", "commit", "source", "target", "domain", "file path", "lines",
                          "source APIs",
                          "target APIs", "source program elements", "target program elements", "cardinality",
                          "properties"]


def join_round0_lines(row):
    s_lines: list[str] = row["source_version_line"].split(",")
    s_lines = [line.replace(":", ",") for line in s_lines]
    t_lines = row["target_version_line"].split(",")
    t_lines = [line.replace(":", ",") for line in t_lines]

    return ";".join(f"{s_lines[i]}:{t_lines[i]}" for i in range(len(s_lines)))


def read_round0_data():
    data = read_round_file_raw(0)
    data["lines"] = data.apply(join_round0_lines, axis=1)
    data = data[
        ["id", "repo", "commit", "source", "target", "domain", "file path", "lines", "source API", "target API",
         "source program elements", "target program elements", "cardinality", "properties"]]
    data.insert(1, "id 2", "--")
    data.insert(2, "flag", "")
    data.columns = props_in_combined_file
    data.insert(0, "round", 0)
    return data


def read_round_file_raw(round: int):
    round_gids = [1441700695, 1357108589, 378878320, 1408273449, 1668404934]
    gsheet_id = config.data_gsheet_id
    round_page = round_gids[round]
    url = f'https://docs.google.com/spreadsheets/d/{gsheet_id}/export?gid={round_page}&format=csv'
    data = pd.read_csv(url, keep_default_na=False, na_values=["@{}]#"])
    return data


def read_round_data(round: int):
    data = read_round_file_raw(round)
    data = data[props_in_merge_files]
    data.columns = props_in_combined_file
    data.insert(0, "round", round)
    return data


def read_round4_data():
    data = read_round_file_raw(4)
    data = data[["id", "flag", "repo", "commit", "source", "target", "domain", "file path", "lines", "source APIs",
                 "target APIs",
                 "source program elements", "target program elements", "cardinality", "properties"]]
    data.insert(1, "id 2", "--")
    data.columns = props_in_combined_file
    data.insert(0, "round", 4)

    return data


def combine_rounds(export_csv=False, filter_out_flagged=True):
    dfs = [read_round0_data(), read_round_data(1), read_round_data(2), read_round_data(3), read_round4_data()]
    combined = pd.concat(dfs)

    combined["migration id"] = combined["source"] + "__" + combined["target"] + "__" + combined["repo"] + "__" + \
                               combined["commit"].str[:7]
    combined["pair id"] = combined["source"] + "__" + combined["target"]

    combined["commit url"] = f"https://github.com/" + combined['repo'] + "/commit/" + combined['commit'].str[:7]

    if export_csv:
        combined.to_csv(config.report_dir / "combined-ccs-raw.csv", index=False)

    salm = combined[combined["round"] > 0]

    update_report_data({
        "SALMLabeledMigCount": len(set(salm["migration id"])),
        "SALMLabeledRepoCount": len(set(salm["repo"])),
        "SALMLabeledLPCount": len(set(salm["pair id"])),
        "SALMLabeledLibCount": len(set(salm["source"]).union(salm["target"])),
        "SALMLabeledDomainCount": len(set(salm["domain"])),
        "TotalLabeledMigCount": len(set(combined["migration id"])),
        "TotalLabeledRepoCount": len(set(combined["repo"])),
        "TotalLabeledLPCount": len(set(combined["pair id"])),
        "TotalLabeledLibCount": len(set(combined["source"]).union(combined["target"])),
        "TotalLabeledDomainCount": len(set(combined["domain"]))
    })

    if filter_out_flagged:
        combined = combined[(combined["lines"].str.len() > 0) | (combined["flag"].str.len() > 0)]

    return combined


if __name__ == '__main__':
    combine_rounds(True)
