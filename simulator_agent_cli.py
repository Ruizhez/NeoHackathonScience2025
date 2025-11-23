#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

spoon_core = Path.cwd() / "spoon-core"
sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(spoon_core))

from simulator_agent.agent import run_with_demand

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim", required=True)
    ap.add_argument("--demand", required=True)
    ap.add_argument("--json-out")
    ap.add_argument("--no-save", action="store_true")
    args = ap.parse_args()
    run_with_demand(args.sim, args.demand, json_out=args.json_out, no_save=args.no_save)

if __name__ == "__main__":
    main()