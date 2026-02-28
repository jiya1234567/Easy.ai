from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import kernel  # The Reasoning Engine
import uvicorn
import os
import json

app = FastAPI(title="A&P Phillips Institutional Kernel")

# 1. SOVEREIGN PATHS (Exact names for the 90-step cycle)
PATHS = {
    "fixed": "./FIXED/profile.json",
    "target": "Target.JASON",
    "variable_img": "./VARIABLE/input_image.jpg",
    "variable_txt": "./VARIABLE/placeholder.txt",
    "dashboard": "DASHBOARD.md",
    "prompt": "PROMPT"
}

@app.get("/status")
async def get_status():
    # This confirms the iPhone can see the Brain
    return {"status": "Phillips Kernel Online", "hardware": "Sovereign Mobile Bridge"}

@app.post("/execute")
async def execute_audit():
    """
    Triggers the 90-step Sovereign Cycle.
    No Hard-Coded logic. Everything is driven by the keyed-in files.
    """
    try:
        report = await kernel.run_audit(PATHS)
        return {"status": "Success", "data": report}
    except Exception as e:
        return {"status": "Error", "data": f"Kernel Execution Failure: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)