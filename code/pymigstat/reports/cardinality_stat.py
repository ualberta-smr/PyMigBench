from complexity import MaxCardinality
from datamodels.loaders import load_migs
from taxonomy import constants

if __name__ == '__main__':
    migs = load_migs()
    mig_cardinality_counts = {cardinality: 0 for cardinality in constants.ALL_CARDINALITIES}
    mig_cardinality_counts["one-to-many or many-to-one"] = 0
    mig_cardinality_counts["zero-to-one or one-to-zero"] = 0
    mig_cardinality_counts[None] = 0
    cc_cardinality_counts = {cardinality: 0 for cardinality in constants.ALL_CARDINALITIES}
    cc_cardinality_counts["N/A"] = 0
    max_card_metric = MaxCardinality()

    for mig in migs:
        mig_cardinality = max_card_metric.calculate(mig)
        mig_cardinality_counts[mig_cardinality] += 1
        for cc in mig.code_changes(True):
            if cc.is_import():
                cc_cardinality_counts["N/A"] += 1
            else:
                cc_cardinality_counts[cc.cardinality] += 1

    print("Migration cardinalities:")
    print(mig_cardinality_counts)
    print("Code change cardinalities:")
    print(cc_cardinality_counts)
