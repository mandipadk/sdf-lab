from __future__ import annotations
import argparse, json, math, os
from typing import List, Dict, Any
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM, get_cosine_schedule_with_warmup

try:
    from peft import LoraConfig, get_peft_model
    _PEFT=True
except Exception:
    _PEFT=False

class SFTJsonl(Dataset):
    def __init__(self, path: str):
        self.rows=[]
        with open(path,'r',encoding='utf-8') as f:
            for line in f:
                j=json.loads(line)
                if 'instruction' in j and 'output' in j:
                    self.rows.append(j)
        if not self.rows: raise ValueError('empty dataset')
    def __len__(self): return len(self.rows)
    def __getitem__(self, i): return self.rows[i]

def collate(batch, tok, max_seq: int):
    texts = [f"### Instruction:\n{b['instruction']}\n\n### Response:\n{b['output']}" for b in batch]
    enc = tok(texts, padding=True, truncation=True, max_length=max_seq, return_tensors='pt')
    labels = enc['input_ids'].clone()
    labels[labels == tok.pad_token_id] = -100
    enc['labels'] = labels
    return enc

def train(args):
    tok = AutoTokenizer.from_pretrained(args.model_id)
    if tok.pad_token is None: tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.model_id, torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32)
    if args.lora_r>0:
        if not _PEFT: raise RuntimeError('peft not installed')
        cfg = LoraConfig(r=args.lora_r, lora_alpha=args.lora_alpha, lora_dropout=args.lora_dropout, bias='none', task_type='CAUSAL_LM', target_modules=args.lora_target)
        model = get_peft_model(model, cfg)
    else:
        for p in model.parameters(): p.requires_grad_(True)
    model.train()

    ds = SFTJsonl(args.data)
    dl = DataLoader(ds, batch_size=args.batch_size, shuffle=True, collate_fn=lambda b: collate(b, tok, args.max_seq))

    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=args.lr)
    steps = max(1, len(dl)*args.epochs)
    sch = get_cosine_schedule_with_warmup(opt, int(0.1*steps), steps)
    step=0
    for ep in range(args.epochs):
        for batch in dl:
            batch = {k:v.to(model.device) for k,v in batch.items()}
            out = model(**batch)
            loss = out.loss
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); sch.step(); opt.zero_grad()
            if step % args.log_every == 0:
                print(f"epoch {ep} step {step} loss {loss.item():.4f}")
            step += 1
    os.makedirs(args.out_dir, exist_ok=True)
    model.save_pretrained(args.out_dir); tok.save_pretrained(args.out_dir)
    print(f"Saved to {args.out_dir}")

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--model_id', required=True)
    ap.add_argument('--data', required=True)
    ap.add_argument('--out_dir', required=True)
    ap.add_argument('--epochs', type=int, default=1)
    ap.add_argument('--batch_size', type=int, default=4)
    ap.add_argument('--lr', type=float, default=5e-5)
    ap.add_argument('--max_seq', type=int, default=512)
    ap.add_argument('--log_every', type=int, default=10)
    ap.add_argument('--lora_r', type=int, default=16)
    ap.add_argument('--lora_alpha', type=int, default=32)
    ap.add_argument('--lora_dropout', type=float, default=0.05)
    ap.add_argument('--lora_target', nargs='+', default=['q_proj','k_proj','v_proj','o_proj'])
    args=ap.parse_args(); train(args)
