import pandas as pd

from datamodels.loaders import load_migs
from datamodels.migration import *

# groups:
# fc -> fc, no prop
# fc -> fc,
from latex.utils import *
from reports.update_report_data import *
from taxonomy.constants import *
from utils.utils import sort_join


class HasId:
    id: str

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.id > other.id

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return self.id


def cc_comb_id(s_pes, t_pes, props):
    return ", ".join(sorted(s_pes or {NO_PE})) + " -> " + ", ".join(sorted(t_pes or {NO_PE})) + " | " + ", ".join(
        sorted(props or {NO_PROP}))


def group_properties(properties):
    grouped_properties = set()
    for prop in properties:
        if prop.startswith("argument"):
            grouped_properties.add("input transformation")
        else:
            grouped_properties.add(prop)
    props = {short_name(p) for p in grouped_properties}
    return props


def generic_pe(pe):
    return pe


class CCCombination(HasId):

    def __init__(self, cc: CodeChangeInMig):
        self.source_pes = set(cc.source_program_elements)
        self.target_pes = set(cc.target_program_elements)

        self.all_pes = self.source_pes.union(self.target_pes)
        props = set(cc.properties)
        self.props = props
        self.short_props = {short_name(p) for p in props}
        # self.props = group_properties(self.props)

        self.id = cc_comb_id(self.source_pes, self.target_pes, self.short_props)

    def has_function_call(self):
        return F_CALL in self.source_pes

    def only_function_call(self):
        return self.all_pes == {F_CALL}

    def no_function_calls(self):
        return F_CALL not in self.all_pes

    def is_addition(self):
        return not len(self.source_pes)

    def is_removal(self):
        return not len(self.target_pes)

    def category(self):
        if self.is_addition():
            return "addition"
        if self.is_removal():
            return "removal"

        group_props = group_properties(self.props)
        s_pes = {generic_pe(pe) for pe in self.source_pes}
        t_pes = {generic_pe(pe) for pe in self.target_pes}

        return cc_comb_id(s_pes, t_pes, group_props)


def merge_in_supersets(cc_combos: set[CCCombination]):
    to_remove = []
    for super in cc_combos:
        for sub in cc_combos:
            if super == sub:
                continue
            if super.source_pes == sub.source_pes and \
                    super.target_pes == sub.target_pes and super.props.issuperset(sub.props):
                to_remove.append(sub)

    return cc_combos.difference(to_remove)


class MigCombination(HasId):
    def __init__(self, mig: Migration):
        processes = []
        ccs = mig.code_changes(False)
        cc_combos = {CCCombination(cc) for cc in ccs}

        for process in processes:
            cc_combos = process(cc_combos)

        self.cc_combos: set[CCCombination] = cc_combos
        self.id = "\n".join(cc_combo.id for cc_combo in sorted(self.cc_combos))

    def category(self):
        other = "other"
        if len(self.cc_combos) > 1:
            return "\n".join(sorted({ccc.category() for ccc in self.cc_combos}))
            # if all(ccc.no_function_calls() for ccc in self.cc_combos):
            #     return "no " + F_CALL
            # if all(ccc.only_function_call() for ccc in self.cc_combos):
            #     return "all " + F_CALL
            # if any(ccc.has_function_call() for ccc in self.cc_combos):
            #     return "has " + F_CALL
            # return other
        cc_combo = list(self.cc_combos)[0]
        cat = cc_combo.category()
        return cat

    def has_function_call(self):
        return any(ccc.has_function_call() for ccc in self.cc_combos)

    def only_function_call(self):
        return all(ccc.only_function_call() for ccc in self.cc_combos)

    def what_is_with_fc(self):
        results = []
        if self.only_function_call():
            props = set(flatten(ccc.props for ccc in self.cc_combos))
            if not props:
                results.append("just " + F_CALL + " without properties")
            else:
                if not props.isdisjoint(ARGUMENT_PROPERTIES):
                    results.append("just " + F_CALL + " with argument changes")
                if ASYNC_TRANS in props:
                    results.append("just " + F_CALL + " with " + short_name(ASYNC_TRANS))
                if OUT_TRANS in props:
                    results.append("just " + F_CALL + " with " + short_name(OUT_TRANS))
                if ENC in props:
                    results.append("just " + F_CALL + " with " + short_name(ENC))
                if PARAM_ADD_TO_DECORATE in props:
                    raise ValueError(short_name(PARAM_ADD_TO_DECORATE) + " in " + F_CALL)
                print(props)
        elif self.has_function_call():
            for ccc in self.cc_combos:
                non_fc_pes = sort_join(ccc.all_pes - {F_CALL})
                if non_fc_pes:
                    if ccc.has_function_call():
                        results.append(non_fc_pes + " in same cc")
                    else:
                        results.append(non_fc_pes + " in different cc")
        else:
            results.append("does not have " + F_CALL)

        return sort_join(set(results), "\n")


