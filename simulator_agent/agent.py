from typing import Any, Dict, List
from .analyzer import analyze_module
from .runner import run_simulator
from .demand import parse_demand
from .planner import make_grid, select_top
from pathlib import Path
import json

def run_with_demand(sim_path: str, demand_text: str, json_out: str = None, no_save: bool = False) -> Dict[str, Any]:
    spec = analyze_module(sim_path)
    demand = parse_demand(demand_text)
    objective = demand.get("objective", {"type": "max", "target": ""})
    constraints = demand.get("constraints", [])
    k_val = demand.get("k", 3)
    try:
        k = int(k_val)
    except Exception:
        k = 3
    grid = make_grid(spec.inputs, constraints, samples=30)
    fixed_grid = []
    for item in grid:
        fixed = {}
        for key, v in item.items():
            if v is None:
                lk = key.lower()
                if "time" in lk:
                    v = 600.0
                elif "current" in lk or "amp" in lk:
                    v = 2.0
                elif lk == "dt_s" or lk == "dt":
                    v = 1.0
                elif "temperature" in lk or "temp" in lk:
                    v = 25.0
                elif "pressure" in lk:
                    v = 1.0
                elif "efficiency" in lk:
                    v = 1.0
                else:
                    v = 1.0
            fixed[key] = v
        fixed_grid.append(fixed)
    runs = []
    success = 0
    for item in fixed_grid:
        try:
            raw, final = run_simulator(spec.module_path, spec.func_name, item)
            runs.append({"inputs": item, "final": final, "raw_keys": list(raw.keys())})
            success += 1
        except Exception as e:
            runs.append({"inputs": item, "error": str(e)})
    if success == 0:
        seeds = []
        base = {}
        for it in spec.inputs:
            n = it["name"]
            ln = n.lower()
            if "time" in ln:
                base[n] = 600.0
            elif "current" in ln:
                base[n] = 2.0
            elif ln in ["dt", "dt_s"]:
                base[n] = 1.0
            elif "temperature" in ln or "temp" in ln:
                base[n] = 25.0
            elif "pressure" in ln:
                base[n] = 1.0
            elif "efficiency" in ln:
                base[n] = 1.0
            else:
                base[n] = it.get("default") or 1.0
        for c in [1.0, 2.0, 3.0]:
            s = dict(base)
            for k in list(s.keys()):
                if "current" in k.lower():
                    s[k] = c
            seeds.append(s)
        for item in seeds:
            try:
                raw, final = run_simulator(spec.module_path, spec.func_name, item)
                runs.append({"inputs": item, "final": final, "raw_keys": list(raw.keys())})
                success += 1
            except Exception as e:
                runs.append({"inputs": item, "error": str(e)})
    final_keys = set()
    for r in runs:
        fk = r.get("final", {})
        for kk in fk.keys():
            final_keys.add(kk)
    tgt = objective.get("target")
    if tgt not in final_keys:
        norm = normalize_name(tgt)
        mapped = best_match(norm, final_keys)
        objective["target"] = mapped or (next(iter(final_keys), tgt))
    top = select_top(runs, objective, k)
    if not top:
        if "V_H2_L" in final_keys:
            objective["target"] = "V_H2_L"
            top = select_top(runs, objective, k)
        if not top:
            top = [r for r in runs if r.get("final")] [:k]
    result = {
        "experiment_name": Path(sim_path).stem,
        "experiment_description": demand_text,
        "runs": top,
        "selection_summary": {"objective": objective, "candidate_count": len(runs), "success_count": success},
    }
    if json_out:
        p = Path(json_out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    if not no_save:
        save_default(result)
    return result

def normalize_name(s: str) -> str:
    return (s or "").lower().replace("_", "").replace(" ", "")

def best_match(target_norm: str, keys: set) -> str:
    if not keys:
        return ""
    if not target_norm:
        # pick first numeric-looking key
        return next(iter(keys))
    for k in keys:
        nk = normalize_name(k)
        if target_norm and (target_norm in nk or nk in target_norm):
            return k
    return ""

def save_default(result: Dict[str, Any]):
    base = Path.cwd() / "Experiments"
    base.mkdir(parents=True, exist_ok=True)
    out = base / f"agent_{result['experiment_name']}.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")