import os
import json
import base64
from intelligence.retinal_analyzer import RetinalAnalyzer

def test_mistral_vision():
    print("--- OMEGA-CORE MISTRAL VISION TEST (PIXTRAL) ---")
    
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("ERROR: MISTRAL_API_KEY not found.")
        return

    # Use a dummy small image (1x1 black pixel) for testing connectivity
    # Real testing should use a proper fundus image
    dummy_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    image_bytes = base64.b64decode(dummy_b64)
    
    print("Initializing RetinalAnalyzer with Mistral engine...")
    analyzer = RetinalAnalyzer(api_key=api_key, engine="Mistral")
    
    print("Simulating Eyescan Analysis...")
    try:
        # Note: This might fail if the dummy image is too small for the model to classify, 
        # but we are testing the API logic/plumbing.
        result = analyzer.analyze_image_bytes(image_bytes)
        print("\nSUCCESS: Analysis Received.")
        print(f"Engine used: {result.get('engine')}")
        print(f"Model used: {result.get('model')}")
        print(f"Risk Level: {result.get('overall_risk')}")
        print(f"Summary: {result.get('medical_disclaimer')}")
        
    except Exception as e:
        print(f"ERROR: Analysis failed: {e}")

if __name__ == "__main__":
    test_mistral_vision()
