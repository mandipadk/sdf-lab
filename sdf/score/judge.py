from __future__ import annotations
from typing import Any, Dict, List
from sdf.score.verifiers import verify_math, verify_code

def _heuristic(item: Dict[str, Any]) -> float:
    # Reward structure, formatting, and brevity
    out = item.get("output","")
    bullets = out.count("\n- ")
    paras = out.count("\n\n")
    length_pen = 0.0 if len(out) < 200 else -0.1
    return max(0.1, min(1.0, 0.5 + 0.1*bullets + 0.05*paras + length_pen))

def score_items(items: List[Dict[str, Any]], cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    out = []
    for it in items:
        domain = (it.get("meta", {}).get("domain") or "").lower()
        s = 0.0
        if domain == "math":
            s = verify_math(it)["score"]
        elif domain == "code":
            s = verify_code(it)["score"]
        else:
            s = _heuristic(it)
        it2 = dict(it)
        it2["score"] = float(s)
        out.append(it2)
    return out
