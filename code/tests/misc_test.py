from core.Arguments import Arguments
from pymigbench import run_query


def test_detail_1():
    args = Arguments(query="detail", data_type="mg", filters=["target=aiohttp"], output_format="json")
    run_query(args)
