import importlib.util
import inspect
import ast
from pathlib import Path
from typing import Any, Dict, List, Optional

class SimulatorSpec:
    def __init__(self, module_path: str, func_name: str, inputs: List[Dict[str, Any]], outputs: List[str], description: str):
        self.module_path = module_path
        self.func_name = func_name
        self.inputs = inputs
        self.outputs = outputs
        self.description = description

def load_module(module_path: str):
    p = Path(module_path)
    spec = importlib.util.spec_from_file_location(p.stem, str(p))
    m = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m

def pick_simulate_function(module) -> Optional[str]:
    candidates = []
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if name.startswith("simulate"):
            candidates.append(name)
    if candidates:
        return candidates[0]
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        sig = inspect.signature(obj)
        if len(sig.parameters) > 0:
            candidates.append(name)
    return candidates[0] if candidates else None

def analyze_function(module, func_name: str) -> List[Dict[str, Any]]:
    fn = getattr(module, func_name)
    sig = inspect.signature(fn)
    items = []
    for name, param in sig.parameters.items():
        default = None
        if param.default is not inspect._empty:
            default = param.default
        ann = None
        if param.annotation is not inspect._empty:
            ann = param.annotation
        items.append({"name": name, "default": default, "annotation": str(ann) if ann is not None else None})
    return items

def read_docstring(module, func_name: str) -> str:
    fn = getattr(module, func_name)
    doc = inspect.getdoc(fn) or ""
    return doc

def analyze_module(module_path: str) -> SimulatorSpec:
    module = load_module(module_path)
    func_name = pick_simulate_function(module)
    if not func_name:
        raise RuntimeError("no simulate function found")
    inputs = analyze_function(module, func_name)
    desc = read_docstring(module, func_name)
    outputs = []
    return SimulatorSpec(module_path, func_name, inputs, outputs, desc)