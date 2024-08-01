from pymigbench.code_change import CodeChange


class MigrationFile:
    def __init__(self, path: str, code_changes: list[CodeChange]):
        self.path = path
        self.code_changes = code_changes
        self.mig: 'Migration' = None
        for cc in self.code_changes:
            cc.file = self

    def id(self):
        return f"{self.mig.id()}__{self.path}"

    def __str__(self):
        return f"{self.path}@{self.mig}"

    def api_ccs(self):
        return [cc for cc in self.code_changes if not cc.is_import()]
