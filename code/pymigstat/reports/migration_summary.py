import pandas as pd

from config import config
from datamodels.loaders import load_migs
from utils.utils import flatten_unique_sort


def migration_summary():
    rows = []
    for i, mig in enumerate(load_migs(), start=1):
        properties = flatten_unique_sort(cc.properties for cc in mig.code_changes())
        source_pes = flatten_unique_sort(cc.source_program_elements for cc in mig.code_changes())
        target_pes = flatten_unique_sort(cc.target_program_elements for cc in mig.code_changes())
        rows.append([
            mig.source,
            mig.target,
            mig.repo,
            mig.commit,
            len(mig.code_changes()),
            len(mig.files),
            ", ".join(source_pes),
            ", ".join(target_pes),
            ", ".join(properties),
            len(set(source_pes + target_pes)),
            len(properties),
            mig.commit_url,
            mig.id()
        ])

    df = pd.DataFrame(rows, columns=["source", "target", "repo", "commit", "# ccs", "# files", "source PEs",
                                     "target PEs", "properties", "# PE", "# props", "commit URL", "id"])
    df.to_csv(config.report_dir.joinpath("migrations.csv"), index=False)


if __name__ == '__main__':
    migration_summary()
