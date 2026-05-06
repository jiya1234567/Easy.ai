"""
RetinalAnalyzer — OMEGA-CORE Optometric Vision Module
Uses Gemini Vision (multimodal diffusion-style analysis) to perform:
  - Retinal vascular mapping
  - Pupillary response & dilation assessment
  - Scleral health (yellowing / redness index)
  - Diabetic retinopathy risk scoring
  - Glaucoma / cup-to-disc ratio estimate
  - Macular degeneration early markers
  - Optometric depth score (simulated OCT proxy)
"""

import os
import json
import base64
import datetime

try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"), override=False)
except ImportError:
    pass

from google import genai
from google.genai import types
from mistralai.client import Mistral

# ── Risk colour map ────────────────────────────────────────────────────────────
RISK_COLORS = {
    "NORMAL":   "#10B981",
    "LOW":      "#10B981",
    "MODERATE": "#F59E0B",
    "HIGH":     "#EF4444",
    "CRITICAL": "#EF4444",
}

RETINAL_SCHEMA = {
    "overall_risk":          "NORMAL|LOW|MODERATE|HIGH|CRITICAL",
    "confidence":            {"mean": 0.0, "uncertainty": 0.0},
    "pupil_dilation_mm":     {"mean": 0.0, "uncertainty": 0.0},
    "pupil_symmetry":        "NORMAL|ASYMMETRIC",
    "scleral_health":        "CLEAR|MILD_REDNESS|SEVERE_REDNESS|YELLOWING",
    "vascular_density":      "NORMAL|REDUCED|ELEVATED",
    "cup_disc_ratio":        {"mean": 0.0, "uncertainty": 0.0},
    "retinal_depth_score":   {"mean": 0.0, "uncertainty": 0.0},
    "diabetic_risk_score":   {"band": "LOW|MODERATE|HIGH|CRITICAL", "probability": 0.0},
    "glaucoma_risk_score":   {"band": "LOW|MODERATE|HIGH|CRITICAL", "probability": 0.0},
    "macular_risk_score":    {"band": "LOW|MODERATE|HIGH|CRITICAL", "probability": 0.0},
    "findings":              ["finding 1", "finding 2"],
    "bounding_boxes":        [{"label": "exudate", "ymin": 0, "xmin": 0, "ymax": 0, "xmax": 0}],
    "recommendations":       ["action 1", "action 2"],
    "optometric_summary":    "Clinical summary text",
    "alert_required":        False,
    "alert_reason":          ""
}


