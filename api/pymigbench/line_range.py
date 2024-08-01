from typing import Iterable


class LineRange:
    def __init__(self, expression: str = None):
        self.expression = expression or ""
        values = set()
        if expression:
            parts = expression.split(",")  # 1,5-6 -> [1, 5-6]
            for part in parts:
                if "-" in part:
                    start, end = part.split("-")
                    values.update(range(int(start), int(end) + 1))
                else:
                    values.add(int(part))

        self.lines = frozenset(values)
        self.min = min(self.lines) if self.lines else 0
        self.max = max(self.lines) if self.lines else 0
        self.is_contiguous = (len(self.lines) == 0) or (len(self.lines) == self.max - self.min + 1)

    def intersects_range(self, start: int, end: int = -1):
        if end == -1:
            end = start
        for i in range(start, end + 1):
            if i in self.lines:
                return True
        return False

    def intersects(self, other: 'LineRange'):
        return bool(self.lines.intersection(other.lines))

    def intersects_or_adjacent(self, other: 'LineRange'):
        if not self.is_contiguous or not other.is_contiguous:
            return False
        if self.max + 1 == other.min:  # 1-5,6-10
            return True
        if other.max + 1 == self.min:  # 6-10,1-5
            return True
        if self.intersects(other):  # 1-5,3-10
            return True
        return False

    def __eq__(self, other):
        if not isinstance(other, LineRange):
            return False
        return self.lines == other.lines

    def __hash__(self):
        return hash(self.lines)

    def __str__(self):
        return str(self.expression)

    def __repr__(self):
        return str(self.expression) + " = " + str(sorted(self.lines))

    def __len__(self):
        return len(self.lines)

    @staticmethod
    def from_bounds(start: int, end: int):
        if start > end:
            raise ValueError(f"start should be less than or equal to end. found {start} > {end}")
        if start == end:
            return LineRange(str(start))
        return LineRange(f"{start}-{end}")

    @staticmethod
    def from_merge(ranges: Iterable['LineRange']):
        return LineRange.from_values(ln for lr in ranges for ln in lr.lines)

    @staticmethod
    def from_values(values: Iterable[int]):
        if not values:
            return LineRange()
        all_lines: list[int] = sorted(values)
        ranges = []
        start = all_lines[0]
        for i in range(1, len(all_lines)):
            if all_lines[i] != all_lines[i - 1] + 1:
                ranges.append(LineRange.from_bounds(start, all_lines[i - 1]))
                start = all_lines[i]

        ranges.append(LineRange.from_bounds(start, all_lines[-1]))
        if len(ranges) == 1:
            return ranges[0]

        expression = ",".join(r.expression for r in ranges if r.expression)
        return LineRange(expression)
