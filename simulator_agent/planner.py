from typing import Any, Dict, List
import numpy as np

def make_grid(inputs: List[Dict[str, Any]], constraints: List[Dict[str, Any]], samples: int = 20) -> List[Dict[str, Any]]:
    grid = []
    ranges = []
    names = []
    for item in inputs:
        name = item["name"]
        default = item.get("default")
        if not isinstance(default, (int, float)):
            lname = name.lower()
            if "time" in lname:
                default = 600.0
            elif "current" in lname or "amp" in lname:
                default = 2.0
            elif "dt" == lname:
                default = 1.0
            elif "temperature" in lname or "temp" in lname:
                default = 25.0
            elif "pressure" in lname:
                default = 1.0
            elif "efficiency" in lname:
                default = 1.0
            else:
                default = 1.0
        names.append(name)
        if isinstance(default, (int, float)):
            lo = default*0.5 if default not in [0] else 0
            hi = default*1.5 if default not in [0] else 1.0
            ranges.append(np.linspace(lo, hi, 5))
        else:
            ranges.append([default])
    def product(acc, idx):
        if idx == len(ranges):
            item = dict(acc)
            if satisfies(item, constraints):
                grid.append(item)
            return
        for v in ranges[idx]:
            acc[names[idx]] = float(v) if isinstance(v, np.floating) else v
            product(acc, idx+1)
    product({}, 0)
    return grid[:samples]

def satisfies(item: Dict[str, Any], constraints: List[Dict[str, Any]]) -> bool:
    for c in constraints or []:
        key = c.get("key")
        op = c.get("op")
        val = c.get("value")
        if key not in item:
            continue
        x = item[key]
        try:
            if op == "<=":
                if not (x <= val): return False
            elif op == ">=":
                if not (x >= val): return False
            elif op == "==":
                if not (x == val): return False
            elif op == "between" and isinstance(val, list) and len(val) == 2:
                a, b = val
                if not (a <= x <= b): return False
        except Exception:
            continue
    return True

def select_top(runs: List[Dict[str, Any]], objective: Dict[str, Any], k: int) -> List[Dict[str, Any]]:
    target = objective.get("target")
    tp = objective.get("type", "max")
    scored = []
    for r in runs:
        final = r.get("final", {})
        val = final.get(target)
        if isinstance(val, dict):
            val = None
        scored.append((val, r))
    scored = [x for x in scored if x[0] is not None]
    reverse = tp == "max"
    scored.sort(key=lambda x: x[0], reverse=reverse)
    return [x[1] for x in scored[:k]]