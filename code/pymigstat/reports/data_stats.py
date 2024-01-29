import pandas as pd

from config import config
from taxonomy.combine_rounds import combine_rounds


def round_row(round_data, round_name, data_source):
    migs = round_data["migration id"].nunique()
    lps = round_data["pair id"].nunique()
    libs = len(set(round_data["source"].tolist() + round_data["target"].tolist()))
    repos = round_data["repo"].nunique()
    commits = round_data["commit url"].nunique()

    return [round_name, data_source, migs, lps, libs, repos, commits]


def append_percent(data_row, total_row):
    for i in range(2, 7):
        data_row[i] = f"{data_row[i]} ({(data_row[i]/total_row[i]):.0%})"


def data_stats():
    migbench_total_row = ["Full data", "\\migbench", 75, 34, 55, 57, 74]
    salm_total_row = ["Full data", "\\salm", 2335, 231, 288, 1876, 2462]
    all_total_row = ["Full data", "all", 2405, 256, 319, 1923, 2231]

    df = combine_rounds(False)
    grid = []
    for round in range(0, 5):
        ds = "\\migbench" if round == 0 else "\\salm"
        round_data = df[df["round"] == round]
        grid.append(round_row(round_data, round, ds))

    migbench_labeled = list(grid[0])
    migbench_labeled[0] = "Labeled data"
    append_percent(migbench_labeled, migbench_total_row)
    grid.append(migbench_labeled)

    salm_data = df[df["round"] > 0]
    salm_labeled = round_row(salm_data, "Labeled data", "\\salm")
    append_percent(salm_labeled, salm_total_row)
    grid.append(salm_labeled)

    all_labeled = round_row(df, "Labeled data", "all")
    grid.append(all_labeled)
    append_percent(all_labeled, all_total_row)

    grid += [
        migbench_total_row, salm_total_row, all_total_row
    ]

    result_df = pd.DataFrame(
        data=grid,
        columns=["Round", "Dataset", "# Migs", "# LPs", "# Libs", "# Repos", "# Commits"]
    )
    result_df.to_csv(config.report_dir / "data-stats.csv", index=False)
    print(result_df)


if __name__ == '__main__':
    data_stats()
