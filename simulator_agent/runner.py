import importlib.util
import inspect
from pathlib import Path
from typing import Any, Dict, Tuple

def load_module(module_path: str):
    p = Path(module_path)
    spec = importlib.util.spec_from_file_location(p.stem, str(p))
    m = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m

def run_simulator(module_path: str, func_name: str, kwargs: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    module = load_module(module_path)
    fn = getattr(module, func_name)
    result = fn(**kwargs)
    final = {}
    for k, v in result.items():
        try:
            if hasattr(v, "__array__"):
                v = v.tolist()
        except Exception:
            pass
        if isinstance(v, list) and len(v) > 0:
            final[k] = v[-1]
        else:
            final[k] = v
    return result, final