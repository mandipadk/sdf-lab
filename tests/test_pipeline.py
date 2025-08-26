import json, tempfile, os
from sdf.generate.templates import generate_templates
from sdf.generate.code_math import generate_code_math
from sdf.filter.schema import filter_schema
from sdf.dedupe.exact import dedupe_exact
from sdf.score.judge import score_items
from sdf.curate.mixture import curate_mixture

def test_end_to_end_small():
    items = generate_templates(10, 1) + generate_code_math(10, 2)
    kept, dropped = filter_schema(items, {})
    assert len(kept) > 0
    dd = dedupe_exact(kept)
    sc = score_items(dd, {})
    cur = curate_mixture(sc, 10, {})
    assert len(cur) == 10
    for it in cur:
        assert "instruction" in it and "output" in it
