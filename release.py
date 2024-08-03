"""
This file is not part of the library itself, rather is a script to build the library.
This should have minimal third-party dependencies so that it can be run in any environment.

Third-party dependencies that should be globally installed:
- requests
"""
import json
import shutil
import subprocess
import sys

import requests


class Release:
    def __init__(self, non_interactive: bool):
        self.non_interactive = non_interactive
        self.version = open("./version").read().strip()
        self.secrets = json.load(open("./secrets.json"))
        self.pypi_release_url = f"https://pypi.org/project/pymigbench/{self.version}/"
        self.github_repo = "ualberta-smr/pymigbench"
        self.github_url = f"https://github.com/{self.github_repo}"

    def validate(self):
        gh_tag = f"v{self.version}"

        try:
            current_tag = run_command(["git", "describe", "--tags", "--exact-match"])
            if current_tag.strip() != gh_tag:
                raise ValueError(f"Current tag {current_tag} does not match the expected tag {gh_tag}.")
        except Exception as e:
            raise ValueError(f"Current head is not tagged with the expected version: {gh_tag}") from e

        response = requests.head(self.pypi_release_url)
        if response.status_code == 200:
            raise ValueError(f"Version {self.version} already released on PyPI.")

        print("Validated")
        print(f"  Version: {self.version}")
        return self

    def build(self):
        print("Building...")
        run_command(["python", "-m", "build"])
        print("Built successfully.")
        return self

    def publish_pypi(self):
        if self.non_interactive:
            return self
        if not self.non_interactive:
            confirm = input("Do you want to publish to PyPI? Note that this is an irreversible process. (y/n): ")
            if confirm.lower() != 'y':
                print("Not publishing to PyPI.")
                return self
        print("Publishing to PyPI...")
        run_command(["twine", "upload", "dist/*", "-u", "__token__", "-p", self.secrets['pypi']])
        print("Published to PyPI.")
        return self


def run_command(commands: list[any]):
    process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    lines = []
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            lines.append(output.strip())
            print(output.strip())

    return "\n".join(lines)


def main():
    non_interactive = "--non-interactive" in sys.argv
    Release(non_interactive).build().validate().publish_pypi()


if __name__ == "__main__":
    main()
