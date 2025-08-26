from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from sdf.generate.templates import generate_templates
from sdf.generate.code_math import generate_code_math
from sdf.generate.tools import generate_tools
from sdf.filter.schema import filter_schema
from sdf.filter.pii import filter_pii
from sdf.filter.safety import filter_safety
from sdf.filter.format import filter_format
from sdf.dedupe.exact import dedupe_exact
from sdf.dedupe.minhash import dedupe_minhash
from sdf.dedupe.semantic import dedupe_semantic
from sdf.score.judge import score_items
from sdf.curate.mixture import curate_mixture

app = FastAPI(title="SDF", version="0.1.0")

class GenReq(BaseModel):
    kind: str = "templates"  # templates | code_math
    n: int = 50
    seed: int = 42
    params: Dict[str, Any] = {}

class ItemsReq(BaseModel):
    items: List[Dict[str, Any]]
    config: Dict[str, Any] = {}

class DedupeReq(BaseModel):
    items: List[Dict[str, Any]]
    method: str = "exact"  # exact|minhash
    threshold: float = 0.9

class CurateReq(BaseModel):
    items: List[Dict[str, Any]]
    size: int = 200
    quotas: Optional[Dict[str, int]] = None  # domain -> quota

@app.post("/v1/generate")
def generate(req: GenReq):
    if req.kind == "templates":
        items = generate_templates(req.n, req.seed, req.params or {})
    elif req.kind == "code_math":
        items = generate_code_math(req.n, req.seed, req.params or {})
    elif req.kind == "tools":
        items = generate_tools(req.n, req.seed, req.params or {})
    else:
        return {"error": f"unknown kind: {req.kind}"}
    return {"count": len(items), "items": items}

@app.post("/v1/filter")
def filter_items(req: ItemsReq):
    items = req.items
    cfg = req.config or {}
    kept, dropped = items, []
    # apply filters in a simple order
    kept, dr = filter_schema(kept, cfg.get("schema", {})); dropped += dr
    kept, dr = filter_pii(kept, cfg.get("pii", {})); dropped += dr
    kept, dr = filter_safety(kept, cfg.get("safety", {})); dropped += dr
    kept, dr = filter_format(kept, cfg.get("format", {})); dropped += dr
    return {"kept": kept, "dropped": dropped, "kept_count": len(kept), "dropped_count": len(dropped)}

@app.post("/v1/dedupe")
def dedupe(req: DedupeReq):
    if req.method == "exact":
        items = dedupe_exact(req.items)
    elif req.method == "minhash":
        items = dedupe_minhash(req.items, threshold=req.threshold)
    elif req.method == "semantic":
        items = dedupe_semantic(req.items, threshold=req.threshold)
    else:
        return {"error": f"unknown method: {req.method}"}
    return {"count": len(items), "items": items}

@app.post("/v1/score")
def score(req: ItemsReq):
    scored = score_items(req.items, req.config or {})
    return {"count": len(scored), "items": scored}

@app.post("/v1/curate")
def curate(req: CurateReq):
    out = curate_mixture(req.items, req.size, req.quotas or {})
    return {"count": len(out), "items": out}
