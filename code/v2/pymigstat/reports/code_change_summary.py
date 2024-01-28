from pathlib import Path

import pandas as pd

from config import config
from datamodels.loaders import load_migs


def code_change_summary():
    rows = []
    for i, mig in enumerate(load_migs(), start=1):
        for file in mig.files:
            ccs = file.code_changes
            for cc in ccs:
                rows += [[
                    mig.source,
                    mig.target,
                    mig.repo,
                    mig.commit,
                    file.path,
                    cc.line,
                    ", ".join(cc.source_program_elements),
                    ", ".join(cc.target_program_elements),
                    cc.cardinality,
                    ", ".join(cc.properties),
                    ", ".join(cc.source_apis),
                    ", ".join(cc.target_apis),
                    mig.commit_url,
                    mig.id()
                ]]

    df = pd.DataFrame(rows, columns=["source", "target", "repo", "commit", "path", "line", "source PEs",
                                     "target PEs", "cardinalities", "properties", "source APIs", "target APIs",
                                     "commit URL", "mig id"])
    df.to_csv(config.report_dir.joinpath("code-changes.csv"), index=False)


if __name__ == '__main__':
    code_change_summary()
