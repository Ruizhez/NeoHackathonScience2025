from typing import Any, Dict, Optional, List, Tuple
import re

def parse_demand(demand: str) -> Dict[str, Any]:
    # objective
    obj_type = "max" if "最大化" in demand or "maximize" in demand.lower() else ("min" if "最小化" in demand or "minimize" in demand.lower() else "max")
    target = extract_target(demand)
    constraints = extract_constraints(demand)
    k = extract_k(demand) or 3
    return {"objective": {"type": obj_type, "target": target}, "constraints": constraints, "k": k}

def extract_target(text: str) -> str:
    m = re.search(r"最大化\s*([A-Za-z0-9_\.\-]+)", text)
    if m:
        return m.group(1).strip()
    m = re.search(r"最小化\s*([A-Za-z0-9_\.\-]+)", text)
    if m:
        return m.group(1).strip()
    # fallback: try find uppercase-like tokens
    m = re.findall(r"[A-Za-z][A-Za-z0-9_]+", text)
    return m[0] if m else ""

def extract_k(text: str) -> Optional[int]:
    m = re.search(r"选取(\d+)组", text)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return None
    return None

def extract_constraints(text: str) -> List[Dict[str, Any]]:
    cons: List[Dict[str, Any]] = []
    # patterns like key<=value, key>=value, key=value
    for pat in [r"([A-Za-z_][A-Za-z0-9_]*)\s*<=\s*([0-9\.]+)", r"([A-Za-z_][A-Za-z0-9_]*)\s*>=\s*([0-9\.]+)", r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([0-9\.]+)"]:
        for m in re.finditer(pat, text):
            key = m.group(1)
            val = float(m.group(2))
            op = "<=" if "<=" in pat else (">=" if ">=" in pat else "==")
            cons.append({"key": key, "op": op, "value": val})
    # ranges: key 在 a-b / between a-b
    for m in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*(?:在|between)\s*([0-9\.]+)\s*-\s*([0-9\.]+)", text):
        key = m.group(1)
        a = float(m.group(2)); b = float(m.group(3))
        cons.append({"key": key, "op": "between", "value": [a, b]})
    return cons