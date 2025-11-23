#!/usr/bin/env python3
"""
Minimal FastAPI server to connect frontend with simulator_agent
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import sys
import shutil
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path.cwd()))

from simulator_agent.agent import run_with_demand

app = FastAPI(title="Simulator Agent API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationRequest(BaseModel):
    simulator_path: str  # e.g., "simulators/H20E.py"
    demand: str          # e.g., "最大化 V_H2_L"
    k: int = 3          # Number of top results to return


class SimulationResponse(BaseModel):
    success: bool
    data: dict = None
    error: str = None


@app.get("/")
async def root():
    return {"message": "Simulator Agent API is running", "version": "1.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/upload")
async def upload_simulator(file: UploadFile = File(...)):
    """
    Upload a simulator Python file

    Returns the path where the file was saved
    """
    try:
        print("=" * 80)
        print("📤 Received file upload:")
        print(f"   Filename: {file.filename}")
        print(f"   Content-Type: {file.content_type}")
        print("=" * 80)

        # Validate file type
        if not file.filename.endswith('.py'):
            raise HTTPException(status_code=400, detail="Only .py files are allowed")

        # Create uploads directory if it doesn't exist
        uploads_dir = Path("uploaded_simulators")
        uploads_dir.mkdir(exist_ok=True)

        # Create unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = uploads_dir / safe_filename

        # Save the file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"✅ File saved to: {file_path}")
        print("=" * 80)

        return {
            "success": True,
            "path": str(file_path),
            "filename": file.filename,
            "message": f"File uploaded successfully to {file_path}"
        }

    except Exception as e:
        print(f"🔴 Error uploading file: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/api/simulate", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest):
    """
    Run simulator with user demand

    Example request:
    {
        "simulator_path": "simulators/H20E.py",
        "demand": "最大化 V_H2_L",
        "k": 3
    }
    """
    try:
        print("=" * 80)
        print("🔵 Received simulation request:")
        print(f"   Simulator: {request.simulator_path}")
        print(f"   Demand: {request.demand}")
        print(f"   K: {request.k}")
        print("=" * 80)

        # Check if simulator file exists
        sim_path = Path(request.simulator_path)
        if not sim_path.exists():
            print(f"🔴 Simulator file not found: {request.simulator_path}")
            raise HTTPException(status_code=404, detail=f"Simulator file not found: {request.simulator_path}")

        print(f"✅ Simulator file found: {sim_path}")

        # Run the simulator agent
        print("🚀 Running simulator agent...")
        result = run_with_demand(
            sim_path=str(sim_path),
            demand_text=request.demand,
            json_out=None,  # Don't save to file, just return data
            no_save=True    # Don't auto-save to Experiments/
        )

        print("✅ Simulation completed successfully!")
        print(f"   Total runs: {len(result.get('runs', []))}")
        print(f"   Success count: {result.get('selection_summary', {}).get('success_count', 0)}")
        print("=" * 80)

        return SimulationResponse(success=True, data=result)

    except HTTPException:
        raise
    except Exception as e:
        print(f"🔴 Error running simulation: {e}")
        import traceback
        traceback.print_exc()
        return SimulationResponse(success=False, error=str(e))


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simulator Agent API Server...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
