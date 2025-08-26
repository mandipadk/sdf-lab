from __future__ import annotations
import re
from typing import Any, Dict, List, Tuple

RE_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
RE_PHONE = re.compile(r"\b(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}\b")
RE_SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
RE_CREDIT = re.compile(r"\b(?:\d[ -]*?){13,19}\b")

def _scan(text: str) -> List[str]:
    hits = []
    for r in [RE_EMAIL, RE_PHONE, RE_SSN, RE_CREDIT]:
        hits += [m.group(0) for m in r.finditer(text or "")]
    return hits

def filter_pii(items: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    redact = bool(cfg.get("redact", True))
    kept, dropped = [], []
    for it in items:
        txt = (it.get("instruction","") + " " + it.get("input","") + " " + it.get("output",""))
        hits = _scan(txt)
        if not hits:
            kept.append(it); continue
        if redact:
            rep = it.copy()
            for h in hits:
                rep["instruction"] = rep["instruction"].replace(h, "[REDACTED]")
                rep["input"] = rep["input"].replace(h, "[REDACTED]")
                rep["output"] = rep["output"].replace(h, "[REDACTED]")
            kept.append(rep)
        else:
            dropped.append({"item": it, "reason": "pii", "hits": hits})
    return kept, dropped
