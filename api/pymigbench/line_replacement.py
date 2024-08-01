from pymigbench.line_range import LineRange


class LineReplacement:
    @staticmethod
    def from_expression(expression: str):
        if not expression or not expression.strip():
            raise ValueError("empty expression")
        if ":" not in expression:
            raise ValueError(f"Invalid expression: {expression}. Must have ':' separator.")
        parts = expression.split(":")
        if len(parts) != 2:
            raise ValueError(f"Invalid expression: {expression}. Must have exactly one ':' separator.")
        if not parts[0] and not parts[1]:
            raise ValueError(f"Invalid expression: {expression}. Both source and target cannot be empty.")
        src = LineRange(parts[0])
        tgt = LineRange(parts[1])
        return LineReplacement(src, tgt, expression)

    def __init__(self, src: LineRange, tgt: LineRange, expression: str):
        self.source = src
        self.target = tgt
        self.expression = expression

    def __str__(self):
        return self.expression

    def __repr__(self):
        return self.expression

    def __eq__(self, other):
        if not isinstance(other, LineReplacement):
            return False
        return self.source == other.source and self.target == other.target
