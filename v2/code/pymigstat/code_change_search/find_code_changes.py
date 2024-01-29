from pathlib import Path

from code_change_search.diff_meta_parser import DiffMetaParser
from code_change_search.usage_resolver import UsageResolver
from config import config
from datamodels.migration import Migration, MigrationCodeFile, CodeChangeInMig, APIUsage
from datamodels.storage import load_data
from tools import GitRepo
from utils import Dynamic


def find_code_changes(repo_path: Path, commit: str, source_name: str, target_name: str, domain: str):
    git_repo = GitRepo(repo_path)
    diff_text = git_repo.get_diff(commit)
    diff_files = DiffMetaParser(diff_text).parse()

    migration = Migration(repo_path.stem.replace("@", "/"), commit, source_name, target_name, [], "", domain)

    source_lib: Dynamic = load_data(config.lib_data_dir, source_name + ".yaml")
    target_lib: Dynamic = load_data(config.lib_data_dir, target_name + ".yaml")

    source_imports = list(source_lib["import_names"])
    target_imports = list(target_lib["import_names"])
    # print(f"  repo: {repo_path}")
    errors = []

    for file in diff_files:
        try:
            src_usage_resolver = UsageResolver(git_repo.run("show", f"{commit}^:{file.path}"), file.path)
            tgt_usage_resolver = UsageResolver(git_repo.run("show", f"{commit}:{file.path}"), file.path)
        except SyntaxError as se:
            errors.append(file.path + " :: " + str(se))
            print(f"  file: {file.path}")
            print(str(se))
            continue

        source_lines = src_usage_resolver.find_used_lines(source_imports).intersection(file.removed_lines)
        target_lines = tgt_usage_resolver.find_used_lines(target_imports).intersection(file.added_lines)

        if source_lines or target_lines:
            mig_file = MigrationCodeFile(file.path, [], sorted(source_lines), sorted(target_lines))
            migration.files.append(mig_file)

    if errors:
        migration.errors = errors
    return migration


def find_code_changes_from_raw_migration(migration_info: Dynamic):
    repo = migration_info["repo"]
    repo_filename = repo.replace("/", "@")
    repo_path = config.git_dir / repo_filename
    commit = migration_info["commit"]
    source = migration_info["source"]
    target = migration_info["target"]
    domain = migration_info["domain"]
    migration = find_code_changes(repo_path, commit, source, target, domain)
    return migration
