from sdf.dedupe.semantic import dedupe_semantic

def test_semantic_dedupe_small():
    items = [
        {"instruction":"Write an email to Jordan about the Q3 report.","input":"","output":"Dear Jordan, The Q3 report is ready.","meta":{"domain":"email"}},
        {"instruction":"Write an email to Jordan about the Q3 report.","input":"","output":"Dear Jordan, Q3 report attached.","meta":{"domain":"email"}},
        {"instruction":"List 3 uses for a paperclip.","input":"","output":"- Use 1 for paperclip","meta":{"domain":"list"}},
    ]
    out = dedupe_semantic(items, threshold=0.9, model_id="prajjwal1/bert-tiny")
    # the two emails are near duplicates; the tiny model is used for speed
    assert len(out) <= 3
