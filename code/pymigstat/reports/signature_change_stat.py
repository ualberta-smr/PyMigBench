import pandas as pd

from config import config


def signature_change_stat():
    df = pd.read_csv(config.report_dir / "complexity_all.csv")
    pe_prop = "program elements"
    can_have_name_change = df[df[pe_prop].str.contains("attribute access|decorator|exception|function call|function object|type")]
    has_name_change = can_have_name_change[can_have_name_change["properties"].str.contains("element name change")]
    print(len(can_have_name_change), len(has_name_change))

    can_have_argument_change = df[df[pe_prop].str.contains("decorator|function call")]
    has_argument_change = can_have_argument_change[can_have_name_change["properties"].str.contains("argument addition|argument deletion|argument transformation|argument name change|argument name deletion")]
    print(len(can_have_argument_change), len(has_argument_change))


if __name__ == '__main__':
    signature_change_stat()
