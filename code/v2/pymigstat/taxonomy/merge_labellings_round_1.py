import pandas as pd
from pandas import DataFrame


def merge_cells(prop: str, r1_row, r2_row):
    r1_cell = r1_row[prop].iloc[0]
    r2_cell = r2_row[prop].iloc[0]
    return [r1_cell, r2_cell, r1_cell if r1_cell == r2_cell else ""]


def merge_labellings(r1_data: DataFrame, r2_data: DataFrame):
    matches = []
    for i, r1_row in r1_data.iterrows():
        r2_row = r2_data.loc[(r2_data["file id"] == r1_row["file id"]) & (r2_data["lines"] == r1_row["lines"])]
        if len(r2_row["id"]) == 1:
            matches.append((r1_row["id"], r2_row["id"].iloc[0]))

    merge_rows = []
    for match in matches:
        r1 = r1_data.loc[r1_data["id"] == match[0]]
        r2 = r2_data.loc[r2_data["id"] == match[1]]
        merge = [
            item.iloc[0] for item in
            [r1["id"], r2["id"], r1["repo"], r1["commit"], r1["source"], r1["target"], r1["file path"], r1["lines"]]
        ]
        merge += merge_cells("source APIs", r1, r2)
        merge += merge_cells("target APIs", r1, r2)
        merge += merge_cells("program element", r1, r2)
        merge += merge_cells("cardinality", r1, r2)
        merge += merge_cells("properties", r1, r2)
        merge_rows.append(merge)

    remaining_r1_data = r1_data[~r1_data["id"].isin({m[0] for m in matches})]
    remaining_r2_data = r2_data[~r2_data["id"].isin({m[1] for m in matches})]

    merge_rows += remaining_r1_data.apply(
        lambda rr1: [rr1["id"], "", rr1["repo"], rr1["commit"], rr1["source"], rr1["target"], rr1["file path"],
                     rr1["lines"],
                     rr1["source APIs"], "", "",
                     rr1["target APIs"], "", "",
                     rr1["program element"], "", "",
                     rr1["cardinality"], "", "",
                     rr1["properties"], "", ""], axis=1).tolist()

    merge_rows += remaining_r2_data.apply(
        lambda rr2: ["", rr2["id"], rr2["repo"], rr2["commit"], rr2["source"], rr2["target"], rr2["file path"],
                     rr2["lines"],
                     "", rr2["source APIs"], "",
                     "", rr2["target APIs"], "",
                     "", rr2["program element"], "",
                     "", rr2["cardinality"], "",
                     "", rr2["properties"], ""], axis=1).tolist()

    merge_data = pd.DataFrame(
        columns=["id 1", "id 2", "repo", "commit", "source", "target", "file path", "lines",
                 "R1 source APIs", "R2 source APIs", "agreed source API",
                 "R1 target APIs", "R2 target APIs", "agreed target APIs",
                 "R1 program element", "R2 program element", "agreed program element",
                 "R1 cardinality", "R2 cardinality", "agreed cardinality",
                 "R1 properties", "R2 properties", "agreed properties"],
        data=merge_rows, dtype=str)

    merge_data.to_csv("../taxonomy-data/round1--merge.csv", index=False, na_rep="")


def format_lines(lines: str):
    return str(lines or "").replace(" ", "")


def format_multi_value_cell(content: str):
    translation_table = str.maketrans("", "", "()@")  # for APIs
    parts = str(content or "").translate(translation_table).split(";")
    return ";".join([part.strip() for part in sorted(parts)])


def read_labelling(file_path: str):
    data = pd.read_csv(file_path, keep_default_na=False, na_values=["@{}]#"])
    data["lines"] = data["lines"].map(format_lines)
    for col in ["source APIs", "target APIs", "program element", "properties"]:
        data[col] = data[col].map(format_multi_value_cell)

    return data


def main():
    reviewer1 = read_labelling("../taxonomy-data/round1-moha.csv")
    reviewer2_1 = read_labelling("../taxonomy-data/round1-ajay.csv")
    reviewer2_2 = read_labelling("../taxonomy-data/round1-sarah.csv")
    reviewer2_3 = read_labelling("../taxonomy-data/round1-ildar.csv")
    reviewer2 = pd.concat([reviewer2_1, reviewer2_2, reviewer2_3])
    merge_labellings(reviewer1, reviewer2)


if __name__ == '__main__':
    main()
