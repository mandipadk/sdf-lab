import json, tempfile, os
from sdf.tools.dpo_builder import build_pairs

def test_dpo_from_duplicates():
    # two rows with same instruction, different outputs and scores
    items = [
        {"instruction":"Say hi.","input":"","output":"Hello!","meta":{"domain":"general"},"score":0.9},
        {"instruction":"Say hi.","input":"","output":"Hi.","meta":{"domain":"general"},"score":0.2},
        {"instruction":"Say hi.","input":"","output":"Hey there!","meta":{"domain":"general"},"score":0.5}
    ]
    pairs = build_pairs(items, group_key='instruction', k_pairs_per_group=1)
    assert len(pairs) == 1
    p = pairs[0]
    assert p["prompt"] == "Say hi."
    assert "chosen" in p and "rejected" in p and p["chosen"] != p["rejected"]