def big_combination_stats():
    combination_count: dict[MigCombination, int] = {}
    migs = load_migs()

    total_migs = 0
    for mig in migs:
        if mig.is_import_only():
            continue

        total_migs += 1
        mig_comb = MigCombination(mig)
        if mig_comb not in combination_count:
            combination_count[mig_comb] = 0

        combination_count[mig_comb] += 1

    data = [[combo, count, 100 * count / total_migs, len(combo.cc_combos), combo.what_is_with_fc()] for combo, count in
            combination_count.items()]
    with_fc_col = "what is with FC"
    mig_count_col = "# migs"
    mig_pecent_col = "% migs"
    df = pd.DataFrame(data, columns=["combination", mig_count_col, mig_pecent_col, "comb size", with_fc_col]) \
        .sort_values(mig_count_col, ascending=False).reset_index(drop=True)
    df.index += 1
    df.to_csv(config.report_dir / "migration-combination.csv")

    with_fc_group = df[[with_fc_col, mig_count_col, mig_pecent_col]].groupby(with_fc_col).sum()
    with_fc_group.to_csv(config.report_dir / "migration-combination--with-fc-groups.csv")

    has_fc_combo_count = sum(1 for combo in combination_count if combo.has_function_call())
    # just_fc_percent = with_fc_group[with_fc_group[with_fc_col] == "just function call"][mig_pecent_col]
    latex_data = {
        "UniqueCCCombo": len(combination_count),
        "HasFcComboCount": has_fc_combo_count,
        "HasFcComboPercent": percent(has_fc_combo_count, len(combination_count), True),
        "ComboFunctionCallWithElemNCPercent": escape("8.2%"),
        "ComboAtAtAndFcFcNoPropPercent": red(escape("0.8%")),
        "ComboJustFcMigPercent": escape("56%"),
        "ComboJustNonFCMigPercent": escape("7%"),
        "ComboMixFcNonFcMigPercent": escape("37%"),
        "ComboHasNonFCMigPercent": escape("44%"),  # sum of just nonfc and fc
        "AttributeWithFCInDiffCCPercent": escape("13%"),
        "AttributeWithFCInSameCCPercent": escape("9%"),
        "DecoratorWithFCInDiffCCPercent": escape("11%"),
        "DecoratorWithFCInSameCCPercent": escape("8%"),
        "ExceptionWithFCInSameCCPercent": escape("5%"),
        "TypeWithFCInSameCCPercent": escape("3.5%"),
        "FuncRefWithFCInSameCCPercent": escape("1.6%"),
        "JustFunctionWithNoPropsMigsPercent": escape("10%"),
        "JustFunctionWithENCPercent": escape("10%"),
        "TrivialFCMigPercent": escape("20%"),  # sum of the above two
        "NonTrivialFCMigPercent": escape("75%"),
    }

    update_report_data(latex_data)


if __name__ == '__main__':
    big_combination_stats()
