from config import config
from datamodels.api_mapping import APIMappingSet
from datamodels.migration import migration_from_file


# todo: cache the migs
def load_migs():
    mig_files = config.mig_yaml_dir.glob("*.yaml")
    return [migration_from_file(mf) for mf in mig_files]


def load_api_mappings():
    all = APIMappingSet()
    for mig in load_migs():
        all.merge_all(mig.api_mappings(True))

    return all
