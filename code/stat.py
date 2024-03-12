import yaml
from pathlib import Path

def _is_import(cc):
    return cc["source_program_elements"] == ["import"] or cc["target_program_elements"] == ["import"]

def stat():
    mig_dir = Path("data/migration")
    if not mig_dir.exists():
        print("could not find the migration directory. Please run this command from the root of the project.")
        return
    
    mig_files = mig_dir.glob("*.yaml")
    migs = [yaml.safe_load(f.open()) for f in mig_files]    
    files = [f for mig in migs for f in mig["files"]]
    
    ccs = [cc for file in files for cc in file["code_changes"]]
    import_ccs = [cc for cc in ccs if _is_import(cc)]
    api_ccs = [cc for cc in ccs if not _is_import(cc)]

    migs_count = len(migs)
    repos_count = len(set(mig["repo"] for mig in migs))
    files_count = len(files)
    cc_count = sum(len(cc["lines"]) for cc in ccs)
    api_cc_count = sum(len(cc["lines"]) for cc in api_ccs)
    import_cc_count = sum(len(cc["lines"]) for cc in import_ccs)
    lib_pair_count = len({(mig["source"], mig["target"]) for mig in migs})

    
    print(f"Migs: {migs_count}")
    print(f"Repos: {repos_count}")
    print(f"Lib pairs: {lib_pair_count}")
    print(f"Files: {files_count}")
    print(f"Code changes: {cc_count}")
    print(f"API code changes: {api_cc_count}")
    print(f"Import code changes: {import_cc_count}")


if __name__ == "__main__":
    stat()

