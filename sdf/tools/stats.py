from __future__ import annotations
import argparse, json, sys
from typing import Any, Dict, List
from sdf.generate.templates import generate_templates
from sdf.generate.code_math import generate_code_math
from sdf.generate.tools import generate_tools

def write_jsonl(path: str, rows):
    with open(path,'w',encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False)+"\n")

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--demo', action='store_true')
    ap.add_argument('--with_tools', action='store_true')
    ap.add_argument('--out', default='-')
    ap.add_argument('--n', type=int, default=200)
    ap.add_argument('--seed', type=int, default=42)
    args=ap.parse_args()
    items = generate_templates(args.n//3, args.seed) + generate_code_math(args.n//3, args.seed+1)
    if args.with_tools:
        items += generate_tools(args.n - len(items), args.seed+2)
    if args.out == '-' or args.out == '/dev/stdout':
        for r in items:
            print(json.dumps(r, ensure_ascii=False))
    else:
        write_jsonl(args.out, items)
        print(args.out)
