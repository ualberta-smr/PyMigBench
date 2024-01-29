from latex.core import Node, BeginEndNode


class Tabular(BeginEndNode):
    _current_row: list[Node]

    def __init__(self, indentation: int, alignments: str):
        super().__init__(indentation, "tabular", mandatory_args=[alignments])
        self._indentation = indentation
        self._start_row()

    def add_cell(self, cell: Node):
        self._current_row.append(cell)
        return self

    def _start_row(self):
        self._current_row = []

    def end_row(self):
        self.start_line(self._indentation + 1)
        for i, cell in enumerate(self._current_row):
            if i > 0:
                self.add_text(" & ")
            self.add_child(cell)
        self.add_text(" \\\\ ")
        self._start_row()
        return self

