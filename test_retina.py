import os
import sys
import json
import base64

# Add the local directory to path just in case
sys.path.append(os.path.dirname(__file__))

from intelligence.retinal_analyzer import RetinalAnalyzer

def main():
    img_path = r"C:\Users\simon\.gemini\antigravity\brain\ce9afd1c-7863-4fdc-8b7c-cb5af3a37680\media__1776049215877.jpg"
    out_img = r"C:\Users\simon\.gemini\antigravity\brain\ce9afd1c-7863-4fdc-8b7c-cb5af3a37680\media_heatmap.jpg"
    
    with open(img_path, "rb") as f:
        img_bytes = f.read()
        
    print("Initializing Analyzer...")
    analyzer = RetinalAnalyzer() # This will inherit os.environ["GEMINI_API_KEY"] which must be set!
    
    # Let's ensure the API key is passed explicitly if it's missing from env
    # Since we are running in a terminal, let's load it from .env or require it
    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    if not analyzer.api_key:
        analyzer.api_key = os.environ.get("GEMINI_API_KEY")
        
    if not analyzer.api_key:
        print("ERROR: GEMINI_API_KEY is not set in .env")
        sys.exit(1)
        
    print("Running analyze_image_bytes...")
    result = analyzer.analyze_image_bytes(img_bytes)
    
    if "error" in result:
        print("API ERROR:", result["error"])
        sys.exit(1)
        
    heatmap_b64 = result.pop("diagnostic_heatmap", None)
    
    # Save the heatmap image
    if heatmap_b64:
        print("Heatmap generated! Saving to:", out_img)
        img_data = base64.b64decode(heatmap_b64)
        with open(out_img, "wb") as f:
            f.write(img_data)
    else:
        print("No heatmap was generated in the result.")
        
    print("\n--- JSON PAYLOAD ---\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
