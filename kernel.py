import google.generativeai as genai
import json
import os
import asyncio # Required for FastAPI seamlessness
from PIL import Image

# 1. AUTHENTICATION (The Kernel Heart)
# Ensure you run: export GOOGLE_API_KEY='your_key' in your terminal
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("CRITICAL ERROR: GOOGLE_API_KEY not found in environment.")

genai.configure(api_key=api_key)

# 2. THE 90-STEP AUDIT ENGINE
async def run_audit(paths):
    """
    Asynchronous Kernel execution to prevent FastAPI blocking.
    """
    # Step 1: Institutional Data Retrieval
    with open("PROMPT", "r") as f: system_instructions = f.read()
    with open(paths['target'], "r") as f: target = f.read()
    with open(paths['fixed'], "r") as f: fixed = f.read()
    
    # Building the Sovereign Context
    context = [
        system_instructions, 
        f"FIXED SAFE: {fixed}", 
        f"MISSION TARGET: {target}"
    ]
    
    # Step 2: Multimodal Senses (Variable Ingress)
    if os.path.exists(paths['variable_img']):
        try:
            img = Image.open(paths['variable_img'])
            img.load() # Force load into memory
            context.append(img)
        except Exception as e:
            print(f"Vision Ingress Error: {e}")
    
    if os.path.exists(paths['variable_txt']):
        with open(paths['variable_txt'], "r") as f:
            ingress_data = f.read()
            context.append(f"VARIABLE DATA INGRESS: {ingress_data}")

    # Step 3: Critical Thinking Execution (The Phillips Agent)
    # We use 'to_thread' to run the heavy AI call without blocking other users
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Run the AI call in a background thread for FastAPI
    response = await asyncio.to_thread(model.generate_content, context)
    
    # Step 4: Artifact Generation (DASHBOARD.md)
    with open(paths['dashboard'], "w") as f:
        f.write(response.text)
        
    return response.text