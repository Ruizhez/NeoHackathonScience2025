## Project Overview

This project is a **visual scientific workflow editor** built with **React + Vite + shadcn UI**, paired with a local **Simulation Agent backend** powered by FastAPI.

Users can describe their scientific objectives in natural language. The backend then:

1. Analyzes the request  
2. Selects and configures an appropriate Python-based simulator  
3. Executes the simulation  
4. Returns structured JSON results that are rendered as nodes on an interactive canvas

The system currently includes three example simulators:

- **H₂O Electrolysis (`H20E.py`)** – lightweight and fast to run  
- **2D Acoustic Wave FEM (`FEM2DSonic.py`)** – finite element simulation of wave propagation (best with `scipy` / `matplotlib`)  
- **2D Navier–Stokes FDM (`FDM2DN-S.py`)** – finite difference solver with a standard entry point

---

## Directory Structure

- `simulators/` – Example simulator source code  
  - `H20E.py` – H₂O electrolysis  
  - `FEM2DSonic.py` – 2D acoustic wave FEM  
  - `FDM2DN-S.py` – 2D Navier–Stokes FDM

- `Frontend/exact-display-cap-main/` – Frontend application (React + Vite + shadcn UI)

- `simulator_agent/` – Core Simulation Agent logic  
  - Demand parsing, parameter selection, analysis, and execution

- `simulator_api.py` – FastAPI service exposing JSON endpoints

- `Experiments/` – Example experiment outputs in JSON format (generated via local CLI)

---