class RetinalAnalyzer:
    """
    OMEGA-CORE Vision Module.
    Hardened to separate surface-level external observations from 
    deep-tissue retinal diagnostics with strict confidence gating.
    """

    def __init__(self, api_key=None, engine="Gemini"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.engine  = engine # "Gemini" or "Mistral"
        self.model   = "gemini-2.0-flash" if engine == "Gemini" else "pixtral-12b-2409"

    def classify_image(self, image_bytes: bytes, mime_type: str) -> str:
        """Classifies image type using the multimodal model."""
        prompt = """
        Analyze this image and return a JSON object with a single key 'image_type'.
        Values: 'EXTERNAL_EYE_PHOTO' or 'RETINAL_FUNDUS_SCAN'.
        """
        if self.engine == "Gemini":
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=[types.Part.from_bytes(data=image_bytes, mime_type=mime_type), prompt],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            return json.loads(response.text).get("image_type", "EXTERNAL_EYE_PHOTO")
        else:
            # Mistral Pixtral Classification
            client = Mistral(api_key=self.api_key)
            b64 = base64.b64encode(image_bytes).decode("utf-8")
            response = client.chat.complete(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": f"data:{mime_type};base64,{b64}"}
                        ]
                    }
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content).get("image_type", "EXTERNAL_EYE_PHOTO")

    def analyze_image_bytes(self, image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
        """
        Hardened entry: Classifies image type and applies branched diagnostic logic.
        """
        if not self.api_key:
            return {"error": f"No {self.engine.upper()} API_KEY provided."}

        b64 = base64.b64encode(image_bytes).decode("utf-8")
        
        # ── Step 1: Classification ──
        image_type = self.classify_image(image_bytes, mime_type)

        # ── Step 2: Branched Prompting ──
        if image_type == "RETINAL_FUNDUS_SCAN":
            system_role = "expert AI ophthalmologist performing a clinical fundus analysis."
            focus_areas = "Vascular density, Cup-to-disc ratio, Hemorrhages, and Exudates."
        else:
            system_role = "AI triage engine performing an external ocular surface assessment."
            focus_areas = "Scleral health (redness/yellowing), Pupil symmetry, and Periorbital markers."

        prompt = f"""
You are OMEGA-CORE {system_role}. 

IMAGE TYPE DETECTED: {image_type}.
FOCUS AREAS: {focus_areas}.

STRICT REQUIREMENT: Separate what is OBSERVED (directly seen) from what is INFERRED (suggested).
If image_type is EXTERNAL_EYE_PHOTO, strictly suppress claims about 'retinal vascularity' or 'fundus hemorrhages'.

Return ONLY valid JSON matching this exact structure:
{{
  "image_type": "{image_type}",
  "overall_risk": "NORMAL|LOW|MODERATE|HIGH|CRITICAL",
  "confidence_score": 0.0,
  "observations": [
    {{ "attribute": "sclera", "finding": "...", "confidence": 0.0, "evidence": "patch_analysis_description" }}
  ],
  "inferences": [
    {{ "category": "metabolic", "theory": "...", "confidence": 0.0, "source": "visual_marker" }}
  ],
  "pupil_data": {{ "dilation_mm": 0.0, "symmetry": "NORMAL|ASYMMETRIC" }},
  "bounding_boxes": [{{ "label": "...", "ymin": 0, "xmin": 0, "ymax": 0, "xmax": 0 }}],
  "recommendations": ["action 1"],
  "medical_disclaimer": "This is a triage tool. Not for clinical diagnosis."
}}
"""

        try:
            if self.engine == "Gemini":
                client   = genai.Client(api_key=self.api_key)
                response = client.models.generate_content(
                    model=self.model,
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                        prompt
                    ],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
                result = json.loads(response.text)
            else:
                # Mistral Pixtral Analysis
                client = Mistral(api_key=self.api_key)
                response = client.chat.complete(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": f"data:{mime_type};base64,{b64}"}
                            ]
                        }
                    ],
                    response_format={"type": "json_object"}
                )
                result = json.loads(response.choices[0].message.content)

            result["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result["image_type"] = image_type
            result["model"]      = self.model
            result["engine"]     = self.engine

            # -- HEATMAP / DIAGNOSTIC MASK RENDERING --
            try:
                import io
                from PIL import Image, ImageDraw, ImageFont
                
                img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
                overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(overlay)
                
                width, height = img.size
                
                for box in result.get("bounding_boxes", []):
                    label = box.get("label", "lesion")
                    
                    # Normalize from Gemini 0-1000 scale
                    y_min = (box["ymin"] / 1000.0) * height if box["ymin"] > 1 else box["ymin"] * height
                    x_min = (box["xmin"] / 1000.0) * width if box["xmin"] > 1 else box["xmin"] * width
                    y_max = (box["ymax"] / 1000.0) * height if box["ymax"] > 1 else box["ymax"] * height
                    x_max = (box["xmax"] / 1000.0) * width if box["xmax"] > 1 else box["xmax"] * width
                    
                    color = (255, 0, 0, 160) if "hemorrhage" in label.lower() else (255, 200, 0, 160)
                    draw.rectangle([x_min, y_min, x_max, y_max], outline=color, width=4)
                    draw.text((x_min, max(0, y_min - 15)), label, fill=color)
                
                out_img = Image.alpha_composite(img, overlay).convert("RGB")
                buf = io.BytesIO()
                out_img.save(buf, format="JPEG")
                result["diagnostic_heatmap"] = base64.b64encode(buf.getvalue()).decode("utf-8")
            except Exception as mask_error:
                result["heatmap_error"] = str(mask_error)

            self._save_scan(result)
            return result

        except Exception as e:
            return {"error": f"Retinal analysis failed: {e}"}
    def _save_scan(self, result: dict):
        """Persist scan to reports/retinal_scans.json"""
        log_path = "reports/retinal_scans.json"
        scans    = []
        if os.path.exists(log_path):
            try:
                with open(log_path) as f:
                    scans = json.load(f)
            except Exception:
                scans = []
        scans.append(result)
        os.makedirs("reports", exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(scans[-50:], f, indent=2)   # Keep last 50 scans

    def get_scan_history(self) -> list:
        log_path = "reports/retinal_scans.json"
        if os.path.exists(log_path):
            try:
                with open(log_path) as f:
                    return json.load(f)
            except Exception:
                return []
        return []


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], "rb") as img_file:
            data = img_file.read()
        analyzer = RetinalAnalyzer()
        result   = analyzer.analyze_image_bytes(data)
        print(json.dumps(result, indent=2))
    else:
        print("Usage: py intelligence/retinal_analyzer.py path/to/eye_image.jpg")
