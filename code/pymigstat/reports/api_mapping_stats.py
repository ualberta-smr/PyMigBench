from pathlib import Path

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from config import config
from latex.core import TextNode, BeginEndNode, TagNode, Node
from latex.graphics import GraphicsNode
from latex.tables import Tabular
from latex.utils import to_macro_name
from reports.api_mapping_data import *
from reports.update_report_data import update_report_data, percent


class ApiMappingStats:
    def __init__(self):
        self.data = APIMappingData()

    def _data_cell(self, src, tgt) -> Node:
        lp_count_key = lp_count_latex_key(src, tgt)
        lp_value = self.data.lip_pair_count(src, tgt)

        if lp_value > 0:
            cc_part = f"{lp_count_key}~({lp_percent_latex_key(src, tgt)})"
            if not {IMP, NO_PE}.isdisjoint({src, tgt}):
                return TextNode(cc_part)
            # prop: self.data[
            prop_data = pd.DataFrame({p: self.data.prop_count(src, tgt, p) for p in ALL_PROPS_WITH_NO_PROPS},
                                     index=["# cc"])
            plt.figure()
            local_path = Path("img", "props", f"{src}-{tgt}.pdf".replace(" ", "_"))
            self.save_properties_chart(local_path, prop_data)

            # return TextNode(cc_part)
            # return GraphicsNode(local_path.as_posix(), "1cm")
            return TagNode("makecell",
                           [cc_part + " \\\\ " + GraphicsNode(local_path.as_posix(), "1.3cm", "0.5cm").render()])
        else:
            return TextNode("-")

    def save_properties_chart(self, local_path, prop_data, legend_only=False):
        fig_path = config.paper_dir / local_path
        bar = prop_data.plot(kind="barh", stacked=True, legend=False, width=0 if legend_only else 1)
        if legend_only:
            bar.legend(ncol=9, frameon=False)
        bar.set(xticklabels=[], yticklabels=[], xlabel=None, ylabel=None)
        bar.tick_params(bottom=False, left=False)
        sns.despine(left=True, bottom=True)
        bar.get_figure().savefig(fig_path, bbox_inches='tight')

    def export_latex(self):
        total_lps = self.data.lip_pair_count(TOTAL, TOTAL)
        latex_data = {}
        dims = ALL_PES + [NO_PE, TOTAL]
        for spe in dims:
            for tpe in dims:
                lp_count = self.data.lip_pair_count(spe, tpe)
                latex_data[lp_count_latex_key(spe, tpe)] = lp_count
                latex_data[lp_percent_latex_key(spe, tpe)] = percent(lp_count, total_lps)

                if lp_count:
                    for prop in ALL_PROPS_WITH_NO_PROPS:
                        latex_data[cc_prop_percent_latex_key(spe, tpe, prop)] = self.data.prop_percent(spe, tpe, prop)

        fc_fc_enc_count = self.data.prop_count(F_CALL, F_CALL, ENC)
        fc_fc_count = self.data.api_mapping_count(F_CALL, F_CALL)
        latex_data[to_macro_name(F_CALL, F_CALL, "SameNamePercent")] = percent(fc_fc_count - fc_fc_enc_count, fc_fc_count)

        # total_enc_count = self.data.prop_count(TOTAL, TOTAL, ENC)
        # total_count = self.data.api_mapping_count(TOTAL, TOTAL) - self.data.api_mapping_count(IMP, IMP)
        # # also need to remove no program elements
        # latex_data[to_macro_name(TOTAL, "SameNamePercent")] = percent(total_count - total_enc_count, total_count)

        latex_data[to_macro_name("HasNonFunctionLPPercent")] = percent(self.data.non_function_libpairs_count(),
                                                                       total_lps)
        update_report_data(latex_data)

        return self

    def grid_2d(self):
        table = BeginEndNode(0, "table*", optional_args=["t!"])
        table \
            .start_line(1).add_tag("centering") \
            .start_line(1).add_tag("caption", "Distribution of types of API mappings in \\migbenchTwo") \
            .start_line(1).add_tag("label", "tab:taxonomy-dist")

        legend_data = pd.DataFrame({short_name(p): [0] for p in ALL_PROPS_WITH_NO_PROPS}, index=["# cc"])
        legend_path = Path("img", "props", f"legend.pdf")
        self.save_properties_chart(legend_path, legend_data, True)
        table.add_child(GraphicsNode(legend_path.with_suffix(".png").as_posix(), "\\textwidth"))
        # We manually saved part of the image legend. Automate it if possible

        # first row is multi-col saying "target"
        # second row has a target program element in each cell
        # first col is multi-row indicating "source", rotated text
        # second col has a source program element in each cell

        tabular = self.create_tabular()
        resize_box = TagNode("resizebox", ["\\textwidth", "!", tabular.render()])

        table.start_line(1).add_child(resize_box)
        table_content = table.add_warning().render() + "\n"
        path = Path("..", "..", "paper", "tabs", "taxonomy-distribution.tex")
        print(table_content)
        print("writing to: " + str(path.absolute().resolve()))
        path.write_text(table_content, encoding="utf8")

    def create_tabular(self):
        tabular = Tabular(2, "ll" + ("c" * len(ALL_PE_DIMS)))
        tabular.add_tag("hline")
        top_cell = TagNode("multicolumn", [len(ALL_PE_DIMS), "c", "\\textbf{Target program elements}"])
        tabular.add_cell(TextNode("")).add_cell(TextNode("")).add_cell(top_cell).end_row()
        for tpe in ["", "", *ALL_PE_DIMS]:
            tabular.add_cell(TagNode("textbf", [tpe]))
        tabular.end_row()
        multirow_size = len(ALL_PE_DIMS) * 2
        left_cell = TagNode("multirow",
                            [multirow_size, "*",
                             TagNode("rotatebox", [90, "\\textbf{Source program elements}"]).render()])
        for i, src in enumerate(ALL_PE_DIMS):
            if i > 0:
                left_cell = TextNode("")
            tabular.add_tag("cmidrule", f"{3}-{len(ALL_PE_DIMS) + 2}")
            tabular.add_cell(left_cell).add_cell(TagNode("textbf", [src]))
            for tgt in ALL_PE_DIMS:
                cell = self._data_cell(src, tgt)
                tabular.add_cell(cell)
            tabular.end_row()
        tabular.add_child(TagNode("hline"))
        return tabular


def _data_key_prefix(src_pe, tgt_pe):
    if src_pe == TOTAL and tgt_pe == TOTAL:
        prefix = TOTAL
    else:
        prefix = src_pe + " " + tgt_pe
    return prefix


def lp_count_latex_key(src_pe, tgt_pe):
    return to_macro_name(_data_key_prefix(src_pe, tgt_pe) + " L P Count")


def cc_prop_count_latex_key(src_pe, tgt_pe, prop: str):
    return to_macro_name(_data_key_prefix(src_pe, tgt_pe) + " " + prop + " Count")


def cc_prop_percent_latex_key(src_pe, tgt_pe, prop: str):
    return to_macro_name(_data_key_prefix(src_pe, tgt_pe) + " " + prop + " Percent")


def lp_percent_latex_key(src_pe, tgt_pe):
    return to_macro_name(_data_key_prefix(src_pe, tgt_pe) + " L P Percent")


def program_elements_stats_in_libpairs():
    ApiMappingStats().export_latex().grid_2d()


if __name__ == '__main__':
    program_elements_stats_in_libpairs()
