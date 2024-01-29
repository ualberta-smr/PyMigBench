from multiprocessing import Pool

from code_change_search.find_code_changes import find_code_changes_from_raw_migration
from config import config
from datamodels.storage import save_data, load_data_list
from utils import Dynamic
from utils.progress import Progress
from utils.utils import reponame_to_filename


def identify_code_change(mig: Dynamic):
    file_name = "__".join([mig['source'], mig['target'], reponame_to_filename(mig['repo']), mig['commit'][:8]])
    file_name += ".yaml"
    try:
        mig_with_cc = find_code_changes_from_raw_migration(mig)
        if mig_with_cc.files:
            out_folder = "code_change"
        else:
            out_folder = "code_change.not_found"

        save_data(mig_with_cc.to_dict(), "", config.data_dir, out_folder, file_name)
    except FileNotFoundError:
        save_data(mig, "", config.data_dir, "code_change.repo_not_found", file_name)
    except Exception as e:
        copy = dict(mig)
        copy["errors"] = [repr(e)]
        save_data(copy, "", config.data_dir, "code_change.detection_error", file_name)
        print(file_name)
        print(e)


def find_all_code_changes(parallel):
    migs = load_data_list("migration/*__salm.yaml")
    migs = sorted(migs, key=lambda m: m["repo"])
    progress = Progress(len(migs), "migrations")

    if parallel:
        with Pool(config.number_of_parallel_processes) as pool:
            results = pool.imap(identify_code_change, migs, chunksize=5)
            for _ in results:
                progress.update()
    else:
        for mig in migs:
            identify_code_change(mig)
            progress.update()


if __name__ == '__main__':
    find_all_code_changes(False)
