from __future__ import annotations
import random, math
from typing import Dict, Any, List

def _math_item():
    a = random.randint(1, 50)
    b = random.randint(1, 50)
    op = random.choice(["+", "-", "*"])
    instr = f"Compute {a} {op} {b}."
    ans = eval(f"{a}{op}{b}")
    return {"instruction": instr, "input": "", "output": f"The answer is {ans}.",
            "meta": {"domain":"math","a":a,"b":b,"op":op,"answer": ans}}

def _code_item():
    a = random.randint(-5, 5)
    b = random.randint(-5, 5)
    instr = "Write a Python function add(a, b) that returns a+b."
    # We also include simple tests in meta
    tests = [{"args":[1,2],"expected":3}, {"args":[a,b],"expected":a+b}]
    out = "```python\ndef add(a, b):\n    return a + b\n```"
    return {"instruction": instr, "input": "", "output": out,
            "meta": {"domain":"code","tests": tests}}

def generate_code_math(n: int = 50, seed: int = 42, params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    random.seed(seed)
    out = []
    for i in range(n):
        if random.random() < 0.5:
            out.append(_math_item())
        else:
            out.append(_code_item())
    return out
