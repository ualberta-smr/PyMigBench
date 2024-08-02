from pymigbench.code_change import CodeChange
from pymigbench.migration_file import MigrationFile


class Migration:
    def __init__(self, repo: str, commit: str, source: str, target: str, files: list[MigrationFile], domain: str):
        self.repo = repo
        self.commit = commit
        self.source = source
        self.target = target
        self.files = files
        self.domain = domain
        self._ccs: list[CodeChange] | None = None
        self.pair_id = "__".join([self.source, self.target])
        self.commit_url: str = f"https://github.com/{self.repo}/commit/{self.short_commit()}"
        for file in self.files:
            file.mig = self

    def short_commit(self):
        return self.commit[:8]

    def id(self):
        return "__".join([self.source, self.target, self.repo, self.short_commit()])

    def code_changes(self):
        if self._ccs is None:
            self._ccs = [cc for file in self.files for cc in file.code_changes]
        return self._ccs

    def __str__(self):
        return self.id()

    def __repr__(self):
        return str(self)
