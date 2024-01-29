from typing import Tuple

from core.pypi_cache import PyPICache
from datamodels.data_reader import *
from datamodels.storage import save_data
from utils.gpt_client import get_csv
from utils.utils import reponame_to_filename, commit_url


def lib_pairs_from_migs(migs: set[Tuple]):
    return {(mig[2], mig[3]) for mig in migs}


def libs_from_migs(migs: set[Tuple]):
    return {mig[2] for mig in migs}.union({mig[3] for mig in migs})


def repos_from_migs(migs: set[Tuple]):
    return {mig[0] for mig in migs}


def commits_from_migs(migs: set[Tuple]):
    return {mig[1] for mig in migs}


def domains_from_migs(migs: set[Tuple]):
    return {mig[4] for mig in migs}


def report_count(migs, lib_pairs, libs, repos, commits, domains):
    print(f"migrations   :{len(migs)}")
    print(f"lib pairs    :{len(lib_pairs)}")
    print(f"libraries    :{len(libs)}")
    print(f"repositories :{len(repos)}")
    print(f"commits      :{len(commits)}")
    print(f"domains      :{len(domains)}")


def is_salm_testing_domain(domain: str):
    return domain == "testing" or domain.startswith("testing&") or domain.endswith("&testing")


def filter_migration_data():
    pmb_migs = read_unfiltered_migbench_migs()
    pmb_pairs = lib_pairs_from_migs(pmb_migs)
    pmb_libs = libs_from_migs(pmb_migs)
    pmb_repos = repos_from_migs(pmb_migs)
    pmb_commits = commits_from_migs(pmb_migs)
    pmb_domains = domains_from_migs(pmb_migs)

    raw_salm_migs = read_unfiltered_salm_migs()
    print("==== filtering SALM migrations ===")
    # pmb_migs_in_salm = raw_salm_migs.intersection(pmb_migs)
    # print(f"removing {len(pmb_migs_in_salm)} migrations which are already in PyMigBench")
    # raw_salm_migs = raw_salm_migs - pmb_migs_in_salm

    salm_testing_migs = {mig for mig in raw_salm_migs if is_salm_testing_domain(mig[4])}
    print(f"removing {len(salm_testing_migs)} test library migrations")
    raw_salm_migs = raw_salm_migs - salm_testing_migs

    salm_migs = filter_migrations(raw_salm_migs)
    salm_pairs = lib_pairs_from_migs(salm_migs)
    salm_libs = libs_from_migs(salm_migs)
    salm_repos = repos_from_migs(salm_migs)
    salm_commits = commits_from_migs(salm_migs)
    salm_domains = domains_from_migs(salm_migs)

    all_migs = pmb_migs.union(salm_migs)
    all_pairs = lib_pairs_from_migs(all_migs)
    all_libs = libs_from_migs(all_migs)
    all_repos = repos_from_migs(all_migs)
    all_commits = commits_from_migs(all_migs)
    all_domains = domains_from_migs(all_migs)

    print()
    print("==== SALM dataset ===")
    report_count(salm_migs, salm_pairs, salm_libs, salm_repos, salm_commits, salm_domains)
    print("==== PyMigBench dataset ===")
    report_count(pmb_migs, pmb_pairs, pmb_libs, pmb_repos, pmb_commits, pmb_domains)
    print("=== combined dataset ===")
    report_count(all_migs, all_pairs, all_libs, all_repos, all_commits, all_domains)

    import_map = fetch_import_names(all_libs)
    for lib in all_libs:
        save_data({"name": lib, "import_names": import_map[lib]}, "", config.lib_data_dir, lib + ".yaml")
    for src, tgt in all_pairs:
        save_data({"source": src, "target": tgt}, "", config.data_dir, "lib_pair", f"{src}__{tgt}.yaml")
    save_migrations(pmb_migs, "pymigbench")
    save_migrations(salm_migs, "salm")
    for repo in all_repos:
        save_data({"name": repo}, "", config.data_dir, "repo", reponame_to_filename(repo), "meta.yaml")


def save_migrations(migrations: set, data_source: str):
    for repo, commit, src, tgt, domain in migrations:
        url = commit_url(repo, commit)
        file_name = f"{src}__{tgt}__{reponame_to_filename(repo)}__{commit[:8]}__{data_source}.yaml"
        save_data({"repo": repo, "commit": commit, "source": src, "target": tgt, "domain": domain, "commit_url": url},
                  "", config.data_dir, "migration", file_name)


def filter_migrations(migs: set[tuple]):
    lib_pairs = lib_pairs_from_migs(migs)
    libs = libs_from_migs(migs)
    repos = repos_from_migs(migs)
    commits = commits_from_migs(migs)
    domains = domains_from_migs(migs)
    report_count(migs, lib_pairs, libs, repos, commits, domains)

    print()
    print("checking the libraries in PyPI. It may take a few minutes.")
    pypi_cache = PyPICache(config)
    non_pypi_libs = {lib_name for lib_name in libs if not pypi_cache.is_in_pypi(lib_name)}
    non_pypi_pairs = {lp for lp in lib_pairs if lp[0] in non_pypi_libs or lp[1] in non_pypi_libs}
    non_pypi_migs = {mig for mig in migs if (mig[2], mig[3]) in non_pypi_pairs}
    print(f"{len(non_pypi_libs)} libs excluded because they are not in PyPI")
    print(f"{len(non_pypi_pairs)} lib pairs excluded because at least one lib is not in PyPI")
    print(f"{len(non_pypi_migs)} migrations excluded because at least one lib is not in PyPI")
    pypi_lib_pairs = lib_pairs - non_pypi_pairs
    pypi_migs = migs - non_pypi_migs
    # todo: find analogous pairs using GPT-4
    # for now, use the cached result
    analogous_results = read_analogous_lib_results()
    all_non_analogous_pairs = {(res[0], res[1]) for res in analogous_results if res[2] == "No"}
    non_analogous_pairs = all_non_analogous_pairs.intersection(pypi_lib_pairs)
    non_analogous_migs = {m for m in pypi_migs if (m[2], m[3]) in non_analogous_pairs}
    print(f"{len(non_analogous_pairs)} lib pairs excluded because they are not analogous")
    print(f"{len(non_analogous_migs)} migrations excluded because they are between non analogous pairs")
    final_migs = pypi_migs - non_analogous_migs

    return final_migs


def fetch_import_names(libs: set[str]):
    filepath = config.data_dir / "gpt4_import_names.csv"
    if not filepath.exists():
        message = """
        For the python libraries below, give me the corresponding top level import name in a CSV, 
        where the first column is the library name, the second column is the import names, 
        and the third column is your confidence level of the result. 
        For a library, if you find both a.b and a, just output a.
        Also, just give the import name, not the full statement.
        Here are the comma separated library names:
        """
        message += ", ".join(libs)
        result = get_csv(message)
        filepath.write_text(result, "utf8")

    rows = read_csv(filepath)
    return {r[0]: r[1].split(" ") for r in rows}


if __name__ == '__main__':
    filter_migration_data()
