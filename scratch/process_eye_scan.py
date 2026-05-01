import os
import json
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from intelligence.retinal_analyzer import RetinalAnalyzer

def process_total_eye_scan(image_path):
    print(f"Reading eye image: {image_path}")
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    # 1. Analyze with RetinalAnalyzer (Gemini Vision)
    analyzer = RetinalAnalyzer()
    retinal_findings = analyzer.analyze_image_bytes(image_bytes)
    
    # 2. Get Biometric Data (Watch)
    watch_data = {}
    target_jason_path = "c:/Universal_Lab_AP_Phillips/Target.JASON"
    if os.path.exists(target_jason_path):
        with open(target_jason_path, "r") as f:
            watch_data = json.load(f).get("metrics", {})
    
    # 3. Synthesize with Gemini (Hardened Synthesis)
    print("Synthesizing Total Eye Scan report with Hardened Logic...")
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    system_instruction = """
    You are the OMEGA-CORE TOTAL DIAGNOSTIC ENGINE. 
    You synthesize ocular observations and biometric smartwatch data into a unified triage report.
    
    STRICT RULES:
    1. LABEL every finding as 'OBSERVED' (directly visible in image) or 'INFERRED' (derived from data fusion).
    2. WEIGHTED FUSION: For medical markers (BP, Glucose), the smartwatch data should have 80% weight (0.8) and visual markers 20% weight (0.2).
    3. EPISTEMIC HUMILITY: If image_type is 'EXTERNAL_EYE_PHOTO', do NOT make definitive claims about internal retinal health.
    4. UNCERTAINTY: Provide a confidence range (e.g., 85% +/- 5%) for all inferences.
    
    STRICT SCHEMA REQUIREMENT: You must return a JSON object with these EXACT keys:
    - "asset": "TOTAL EYE SCAN"
    - "image_type": "{retinal_findings.get('image_type')}"
    - "status": A 3-word summary of the outlook
    - "visual_observations": List of observed physical markers
    - "biometric_fusion": List of inferred metrics (BP, Glucose, Heart Rate) with 'confidence' and 'fusion_logic'
    - "systemic_risk": { "level": "LOW|MODERATE|HIGH", "confidence": 0.0 }
    - "medical_disclaimer": "MANDATORY: This is a triage screening tool, not a clinical diagnosis. Consult a professional."
    - "report_date": Current date
    """
    
    full_prompt = f"""
    {system_instruction}
    
    RETINAL FINDINGS:
    {json.dumps(retinal_findings, indent=2)}
    
    BIOMETRIC DATA (SMARTWATCH):
    {json.dumps(watch_data, indent=2)}
    
    Synthesize the final Total Eye Scan report.
    """
    
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=full_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    result = json.loads(response.text)
    
    # 4. Save to reports/metrics/eyescan.json
    save_path = "c:/Universal_Lab_AP_Phillips/reports/metrics/eyescan.json"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"Total Eye Scan report generated: {save_path}")
    return result

if __name__ == "__main__":
    image_path = r"C:\Users\simon\.gemini\antigravity\brain\5b8d3408-0323-45a5-94ff-9abd2ab8a0ee\media__1777602428703.jpg"
    report = process_total_eye_scan(image_path)
    print(json.dumps(report, indent=2))
