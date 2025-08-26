from __future__ import annotations
import random, re
from typing import Any, Dict, List, Tuple

_WORD = re.compile(r"[A-Za-z0-9_]+")

def _shingles(text: str, k: int = 5) -> set:
    toks = _WORD.findall(text.lower())
    return set([" ".join(toks[i:i+k]) for i in range(max(0, len(toks)-k+1))])

def _jaccard(a: set, b: set) -> float:
    if not a and not b: return 1.0
    return len(a & b) / max(1, len(a | b))

def dedupe_minhash(items: List[Dict[str, Any]], threshold: float = 0.9) -> List[Dict[str, Any]]:
    # Simple O(n^2) with shingles + jaccard for modest sizes (sufficient for batches)
    # For large N, replace with real MinHash+LSH.
    reps = []
    seen = [False] * len(items)
    for i, it in enumerate(items):
        if seen[i]: continue
        a = _shingles(it.get("instruction","") + " " + it.get("output",""))
        reps.append(it)
        for j in range(i+1, len(items)):
            if seen[j]: continue
            b = _shingles(items[j].get("instruction","") + " " + items[j].get("output",""))
            if _jaccard(a,b) >= threshold:
                seen[j] = True
    return reps
