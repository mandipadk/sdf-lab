from __future__ import annotations
from typing import List

def minmax(scores: List[float]) -> List[float]:
    if not scores: return []
    lo, hi = min(scores), max(scores)
    if hi - lo < 1e-6: return [0.5 for _ in scores]
    return [(s - lo)/(hi - lo) for s in scores]
