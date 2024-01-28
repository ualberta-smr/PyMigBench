from pathlib import Path

import yaml


def _load_config():
    dev_config = yaml.safe_load(Path("../configs/config.dev.yaml").read_text(encoding="utf8")) or {}
    global_config = yaml.safe_load(Path("../configs/config.yaml").read_text(encoding="utf8")) or {}
    final_config = dict(global_config, **dev_config)
    return Config(final_config)


class Config:
    def __init__(self, config_dict: dict[str, any]):
        self.data_dir = Path(str(config_dict['data_dir'])).resolve()
        self.paper_dir = Path("..", "..", "paper").resolve()
        self.report_dir = Path("..", "report").resolve()
        self.mig_yaml_dir = Path("..", "..", "data", "migration").resolve()
        self.git_dir = Path(str(config_dict['git_dir'])).resolve()
        self.github_tokens: list[str] = config_dict['github_tokens']
        self.skip_download_if_exists: bool = config_dict['skip_download_if_exists']

        self.repo_data_dir = self.data_dir / "repo"
        self.excluded_repo_data_dir = self.data_dir / "repo.excluded"

        self.lib_data_dir = self.data_dir / "lib"

        self.number_of_parallel_processes = int(config_dict["number_of_parallel_processes"])
        self.gpt_api_key = str(config_dict["gpt_api_key"])
        self.data_gsheet_id = str(config_dict["data_gsheet_id"])

        self.report_dir.mkdir(parents=True, exist_ok=True)


config = _load_config()
