import subprocess
from subprocess import CompletedProcess
from pathlib import Path
from typing import Callable


class ExternalTool:
    def __init__(self, path_or_command: str | Path, error_condition: Callable[[CompletedProcess], bool] = None):
        self._error_condition = error_condition
        if isinstance(path_or_command, Path):
            self.path_or_command = str(path_or_command.resolve())
        else:
            self.path_or_command = path_or_command

    def run(self, *args, cwd="."):
        args_ = [self.path_or_command, *args]
        arg_str = " ".join(args_)  # this is for debug. do not remove
        result = subprocess.run(args_, capture_output=True, text=True, cwd=cwd,
                                encoding="utf-8")
        if self.has_error(result):
            raise ExternalToolException(result)

        return result.stdout

    def has_error(self, result: CompletedProcess):
        if self._error_condition:
            return self._error_condition(result)
        return result.returncode != 0


class ExternalToolException(Exception):
    def __init__(self, result: CompletedProcess):
        super().__init__(result.stderr)
        self.result = result
