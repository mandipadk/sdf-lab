from __future__ import annotations
import argparse, json, sys
from typing import Any, Dict, List
from sdf.filter.schema import filter_schema
from sdf.filter.pii import filter_pii
from sdf.filter.safety import filter_safety
from sdf.filter.format import filter_format
from sdf.dedupe.exact import dedupe_exact
from sdf.dedupe.minhash import dedupe_minhash
from sdf.dedupe.semantic import dedupe_semantic
from sdf.score.judge import score_items
from sdf.curate.mixture import curate_mixture

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    out=[]
    with open(path,'r',encoding='utf-8') as f:
        for line in f:
            if line.strip(): out.append(json.loads(line))
    return out

def write_jsonl(path: str, items: List[Dict[str, Any]]):
    with open(path,'w',encoding='utf-8') as f:
        for it in items: f.write(json.dumps(it, ensure_ascii=False)+"\n")

def run_pipeline(items: List[Dict[str, Any]], pipeline: str, size: int) -> List[Dict[str, Any]]:
    steps = [s.strip() for s in pipeline.split(',') if s.strip()]
    kept = items
    for s in steps:
        if s == 'filter':
            kept, dr = filter_schema(kept, {}); kept, dr2 = filter_pii(kept, {}); kept, dr3 = filter_safety(kept, {}); kept, dr4 = filter_format(kept, {})
        elif s == 'exact_dedupe':
            kept = dedupe_exact(kept)
        elif s == 'minhash_dedupe':
            kept = dedupe_minhash(kept, threshold=0.9)
        elif s == 'score':
            kept = score_items(kept, {})
        elif s == 'semantic_dedupe':
            kept = dedupe_semantic(kept, threshold=0.92)
        elif s == 'curate':
            kept = curate_mixture(kept, size, {})
    return kept

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', required=True)
    ap.add_argument('--out', dest='out', required=True)
    ap.add_argument('--pipeline', default='filter,exact_dedupe,score,curate')
    ap.add_argument('--size', type=int, default=200)
    args=ap.parse_args()
    items = load_jsonl(args.inp)
    res = run_pipeline(items, args.pipeline, args.size)
    write_jsonl(args.out, res)
    print(f"Wrote {len(res)} rows to {args.out}")
