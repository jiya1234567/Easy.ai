from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import kernel  # Connects to your logic
import os
import json

app = FastAPI(title="Phillips Institutional Kernel")

# Exact Paths from your Tree
PATHS = {
    "fixed": "./FIXED/profile.json",
    "target": "Target.JASON",
    "variable_img": "./VARIABLE/input_image.jpg",
    "variable_txt": "./VARIABLE/placeholder.txt",
    "dashboard": "DASHBOARD.md"
}

@app.get("/status")
async def get_status():
    return {"status": "Phillips Kernel Online"}

@app.post("/execute")
async def execute_audit():
    """
    Step 21-90: The Institutional Execution.
    """
    try:
        # Run the 90-step reasoning in kernel.py
        report = await kernel.run_audit(PATHS)
        # We return a clear dictionary so app.py doesn't get a KeyError
        return {"status": "Success", "data": report}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)