import pandas
from nltk.metrics import masi_distance
from nltk.metrics.agreement import AnnotationTask
from pandas import DataFrame
from sklearn.metrics import cohen_kappa_score


def report_kappa_for_identification(data: DataFrame):
    # r1_identified = [1, 1, 1, 1, 1, 0]
    # r2_identified = [0, 1, 1, 1, 1, 1]

    r1_identified = []
    r2_identified = []
    r1_ids = data["id 1"]
    r2_ids = data["id 2"]
    for i in range(len(data)):
        r1_identified.append(r1_ids[i] != "-")
        r2_identified.append(r2_ids[i] != "-")

    score = cohen_kappa_score(r1_identified, r2_identified)
    print(f"Kappa score for identification: {score:.2}")


def report_kappa(data: DataFrame, property_name: str):
    col1 = f"R1 {property_name}"
    col2 = f"R2 {property_name}"
    score = cohen_kappa_score(data[col1], data[col2])
    print(f"Kappa score for {property_name}: {score:.2}")


def report_alpha(data: DataFrame, property_name: str):
    col1 = f"R1 {property_name}"
    col2 = f"R2 {property_name}"
    # rater1_data = data[col1]
    # rater2_data = data[col2]
    task_data = []
    for i, item in data.iterrows():
        task_data.append(('rater_1', f'item_{i}', frozenset(item[col1].split(';'))))
        task_data.append(('rater_2', f'item_{i}', frozenset(item[col2].split(';'))))

    task = AnnotationTask(distance=masi_distance)

    task.load_array(task_data)
    score = task.alpha()
    print(f"Alpha score for {property_name}: {score:.2}")


def main():
    round = 3
    print(f"ROUND {round} AGREEMENT RATES")
    code_change_data = pandas.read_csv(f"../taxonomy-data/round{round}--merge_processed.csv", keep_default_na=False,
                                       na_values=["@{}]#"])
    print(f"total {len(code_change_data)} items")
    code_change_data = code_change_data[
        (~code_change_data["flag"].isin({"no code changes", "exclude", "not MR", "tangled"}))]
    # report_kappa_for_identification(code_change_data)
    code_change_data = code_change_data[(code_change_data["id 1"] != "-") & (code_change_data["id 2"] != "-")]

    moha = code_change_data[code_change_data["R1"] == "moha"]
    moha_ajay = moha[moha["R2"] == "ajay"]
    moha_sarah = moha[moha["R2"] == "sarah"]
    moha_ildar = moha[moha["R2"] == "ildar"]

    all_mapped = pandas.concat([moha_ajay, moha_sarah, moha_ildar])
    print(f"{len(all_mapped)} items identified by both reviewers")

    print("\noverall agreement")
    report_all_agreements(all_mapped)

    print("\nmoha and ajay")
    report_all_agreements(moha_ajay)

    print("\nmoha and sarah")
    report_all_agreements(moha_sarah)

    print("\nmoha and ildar")
    report_all_agreements(moha_ildar)


def report_all_agreements(data):
    print(f"{len(data)} items")
    report_kappa(data, "source program elements")
    report_kappa(data, "target program elements")
    report_kappa(data, "cardinality")
    report_alpha(data, "properties")
    report_kappa(data, "source APIs")
    report_kappa(data, "target APIs")


if __name__ == '__main__':
    main()
