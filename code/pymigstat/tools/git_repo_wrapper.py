import time
from pathlib import Path

from tools import ExternalTool
from tools.external_tool import ExternalToolException


class GitRepo(ExternalTool):
    def __init__(self, path: Path):
        super().__init__("git")
        self.git_path = path
        if not self.git_path.exists():
            raise FileNotFoundError(f"  repo not available at {self.git_path}")

    def get_diff(self, hash: str):
        diff = self.run("--no-pager", "show", "--diff-filter=M", "--encoding=utf-8", hash, "--", "*.py")
        return diff

    def get_hashes(self):
        hashes = self.run("log", "--no-merges", "--topo-order", "--reverse", "--format=%H", "--", "*.py").splitlines(
            keepends=False)
        return hashes

    def checkout(self, hash: str):
        self.run("restore", ".")
        self.run("checkout", "-f", hash)

    def get_modified_files(self, hash: str):
        # get Python files which are added (A) or modified (M)
        files = self.run("diff-tree", "--no-commit-id", "--name-only", "--diff-filter", "AM", "-r", hash, "--", "*.py",
                         "*.PY").splitlines(keepends=False)
        return files

    def is_ancestor(self, potential_ancestor_hash: str, potential_descendant_hash: str):
        # merge-base --is-ancestor returns code 0 (i.e., success) if ancestor, returns 1 otherwise
        # https://git-scm.com/docs/git-merge-base#Documentation/git-merge-base.txt---is-ancestor
        try:
            self.run("merge-base", "--is-ancestor", potential_ancestor_hash.strip(), potential_descendant_hash.strip())
            return True
        except ExternalToolException as e:
            if e.result.returncode == 1:
                return False
            raise e

    def run(self, *args):
        # run only if the git lock is clear. but not too long.
        wait_count = 0
        lock_path = self.git_path / ".git" / "index.lock"
        while wait_count < 5 and lock_path.exists():
            print(f"    {self.git_path}: git repo is locked. Waiting for 0.5 seconds.")
            time.sleep(.5)
            wait_count += 1

        if lock_path.exists():
            # if the lock still exists, it is perhaps for an previous error.
            # so remove it and try the command
            print(f"    {self.git_path}: clearing the lock.")
            lock_path.unlink(True)

        # always run on at the git repo path
        return super().run(*args, cwd=self.git_path)
