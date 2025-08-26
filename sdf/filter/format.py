from __future__ import annotations
from typing import Any, Dict, List, Tuple

def filter_format(items: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    min_len = int(cfg.get("min_output", 0))
    max_len = int(cfg.get("max_output", 5000))
    kept, dropped = [], []
    for it in items:
        out = it.get("output","")
        if len(out) < min_len or len(out) > max_len:
            dropped.append({"item": it, "reason":"format"})
        else:
            kept.append(it)
    return kept, dropped
