import math
import random

from config import config
from csv_helper import write_csv
from datamodels.migration import serialize_line_list
from datamodels.storage import load_data_list
from utils.utils import key_by
from munch import munchify

code_change_instructions = """
The "files" list contains all files that potentially have code changes. 
Each of the "file" item has a dummy code change. This is to help understand the data structure of the code changes.
Below is how to update the code changes:
1. Open the commit using the URL.
2. For each file in the files list:
    2.1. Locate the file in the GitHub commit page.
    2.2. Go to each of the lines in "candidate_source_lines" and "candidate_target_lines".
    2.3. Find the code changes and add them in this file.
3. Remove the dummy code change.
4. Save this file, commit, push.
"""

output_folder = config.data_dir / "code_change_for_labeling"


def sample_migrations_for_code_change_labeling():
    # 1269 migs, 5% margin of error, 95% confidence level, required sample size = 296

    if output_folder.exists():
        print("The output folder already exists.")
        print("The process will clear all content and recreate new content.")
        choice = input("Are you sure you want to continue? [y/N]: ")
        if choice in {"y", "Y"}:
            print("processing...")
        else:
            print("aborting.")
            return

    all_cc_migs = load_data_list("code_change/*.yaml")
    total_migs = 1269
    assert len(all_cc_migs) == total_migs
    sample_size = 296
    groups = key_by(all_cc_migs, "domain")
    csv_data = []
    header = ["repo", "commit", "source", "target", "file path", "lines", "count", "source APIs", "target APIs",
              "program element", "cardinality", "properties", "commit URL", "candidate source lines",
              "candidate target lines"]
    csv_data.append(header)

    for domain, domain_migs in groups.items():
        domain_size = len(domain_migs)
        sample_size_for_domain = math.ceil(domain_size * sample_size / total_migs)
        sample_size_for_domain = max(2, sample_size_for_domain)
        if sample_size_for_domain > domain_size:
            sample_size_for_domain = domain_size

        samples = random.sample(domain_migs, sample_size_for_domain)
        for m in samples:
            m = munchify(m)
            for f in m.files:
                r = [m.repo, m.commit, m.source, m.target, f.path, "", "", "", "", "", "", "", m.commit_url,
                     serialize_line_list(f.candidate_source_lines, False),
                     serialize_line_list(f.candidate_target_lines, False)]
                csv_data.append(r)
            # file_name = migration_file_name(m)
            # save_data(m, code_change_instructions, output_folder / file_name)

    write_csv(config.data_dir / "sampled_migrations.csv", csv_data, False)


if __name__ == '__main__':
    sample_migrations_for_code_change_labeling()
