import math

import pandas

from config import config
from datamodels.migration import Migration, CodeChangeInMig, MigrationCodeFile
from datamodels.storage import save_data
from utils.utils import reponame_to_filename


def parse_migbench_lines(line: str):
    lines = []
    parts = line.split(",")
    for part in parts:
        if ":" in part:
            for subpart in part.split(":"):
                lines += parse_migbench_lines(subpart)
        elif "-" in part:
            start, end = part.split("-")
            lines += list(range(int(start), int(end) + 1))
        else:
            lines += [int(part)]

    return lines


def convert_pymigbench_data():
    all_pmb_ccs = pandas.read_csv("../sample_data/py_mig_bench__code_changes.csv")
    info_heads = ["repo", "commit", "source", "target"]
    all_pmb_migs = all_pmb_ccs[info_heads].drop_duplicates()
    print(len(all_pmb_migs))
    for _, pmb_mig in all_pmb_migs.iterrows():
        info_list = list(pmb_mig)
        mig = Migration(*info_list, [])
        pmb_ccs = all_pmb_ccs[all_pmb_ccs[info_heads].isin(info_list).all(axis=1)]
        pmb_files = pmb_ccs[["filepath"]].drop_duplicates()
        for _, filepath in pmb_files.iterrows():
            filepath = filepath[0]
            file_pmb_ccs = pmb_ccs[pmb_ccs["filepath"] == filepath]
            file = MigrationCodeFile(filepath, [])
            mig.files.append(file)
            for _, file_pmb_cc in file_pmb_ccs.iterrows():
                source_lines = parse_migbench_lines(file_pmb_cc["source_version_line"])
                target_lines = parse_migbench_lines(file_pmb_cc["target_version_line"])
                program_element = file_pmb_cc["program_element"]
                cardinality = file_pmb_cc["cardinality"]
                properties = str(file_pmb_cc["properties"]).split(",")
                source_apis = parse_api_list(file_pmb_cc["source API"])
                target_apis = parse_api_list(file_pmb_cc["target API"])
                cc = CodeChangeInMig(source_lines, target_lines, source_apis, target_apis, program_element, cardinality,
                                     properties)
                file.code_changes.append(cc)

        file_name = "__".join([reponame_to_filename(mig.repo), mig.commit[:8], mig.source, mig.target])
        file_name += ".yaml"
        save_data(mig.to_dict(), "", config.data_dir, "pymigbench_migs", file_name)


def parse_api_list(value):
    if not value or (isinstance(value, float) and math.isnan(value)):
        return []
    return value.split(",")


if __name__ == '__main__':
    convert_pymigbench_data()
