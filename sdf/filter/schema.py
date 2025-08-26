from __future__ import annotations
from typing import Any, Dict, List, Tuple
from jsonschema import validate, ValidationError

# SFT minimal requirements
REQ_SFT = ["instruction","output","meta"]
REQ_DPO = ["prompt","chosen","rejected"]
# Tool-calling top-level keys
REQ_TOOL = ["prompt","tools","assistant_call","assistant_result","assistant_response","meta"]

def is_sft(it: Dict[str, Any]) -> bool:
    return all(k in it for k in REQ_SFT) and isinstance(it.get("meta",{}), dict)

def is_dpo(it: Dict[str, Any]) -> bool:
    return all(k in it for k in REQ_DPO)

def is_tool(it: Dict[str, Any]) -> bool:
    return all(k in it for k in REQ_TOOL) and isinstance(it.get("tools",[]), list) and len(it.get("tools",[]))>0

def _validate_tool_row(it: Dict[str, Any]) -> bool:
    """Validate assistant_call.arguments against the provided tool schema."""
    try:
        tool = it["tools"][0]
        schema = tool.get("schema", {})
        call = it.get("assistant_call", {})
        if call.get("name") != tool.get("name"):
            return False
        args = call.get("arguments", {})
        validate(instance=args, schema=schema)
        return True
    except (KeyError, ValidationError):
        return False

def filter_schema(items: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    allowed = set(cfg.get("allow_types", ["sft","tool","dpo"]))
    kept: List[Dict[str, Any]] = []
    dropped: List[Dict[str, Any]] = []
    for it in items:
        ok = False
        reason = None
        if "sft" in allowed and is_sft(it):
            ok = True
        elif "dpo" in allowed and is_dpo(it):
            ok = True
        elif "tool" in allowed and is_tool(it) and _validate_tool_row(it):
            ok = True
        else:
            reason = "schema"
        if ok:
            kept.append(it)
        else:
            dropped.append({"item": it, "reason": reason or "schema"})
    return kept, dropped
