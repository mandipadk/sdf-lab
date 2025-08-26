# Synthetic Data Factory (SDF)

**Generate → filter → dedupe → score → curate** synthetic instruction data (SFT/DPO/tool-calls).
Run locally with Docker or on Colab.
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mandipadk/sdf-lab/blob/main/SDF_Colab.ipynb)

## Quickstart (local)

```bash
pip install -e .[dev]
uvicorn server:app --host 0.0.0.0 --port 9000
```

### CLI: demo pipeline
```bash
python -m sdf.tools.stats --demo | tee /tmp/sdf_raw.jsonl
python -m sdf.tools.mix_preview --in /tmp/sdf_raw.jsonl --out /tmp/sdf_curated.jsonl --pipeline filter,exact_dedupe,score,curate --size 200
```

### Train tiny SFT
```bash
python -m sdf.train.sft_trainer --model_id TinyLlama/TinyLlama-1.1B-Chat-v1.0 --data /tmp/sdf_curated.jsonl --out_dir out/sft_adapter --epochs 1 --batch_size 4 --lr 5e-5 --max_seq 512
```

## Server endpoints
- `POST /v1/generate` {kind, n, seed, params}
- `POST /v1/filter` {items, config}
- `POST /v1/dedupe` {items, method, threshold}
- `POST /v1/score` {items}
- `POST /v1/curate` {items, size, quotas?}

## Data schemas
SFT row:
```json
{"instruction": "Write an email...", "input": "", "output": "Dear...", "meta": {"domain":"email","template":"email_v1"}}
```
DPO row:
```json
{"prompt": "Explain X", "chosen": "...", "rejected": "...", "meta": {"source":"synthetic"}}
```
Tool-calling row:
```json
{"prompt":"Get weather", "tools":[{"name":"get_weather","schema":{}}], "assistant_call":{"name":"get_weather","arguments":{}}, "assistant_result":{}, "assistant_response": "...", "meta": {"valid": true}}
```

### Rolling features
- Tool-calling generator (`sdf/generate/tools.py`) + JSON Schema validation in `filter/schema.py`.
- Semantic dedupe (`sdf/dedupe/semantic.py`) using BERT CLS embeddings.
- DPO builder CLI: `python -m sdf.tools.dpo_builder --in curated.jsonl --out dpo.jsonl` (group by instruction).
- `tools/stats.py --with_tools` to include tool-calling rows in demo data.
