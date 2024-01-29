import pandas as pd

from complexity.max_cardinality import max_cardinality
from reports.lib_pair_data import LibPairDataSet
from taxonomy.constants import *


class LibPairStats:
    def pe_individual(self):
        data = {pe: 0 for pe in NON_IMPORT_PES}
        only_function_count = 0
        lp_set = LibPairDataSet().load()
        for lp in lp_set:
            elements = lp.all_program_elements() - {IMP}
            for pe in elements:
                data[pe] += 1
            if elements == {F_CALL}:
                only_function_count += 1

        df = pd.DataFrame(data.items(), columns=["pe", "count"])
        df = df.set_index(["pe"])
        total_lib_pairs = len(lp_set)

        df["percent"] = df["count"] / total_lib_pairs

        print(df.to_csv())
        print("only function", only_function_count / total_lib_pairs)
        print()
        print()
        return self

    def prop_individual(self):
        has_prop = {prop: 0 for prop in ALL_PROPS_WITH_NO_PROPS}
        lp_set = LibPairDataSet().load()
        func_imp_with_no_prop_or_name_change = 0
        for lp in lp_set:
            for prop in lp.properties():
                has_prop[prop] += 1
            if lp.all_program_elements().issubset([F_CALL, IMP]) and lp.properties().issubset([NO_PROP, ENC]):
                func_imp_with_no_prop_or_name_change += 1

        df = pd.DataFrame(has_prop.items(), columns=["prop", "count"])
        df = df.set_index(["prop"])
        total_lib_pairs = len(lp_set)
        df["percent"] = df["count"] / total_lib_pairs

        print(df.to_csv())
        print("function or import with no prop or enc", func_imp_with_no_prop_or_name_change / total_lib_pairs)
        return self

    def max_cardinality(self):
        max_card_counts = {
            "zero-to-one or one-to-zero": 0,
            "one-to-one": 0,
            "one-to-many or many-to-one": 0,
            "many-to-many": 0
        }
        lp_set = LibPairDataSet().load()
        for lp in lp_set:
            if lp.is_import_only():
                continue
            mc = max_cardinality(lp.cardinalities())
            if mc != Not_Applicable:
                max_card_counts[mc] += 1

        df = pd.DataFrame(max_card_counts.items(), columns=["max cardinality", "count"])
        df = df.set_index(["max cardinality"])
        print(df.to_csv())

        return self


if __name__ == '__main__':
    LibPairStats().pe_individual().prop_individual().max_cardinality()
