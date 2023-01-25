from core.Arguments import Arguments
from pymigbench import run_query


def test_detail_1():
    args = Arguments(query="detail", data_type="mg", filters=["target=aiohttp"], output_format="json")
    run_query(args)


def test_count_1():
    args = Arguments(query="count", data_type="mg", filters=["target=aiohttp"], output_format="json")
    run_query(args)


def test_summary():
    args = Arguments(query="summary", output_format="yaml")
    run_query(args)


def test__no_data_types__should_throw_error():
    args = Arguments(query="detail")
    run_query(args)
