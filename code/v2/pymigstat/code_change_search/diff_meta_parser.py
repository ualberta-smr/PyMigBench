from dataclasses import dataclass


def _part_hunk_header_part(part: str):
    parts = [int(n) for n in part[1:].split(",")]
    if len(parts) == 1:
        parts.append(1)
    return parts


def _parse_hunk_header(line: str):
    removed, added = line.split("@@")[1].strip().split(" ")
    return _part_hunk_header_part(removed) + _part_hunk_header_part(added)


@dataclass
class DiffFile:
    path: str
    removed_lines: list[int]
    added_lines: list[int]


class DiffMetaParser:
    # This class is too stateful
    def __init__(self, diff: str):
        self._lines = Lines(diff.splitlines(keepends=False))

    def parse(self):
        files = []
        while self._lines.has_more():
            files.append(self._parse_file())

        return files

    def _parse_file(self) -> DiffFile:
        self._lines.move_until("---")

        old_name = self._lines.current()[6:].strip()
        self._lines.move_next()
        new_name = self._lines.current()[6:].strip()
        removed_lines = []
        added_lines = []
        while self._lines.has_more() and not self._lines.startswith("diff --git"):
            r, a = self._parse_hunk()
            removed_lines += r
            added_lines += a

        return DiffFile(new_name or old_name, removed_lines, added_lines)

    def _parse_hunk(self):
        self._lines.move_until("@@")
        header = _parse_hunk_header(self._lines.current())
        self._lines.move_next()

        added = []
        removed = []
        old_line = header[0]
        new_line = header[2]
        while self._lines.has_more() and not self._lines.startswith("diff --git") and not self._lines.startswith("@@"):
            if self._lines.startswith("-"):
                removed.append(old_line)
                old_line += 1
            elif self._lines.startswith("+"):
                added.append(new_line)
                new_line += 1
            else:
                old_line += 1
                new_line += 1
            self._lines.move_next()

        return removed, added


class Lines:
    def __init__(self, lines: list[str]):
        self._lines = lines
        self._current = 0

    def has_more(self):
        return self._current < len(self._lines)

    def current(self):
        return self._lines[self._current]

    def move_next(self):
        self._current += 1

    def move_until(self, line_prefix: str):
        while not self.current().startswith(line_prefix):
            self.move_next()

    def startswith(self, line_prefix: str):
        return self.current().startswith(line_prefix)
