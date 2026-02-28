from fastapi import FastAPI
import kernel
import uvicorn

app = FastAPI()

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
async def execute():
    report = await kernel.run_audit(PATHS)
    return {"status": "Success", "data": report}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)