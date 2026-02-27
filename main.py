from fastapi import FastAPI
import kernel # Your 90-step logic
import os

app = FastAPI()

# Strict Paths for the Kernel
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
    # Calling your kernel.py logic
    try:
        report = await kernel.run_audit(PATHS)
        return {"status": "Success", "data": report}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Port 8000 for the Backend
    uvicorn.run(app, host="0.0.0.0", port=8000)