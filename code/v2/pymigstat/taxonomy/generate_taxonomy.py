import pandas as pd

from taxonomy.combine_rounds import combine_rounds

taxonomy_changes = {
    "class object": "type",
    "type cast": "type transformation",
    "nan": "no properties",
    "full statement replacement": "no properties",
    "module name change": "no properties",
    "object name change": "no properties"
}


def replace_item(item: str):
    return taxonomy_changes.get(item, item)


def generate():
    round0 = pd.read_csv("../taxonomy-data/round0-processed.csv")
    round0 = round0[["source program elements", "target program elements", "cardinality", "properties"]]
    round0["round"] = 0
    combined = pd.read_csv("../taxonomy-data/combined.csv")
    combined = combined[["source program elements", "target program elements", "cardinality", "properties", "round"]]
    combined = pd.concat([round0, combined])
    combined.sort_values("round", ascending=True)
    taxonomy = {}
    for i, row in combined.iterrows():
        props = str(row[3]) if row[3] else "no properties"
        props = [p.strip() for p in props.split(";")]
        for p in props:
            key = (replace_item(row[0]), replace_item(row[1]), row[2], replace_item(p))
            if key not in taxonomy:
                taxonomy[key] = row[4]  # round where introduced

    taxonomy_list = sorted([list(v) + [k] for v, k in taxonomy.items()])
    print(*taxonomy_list, sep="\n")
    print(len(taxonomy_list))


if __name__ == '__main__':
    combine_rounds()
    generate()
