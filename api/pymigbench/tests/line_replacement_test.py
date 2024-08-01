# write tests for line_replacement.py
import pytest

from pymigbench.line_replacement import LineReplacement
from pymigbench.line_range import LineRange

from_expression = LineReplacement.from_expression


def test_from_expression():
    with pytest.raises(ValueError):
        from_expression("")

    with pytest.raises(ValueError):
        from_expression("   ")

    with pytest.raises(ValueError):
        from_expression("1-5")

    with pytest.raises(ValueError):
        from_expression(":")

    with pytest.raises(ValueError):
        from_expression("1:2:")

    lr = from_expression("1-5:")
    assert lr.source == LineRange("1-5")
    assert lr.target == LineRange("")

    lr = from_expression(":6")
    assert lr.source == LineRange("")
    assert lr.target == LineRange("6")

    lr = from_expression("1-5:6-10")
    assert lr.source == LineRange("1-5")
    assert lr.target == LineRange("6-10")


def test_equality():
    assert from_expression("1-5:1-3") == from_expression("1-5:1-2,3")
    assert from_expression("1-5:1-3") != from_expression("1-5:1-2,4")
    assert from_expression("1-5:1-3") != 1
