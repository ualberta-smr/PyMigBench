import shutil

from config import config

if __name__ == '__main__':
    cleanup_dirs = [config.data_dir / f for f in
                    ["code_change", "code_change.detection_error", "code_change.not_found", "lib", "lib_pair",
                     "migration", "repo"]]
    print("This will cleanup the data that is already populated.")
    print("The following folders will be deleted:")
    print(*cleanup_dirs, sep="\n")

    choice = input("Are you sure you want to continue? [y/N]: ")
    if choice == "y" or choice == "Y":
        for dir in cleanup_dirs:
            shutil.rmtree(dir, ignore_errors=True)
        print("done cleaning up")
    else:
        print("skipped cleaning up")
