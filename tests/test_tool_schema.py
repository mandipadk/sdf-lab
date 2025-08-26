from sdf.generate.tools import generate_tools
from sdf.filter.schema import filter_schema

def test_tool_rows_validate():
    items = generate_tools(10, seed=1)
    kept, dropped = filter_schema(items, {})
    assert len(kept) == 10
    assert len(dropped) == 0
