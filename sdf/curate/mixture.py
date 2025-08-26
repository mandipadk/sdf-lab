from __future__ import annotations
import random
from typing import Any, Dict, List

def curate_mixture(items: List[Dict[str, Any]], size: int, quotas: Dict[str, int]) -> List[Dict[str, Any]]:
    # Sort by score desc, then sample with quotas per domain (meta.domain)
    items2 = sorted(items, key=lambda x: float(x.get("score", 0.0)), reverse=True)
    by_dom = {}
    for it in items2:
        dom = (it.get("meta",{}).get("domain") or "general")
        by_dom.setdefault(dom, []).append(it)
    out = []
    # Satisfy quotas first
    for dom, q in (quotas or {}).items():
        bucket = by_dom.get(dom, [])
        out.extend(bucket[:q])
        by_dom[dom] = bucket[q:]
    # Fill remaining
    remaining = size - len(out)
    if remaining > 0:
        pool = [it for bucket in by_dom.values() for it in bucket]
        out.extend(pool[:remaining])
    return out[:size]
