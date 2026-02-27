from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import os
import kernel # This connects to your kernel.py

app = FastAPI()

# 1. SETUP TEMPLATES (Points to your /templates folder)
templates = Jinja2Templates(directory="templates")

# 2. THE PATHS (Exact names from your tree)
PATHS = {
    "fixed": "./FIXED/profile.json",
    "target": "Target.JASON",
    "variable_img": "./VARIABLE/input_image.jpg",
    "variable_txt": "./VARIABLE/placeholder.txt",
    "dashboard": "DASHBOARD.md"
}

# 3. THE DASHBOARD VIEW (Table View)
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    # Load data for the table
    with open(PATHS['fixed'], 'r') as f:
        fixed_data = json.load(f)
    with open(PATHS['target'], 'r') as f:
        target_data = json.load(f)
    
    # Check if files exist for the status column
    status = {k: os.path.exists(v) for k, v in PATHS.items()}
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "fixed": fixed_data,
        "target": target_data,
        "status": status
    })

# 4. THE EXECUTION TRIGGER
@app.post("/execute")
async def run_audit_trigger():
    # This calls your async kernel.py
    report = await kernel.run_audit(PATHS)
    return {"status": "Success", "report": report}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)