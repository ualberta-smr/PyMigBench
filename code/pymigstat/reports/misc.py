from datamodels.loaders import load_migs


def count_lib_pairs():
    symmetric_set = set()
    non_symmetric_set = set()
    for mig in load_migs():
        symmetric_set.add("__".join(sorted([mig.source, mig.target])))
        non_symmetric_set.add(mig.pair_id)

    print(len(symmetric_set))
    print(len(non_symmetric_set))


if __name__ == '__main__':
    count_lib_pairs()
