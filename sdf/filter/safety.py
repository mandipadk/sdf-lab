from __future__ import annotations
from typing import Any, Dict, List, Tuple

JB = ["ignore previous instructions", "bypass safety", "developer mode"]
RISKY = ["make a bomb", "how to make meth", "drug lab", "harm someone"]

def filter_safety(items: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    threshold = float(cfg.get("block_threshold", 0.8))
    kept, dropped = [], []
    for it in items:
        text = (it.get("instruction","") + " " + it.get("output","")).lower()
        risk = 0.0
        if any(p in text for p in JB):
            risk = max(risk, 0.7)
        if any(p in text for p in RISKY):
            risk = max(risk, 0.9)
        if risk >= threshold:
            dropped.append({"item": it, "reason":"safety", "risk": risk})
        else:
            kept.append(it)
    return kept, dropped
