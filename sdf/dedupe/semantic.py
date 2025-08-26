from __future__ import annotations
from typing import Any, Dict, List
import torch
from transformers import AutoTokenizer, AutoModel

@torch.no_grad()
def _embed_texts(texts: List[str], model_id: str = "bert-base-uncased"):
    tok = AutoTokenizer.from_pretrained(model_id)
    model = AutoModel.from_pretrained(model_id)
    model.eval()
    embs = []
    bs = 16
    for i in range(0, len(texts), bs):
        batch = texts[i:i+bs]
        enc = tok(batch, padding=True, truncation=True, max_length=256, return_tensors='pt')
        out = model(**enc)
        # CLS pooling
        cls = out.last_hidden_state[:,0,:]
        # L2 normalize
        cls = torch.nn.functional.normalize(cls, p=2, dim=1)
        embs.append(cls)
    return torch.cat(embs, dim=0)

@torch.no_grad()
def dedupe_semantic(items: List[Dict[str, Any]], threshold: float = 0.92, model_id: str = "bert-base-uncased") -> List[Dict[str, Any]]:
    if len(items) <= 1:
        return items
    texts = [(it.get('instruction') or it.get('prompt') or '') + '\n' + (it.get('output') or it.get('assistant_response') or '') for it in items]
    embs = _embed_texts(texts, model_id=model_id)
    keep = [True]*len(items)
    for i in range(len(items)):
        if not keep[i]:
            continue
        vi = embs[i:i+1]
        sims = (embs @ vi.T).squeeze(-1)
        for j in range(i+1, len(items)):
            if keep[j] and sims[j] >= threshold:
                keep[j] = False
    return [it for it,k in zip(items, keep) if k]
