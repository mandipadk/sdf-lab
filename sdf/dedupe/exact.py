from __future__ import annotations
from typing import Any, Dict, List

def _key(it: Dict[str, Any]) -> str:
    return (it.get("instruction","").strip().lower() + "\n" + it.get("input","").strip().lower() + "\n" + it.get("output","").strip().lower())

def dedupe_exact(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for it in items:
        k = _key(it)
        if k in seen:
            continue
        seen.add(k)
        out.append(it)
    return out
