import os
import shutil
import subprocess
import sys
import timeit
from datetime import datetime
from multiprocessing import Pool
from pathlib import Path

from config import config
from datamodels.storage import load_data_list
from utils.utils import reponame_to_filename


def download_all(repos: list[str]):
    start = timeit.default_timer()

    os.environ["GIT_TERMINAL_PROMPT"] = "0"

    log_path = config.data_dir.joinpath(f"_log_{datetime.now().isoformat().replace(':', '-')}.txt")

    total = len(repos)
    with Pool(config.number_of_parallel_processes) as pool:
        results = pool.imap(download_one_repo, repos, chunksize=5)

        i = 0
        for success, message in results:
            i += 1
            runtime = (timeit.default_timer() - start) / 60 / 60
            part_done = i / total
            print(
                f"=== done downloading ({part_done:.2%}) repos in {runtime:.4f} hours. "
                f"Est {runtime * (1 - part_done) / part_done:.4f} hours===")
            print()
            print()
            if not success:
                log_path.write_text(message + "\n", "utf-8")


def download_one_repo(repo_name: str):
    try:
        repo_url = f"https://github.com/{repo_name}"
        git_dir: Path = config.git_dir / reponame_to_filename(repo_name)
        try:
            if git_dir.exists():
                if config.skip_download_if_exists:
                    print(f"skipping download. repo exists at {git_dir}")
                else:
                    fetch(git_dir)
            else:
                clone(git_dir, repo_url)
        except:
            shutil.rmtree(git_dir)
            clone(git_dir, repo_url)
        return True, f"done downloading {repo_name}"
    except Exception as e:
        return False, str(e)


def clone(git_dir: Path, repo_url: str):
    print("== cloning ==")
    cmd = " ".join(["git", "clone", repo_url, str(git_dir), "--progress", "--verbose"])
    print(cmd)
    subprocess.check_call(cmd, shell=True, stdout=sys.stdout,
                          stderr=subprocess.STDOUT)


def fetch(git_dir: Path):
    print("== fetching ==")
    cmd = " ".join(["git", "-C", str(git_dir), "fetch", "--progress", "--verbose"])
    print(cmd)
    subprocess.check_call(cmd, shell=True, stdout=sys.stdout,
                          stderr=subprocess.STDOUT)


def download_repos():
    repo_names = [repo["name"] for repo in load_data_list("repo/*/meta.yaml")]
    download_all(repo_names)


if __name__ == '__main__':
    download_repos()
