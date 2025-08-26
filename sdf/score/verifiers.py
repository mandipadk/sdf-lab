from __future__ import annotations
import re, json, textwrap, builtins
from typing import Any, Dict

def verify_math(item: Dict[str, Any]) -> Dict[str, Any]:
    # Extract last integer in output and compare to meta.answer if present
    out = item.get("output","")
    meta = item.get("meta", {})
    m = re.findall(r"-?\d+", out)
    if not m:
        return {"score": 0.0, "details": {"reason": "no_number"}}
    pred = int(m[-1])
    if "answer" in meta:
        ok = (pred == int(meta["answer"]))
        return {"score": 1.0 if ok else 0.0, "details": {"pred": pred, "gold": meta["answer"]}}
    return {"score": 0.5, "details": {"pred": pred}}

def verify_code(item: Dict[str, Any]) -> Dict[str, Any]:
    # Extract python block and run simple tests from meta.tests
    out = item.get("output","")
    meta = item.get("meta", {})
    tests = meta.get("tests", [])
    m = re.search(r"```python\n([\s\S]*?)\n```", out)
    if not m:
        return {"score": 0.0, "details": {"reason": "no_code"}}
    code = textwrap.dedent(m.group(1))
    g, l = {"__builtins__": {"range": range, "len": len, "sum": sum, "min": min, "max": max, "int": int, "float": float}}, {}
    try:
        exec(code, g, l)
    except Exception as e:
        return {"score": 0.0, "details": {"error": str(e)}}
    passes = 0
    for t in tests:
        args = t.get("args", [])
        exp = t.get("expected")
        try:
            res = l.get("add", g.get("add"))(*args)
            if res == exp: passes += 1
        except Exception as e:
            continue
    total = max(1, len(tests))
    return {"score": passes/total, "details": {"passes": passes, "total": total}}
