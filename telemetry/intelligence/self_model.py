import json, os, random
def get_system_awareness(signals):
    """SELF-AWARENESS: Monitors internal logic health."""
    iq = 185
    conf = float(signals.get("confidence", 0.5))
    # Awareness of 'Uncertainty'
    awareness = "Optimal" if conf > 0.8 else "Internal Logic Deficit Detected"
    return {"awareness": awareness, "iq": iq, "motivation": "High (Breakthrough Seek)"}
