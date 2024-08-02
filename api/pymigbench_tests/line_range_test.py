import pytest

from pymigbench.line_range import LineRange


def test_parsing_empty_range():
    lr = LineRange("")
    assert lr.lines == set()


def test_parsing_single_range():
    lr = LineRange("1-5")
    assert lr.lines == {1, 2, 3, 4, 5}


def test_multiple_ranges():
    lr = LineRange("1-5,7-10, 12")
    assert lr.lines == {1, 2, 3, 4, 5, 7, 8, 9, 10, 12}


def test_equality():
    assert LineRange("") == LineRange("")
    assert LineRange("1-5") == LineRange("1-5")
    assert LineRange("1-5,7-10, 12") == LineRange("1-5,7-10, 12")
    assert LineRange("1-5,7-10, 12") != 1
    assert LineRange("1-5,7-10, 12") != LineRange("1-5,7-10, 13")


def test_intersects_range():
    lr = LineRange("3-5,7-10, 12")
    assert lr.intersects_range(3, 5), "a full subpart"
    assert lr.intersects_range(7, 10), "a full subpart"
    assert lr.intersects_range(12), "upper boundary"
    assert lr.intersects_range(3, 6), "overlap and go beyond"
    assert lr.intersects_range(3, 12), "full cover"
    assert lr.intersects_range(1, 15), "superset"

    assert not lr.intersects_range(1, 2), "should not intersect"
    assert not lr.intersects_range(6), "should not intersect"
    assert not lr.intersects_range(13, 15), "should not intersect"


def test_intersects():
    lr = LineRange("3-5,7-10, 12")
    assert lr.intersects(LineRange("3-5,7-10, 12")), "same"
    assert lr.intersects(LineRange("3-5,7-10, 13")), "different last"
    assert lr.intersects(LineRange("3-5,7-10")), "different last"
    assert lr.intersects(LineRange("1-5,7-10, 11")), "different last"


def test_intersects_or_adjacent():
    assert not LineRange("3-5,7-10, 12").intersects_or_adjacent(LineRange("3-5,7-10, 12")), "multi range"
    assert not LineRange("3-5,7-10, 12").intersects_or_adjacent(LineRange("3-5")), "multi range"
    assert not LineRange("3-5").intersects_or_adjacent(LineRange("3-5,7-10, 12")), "multi range"
    assert LineRange("3-5").intersects_or_adjacent(LineRange("3-5")), "same range"
    assert LineRange("3-5").intersects_or_adjacent(LineRange("6-10")), "intersects"
    assert LineRange("3-5").intersects_or_adjacent(LineRange("6-10")), "adjacent right"
    assert LineRange("6-10").intersects_or_adjacent(LineRange("3-5")), "adjacent left"

    assert not LineRange("3-5").intersects_or_adjacent(LineRange("7-10")), "not adjacent"


def test_from_bound():
    assert LineRange.from_bounds(1, 1) == LineRange("1")
    assert LineRange.from_bounds(1, 5) == LineRange("1-5")
    with pytest.raises(ValueError):
        LineRange.from_bounds(5, 1)


def test_from_merge():
    lr_disjoint = LineRange.from_merge([LineRange("1-5"), LineRange("7-10"), LineRange("12")])
    assert lr_disjoint == LineRange("1-5,7-10,12")

    lr_overlap = LineRange.from_merge([LineRange("1-5"), LineRange("3-10"), LineRange("12")])
    assert lr_overlap == LineRange("1-10,12")

    lr_same = LineRange.from_merge([LineRange("1-5"), LineRange("1-5"), LineRange("1-5")])
    assert lr_same == LineRange("1-5")


def test_from_values():
    assert LineRange.from_values([5, 3, 1, 2, 4]) == LineRange("1-5")
    assert LineRange.from_values([1]) == LineRange("1")
    assert LineRange.from_values([]) == LineRange("")
