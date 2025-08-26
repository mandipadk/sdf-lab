from __future__ import annotations
import argparse, json, collections, random
from typing import Any, Dict, List


def load_jsonl(p: str):
    out=[]
    with open(p,'r',encoding='utf-8') as f:
        for ln in f:
            if ln.strip(): out.append(json.loads(ln))
    return out

def write_jsonl(p: str, rows: List[Dict[str, Any]]):
    with open(p,'w',encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False)+"\n")


def build_pairs(items: List[Dict[str, Any]], group_key: str = 'instruction', k_pairs_per_group: int = 1) -> List[Dict[str, Any]]:
    # group by instruction (or provided key)
    buckets = collections.defaultdict(list)
    for it in items:
        g = it.get(group_key)
        if g is not None:
            buckets[g].append(it)
    out=[]
    for g,rows in buckets.items():
        if len(rows) < 2: continue
        # order by 'score' if present, else random
        rows = sorted(rows, key=lambda r: float(r.get('score', 0.0)), reverse=True)
        for _ in range(min(k_pairs_per_group, len(rows)//2)):
            chosen = rows[0]
            rejected = rows[-1]
            out.append({
                'prompt': g,
                'chosen': chosen.get('output') or chosen.get('assistant_response') or '',
                'rejected': rejected.get('output') or rejected.get('assistant_response') or '',
                'meta': {'source': 'synthetic', 'group_key': group_key}
            })
            # remove used extremes to allow another pair
            rows = rows[1:-1]
            if len(rows) < 2: break
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', required=True)
    ap.add_argument('--out', dest='out', required=True)
    ap.add_argument('--group_key', default='instruction')
    ap.add_argument('--pairs_per_group', type=int, default=1)
    args=ap.parse_args()
    items = load_jsonl(args.inp)
    pairs = build_pairs(items, group_key=args.group_key, k_pairs_per_group=args.pairs_per_group)
    write_jsonl(args.out, pairs)
    print(f"Wrote {len(pairs)} DPO rows to {args.out}")
