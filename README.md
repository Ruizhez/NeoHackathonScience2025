项目概述

一个可视化科研编排前端（React + Vite + Shadcn）配合本地 Simulation Agent 后端（FastAPI），根据用户需求自动分析并运行 Python 模拟器，返回结构化 JSON 结果并在画布节点展示
已内置三个示例模拟器：水电解 H2O（H20E.py）、声学波 FEM（FEM2DSonic.py）、Navier–Stokes FDM（FDM2DN-S.py）
目录结构

simulators/：示例模拟器源代码
H20E.py（轻量）
FEM2DSonic.py（声学波，需 scipy/matplotlib 最佳）
FDM2DN-S.py（Navier–Stokes，已提供标准入口）
Frontend/exact-display-cap-main/：前端项目（React + Vite）
simulator_agent/：后端核心逻辑（分析器、运行器、需求解析、选参）
simulator_api.py：后端 FastAPI 服务（JSON 接口）
Experiments/：运行结果 JSON（本地 CLI 测试生成）
快速启动

后端（本地联调）

cd /Users/ruizhezheng/Documents/trae_projects
安装依赖（在当前 Python 环境）：
python -m pip install fastapi uvicorn pydantic
启动服务：
uvicorn simulator_api:app --host 127.0.0.1 --port 8010
打开接口文档：
http://127.0.0.1:8010/docs
前端（本地联调）

cd /Users/ruizhezheng/Documents/trae_projects/Frontend/exact-display-cap-main
安装依赖：
npm install
启动开发服务器（确保指向本地后端）：
VITE_API_URL=http://127.0.0.1:8010 npm run dev
访问：
http://localhost:5173/
前端使用

进入仪表盘 → 打开项目 → 进入画布
在画布中：
选择或添加模拟器节点，fileName 填相对路径（例如 simulators/H20E.py）
在 Prompt 节点输入需求（如目标与约束），连接 Prompt → Simulator，点击运行
将生成 Result 节点，展示后端返回的 JSON（含 runs 与 selection_summary）
需求示例：
H20E：最大化 V_H2_L; current_a<=3; efficiency>=0.8
FDM2DN-S：最大化 vorticity_max; Nx 在 80-160; Ny 在 40-80; nt 在 200-400; save_every=50
FEM2DSonic（低配）：最大化 u_max_final; T 在 0.5-0.8; num_steps 在 100-200; nx 在 31-51; ny 在 31-51
后端 API

POST /api/simulator/upload
入参：{ "filename": "H20E.py", "content_base64": "<base64>" }
出参：{ "sim_path": "/Users/.../simulators/uploads/H20E.py" }
POST /api/simulator/analyze
入参：{ "sim_path": "/Users/.../simulators/H20E.py" }
出参：{ "module_path": "...", "entry": "simulate_electrolysis|run_wave_2d_fem|simulate_ns2d", "inputs": [...], "description": "..." }
POST /api/simulator/run
入参：{ "sim_path": "/Users/.../simulators/H20E.py", "demand": "最大化 V_H2_L; current_a<=3; efficiency>=0.8", "k": 3, "no_save": true }
出参：结构化 JSON：
experiment_name: 字符串
experiment_description: 字符串
runs: 数组（每项含 inputs、末端 final 指标、raw_keys）
selection_summary: { "objective": { "type": "max|min", "target": "..." }, "candidate_count": N, "success_count": M }
模拟器约定

文件路径：
在前端填写相对路径 simulators/<your_sim>.py；前端会自动转为绝对路径传给后端
入口函数（加载器优先顺序）：
simulate_ns2d（FDM2DN-S）
run_wave_2d_fem（FEM2DSonic）
任何 simulate*
任何 run_*（排除 run_demo）
返回值：dict，包含末端关键指标（例如 V_H2_L、vorticity_max、u_max_final）
CLI 测试（可选）

H20E：
python simulator_agent_cli.py --sim simulators/H20E.py --demand '最大化 V_H2_L; current_a 在 1-3; total_time_s 在 300-600; efficiency>=0.9' --json-out Experiments/h20e_run.json --no-save
FDM2DN-S：
python simulator_agent_cli.py --sim simulators/FDM2DN-S.py --demand '最大化 vorticity_max; Nx 在 80-160; Ny 在 40-80; nt 在 200-400; save_every=50' --json-out Experiments/fdm2d_run.json --no-save
FEM2DSonic（低配）：
python simulator_agent_cli.py --sim simulators/FEM2DSonic.py --demand '最大化 u_max_final; T 在 0.5-0.8; num_steps 在 100-200; nx 在 31-51; ny 在 31-51' --json-out Experiments/fem2d_run_low.json --no-save
