from __future__ import annotations
import random
from typing import Dict, Any, List

TEMPLATES = [
    ("email", "Write a short, polite email to {person} about {topic}.", lambda d: f"Dear {d['person']},\n\n{d['topic']} is on track.\n\nBest,\nAlex"),
    ("summarize", "Summarize the following text in 3 bullet points: {text}", lambda d: "- Point 1\n- Point 2\n- Point 3"),
    ("list", "List {k} creative uses for a {object}.", lambda d: "\n".join(f"- Use {i+1} for {d['object']}" for i in range(d['k']))),
    ("classify", "Classify the sentiment (positive/negative/neutral): {text}", lambda d: "neutral"),
]

PEOPLE = ["Jordan", "Riley", "Taylor", "Sam"]
TOPICS = ["the Q3 report", "our meeting", "the launch plan", "the schedule"]
OBJECTS = ["paperclip", "flashlight", "rubber band", "sticky note"]
TEXTS = ["I really enjoyed the movie.", "The service was okay.", "This is disappointing."]

def generate_templates(n: int = 50, seed: int = 42, params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    random.seed(seed)
    out = []
    for i in range(n):
        dom, prompt_t, out_fn = random.choice(TEMPLATES)
        d = {}
        if dom == "email":
            d = {"person": random.choice(PEOPLE), "topic": random.choice(TOPICS)}
        elif dom == "summarize":
            d = {"text": random.choice(TEXTS)}
        elif dom == "list":
            d = {"k": random.randint(3,5), "object": random.choice(OBJECTS)}
        elif dom == "classify":
            d = {"text": random.choice(TEXTS)}
        instr = prompt_t.format(**d)
        out_text = out_fn(d)
        out.append({
            "instruction": instr,
            "input": "",
            "output": out_text,
            "meta": {"domain": dom, "template": f"{dom}_v1", "seed": seed+i}
        })
    return out
