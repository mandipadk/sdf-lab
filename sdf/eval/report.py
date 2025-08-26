from __future__ import annotations
import argparse, json, collections

def build_report(path: str) -> str:
    n=0; domains=collections.Counter()
    total_len=0; scores=[]
    with open(path,'r',encoding='utf-8') as f:
        for line in f:
            j=json.loads(line); n+=1
            dom = (j.get('meta',{}).get('domain') or 'general')
            domains[dom]+=1
            total_len += len(j.get('output',''))
            if 'score' in j: scores.append(float(j['score']))
    avg_len = total_len / max(1,n)
    avg_score = sum(scores)/max(1,len(scores))
    out = ["# SDF Report", "", f"Total items: {n}", f"Avg output length: {avg_len:.1f}", f"Avg score: {avg_score:.3f}", "", "## Domain distribution:"]
    for d,c in domains.most_common():
        out.append(f"- {d}: {c}")
    return "\n".join(out)

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--data', required=True)
    ap.add_argument('--out', required=True)
    args=ap.parse_args()
    rep = build_report(args.data)
    with open(args.out,'w',encoding='utf-8') as f: f.write(rep)
    print(args.out)
