from pathlib import Path

import pandas as pd
from pandas import DataFrame


def merge_cells(prop: str, r1_row, r2_row):
    r1_cell = r1_row[prop].iloc[0]
    r2_cell = r2_row[prop].iloc[0]
    return [r1_cell, r2_cell, r1_cell if r1_cell == r2_cell else ""]


def data_with_ids(df: DataFrame):
    # filter out data without ID. meaning they are not labeled yet. necessary for partial merging.
    return df.loc[df["id"] != ""]


def data_without_flag(df: DataFrame):
    return df.loc[df["flag"] == ""]


def get_string_from_cell(cell):
    return cell.iloc[0]


def merge_labellings(r1_data: DataFrame, r2_data: DataFrame):
    r1_data = data_with_ids(r1_data)
    r2_data = data_with_ids(r2_data)

    matches = find_matching_rows(r1_data, r2_data)

    merge_rows = []
    for match in matches:
        r1 = r1_data.loc[r1_data["id"] == match[0]]
        r2 = r2_data.loc[r2_data["id"] == match[1]]
        merge = [
            get_string_from_cell(item) for item in
            [r1["id"], r2["id"], r1["repo"], r1["commit"], r1["source"], r1["target"], r1["file path"], r1["lines"]]
        ]
        merge += [""]  # the flag column flag
        merge += merge_cells("source APIs", r1, r2)
        merge += merge_cells("target APIs", r1, r2)
        merge += merge_cells("source program elements", r1, r2)
        merge += merge_cells("target program elements", r1, r2)
        merge += merge_cells("cardinality", r1, r2)
        merge += merge_cells("properties", r1, r2)
        merge += [get_string_from_cell(r1["comments"]), get_string_from_cell(r2["comments"])]
        merge += [get_string_from_cell(r1["reviewer"]), get_string_from_cell(r2["reviewer"])]
        merge_rows.append(merge)

    remaining_r1_data = r1_data[~r1_data["id"].isin({m[0] for m in matches})]
    remaining_r2_data = r2_data[~r2_data["id"].isin({m[1] for m in matches})]

    merge_rows += remaining_r1_data.apply(
        lambda rr1: [rr1["id"], "-", rr1["repo"], rr1["commit"], rr1["source"], rr1["target"], rr1["file path"],
                     rr1["lines"], rr1["flag"],

                     rr1["source APIs"], "", "",
                     rr1["target APIs"], "", "",
                     rr1["source program elements"], "", "",
                     rr1["target program elements"], "", "",
                     rr1["cardinality"], "", "",
                     rr1["properties"], "", "",
                     rr1["comments"], "",
                     rr1["reviewer"], ""], axis=1).tolist()

    merge_rows += remaining_r2_data.apply(
        lambda rr2: ["-", rr2["id"], rr2["repo"], rr2["commit"], rr2["source"], rr2["target"], rr2["file path"],
                     rr2["lines"], rr2["flag"],
                     "", rr2["source APIs"], "",
                     "", rr2["target APIs"], "",
                     "", rr2["source program elements"], "",
                     "", rr2["target program elements"], "",
                     "", rr2["cardinality"], "",
                     "", rr2["properties"], "",
                     "", rr2["comments"],
                     "", rr2["reviewer"]], axis=1).tolist()

    merge_data = pd.DataFrame(
        columns=["id 1", "id 2", "repo", "commit", "source", "target", "file path", "lines", "flag",
                 "R1 source APIs", "R2 source APIs", "agreed source API",
                 "R1 target APIs", "R2 target APIs", "agreed target APIs",
                 "R1 source program elements", "R2 source program elements", "agreed source program elements",
                 "R1 target program elements", "R2 target program elements", "agreed target program elements",
                 "R1 cardinality", "R2 cardinality", "agreed cardinality",
                 "R1 properties", "R2 properties", "agreed properties",
                 "R1 comments", "R2 comments", "R1", "R2"],
        data=merge_rows, dtype=str)

    return merge_data


def find_matching_rows(r1_data: DataFrame, r2_data: DataFrame):
    r1_data = data_without_flag(r1_data)
    r2_data = data_without_flag(r2_data)
    matches = []
    for i, r1_row in r1_data.iterrows():
        r2_row = r2_data.loc[(r2_data["file id"] == r1_row["file id"]) & (r2_data["lines"] == r1_row["lines"])]
        if len(r2_row["id"]) == 1:
            matches.append((r1_row["id"], r2_row["id"].iloc[0]))
    return matches


def format_lines(lines: str):
    return str(lines or "").replace(" ", "")


def format_multi_value_cell(content: str):
    translation_table = str.maketrans("", "", "()@")  # for APIs
    parts = str(content or "").translate(translation_table).split(";")
    parts = [part.strip() for part in parts]
    return ";".join(sorted(parts))


def read_labelling(file_path: str):
    file_path = Path(file_path)
    data = pd.read_csv(file_path, keep_default_na=False, na_values=["@{}]#"])
    data["lines"] = data["lines"].map(format_lines)
    for col in ["source APIs", "target APIs", "source program elements", "target program elements", "properties"]:
        data[col] = data[col].map(format_multi_value_cell)
    reviewer = file_path.name.split(".")[0].split("-")[1]  # get the reviewer name from file path
    data["reviewer"] = reviewer
    return data


def main():
    round = 3
    reviewer1 = read_labelling(f"../taxonomy-data/round{round}-moha.csv")
    reviewer2 = pd.concat([
        read_labelling(f"../taxonomy-data/round{round}-ajay.csv"),
        read_labelling(f"../taxonomy-data/round{round}-sarah.csv"),
        read_labelling(f"../taxonomy-data/round{round}-ildar.csv")
    ])
    merge_data = merge_labellings(reviewer1, reviewer2)
    merge_data.to_csv(f"../taxonomy-data/round{round}--merge.csv", index=False, na_rep="")


if __name__ == '__main__':
    main()
