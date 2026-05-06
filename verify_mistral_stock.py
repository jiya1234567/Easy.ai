import os
import json
import time
from mistralai.client import Mistral

def test_mistral_stock_analysis():
    print("--- OMEGA-CORE MISTRAL STOCK TEST ---")
    
    # 1. Load API Key
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        # Try loading from .env if possible
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.environ.get("MISTRAL_API_KEY")
        except:
            pass
            
    if not api_key:
        print("ERROR: MISTRAL_API_KEY not found in environment or .env file.")
        print("Please run: $env:MISTRAL_API_KEY='your_key_here' (PowerShell)")
        return

    client = Mistral(api_key=api_key)
    
    ticker = "SBUX"
    intent = "Analyze SBUX for Institutional Entry"
    domain = "Finance"
    
    print(f"Executing Mission for {ticker} using Mistral Large...")
    
    system_instruction = f"""
    You are the MULTI-AGENT ORCHESTRATOR. Domain: {domain}. Intent: {intent}. Ticker: {ticker}.
    STRICT SCHEMA REQUIREMENT: You must return a JSON object with these EXACT keys:
    - "asset": "{ticker}"
    - "status": A 3-word summary of the outlook
    - "recent_price": Current market price
    - "regime": Either "RISK-ON" or "RISK-OFF"
    - "regime_summary": A one-sentence macro summary
    - "analysis": A list of dicts with EXACT columns: "Category", "Status", and "Meaning"
    - "prediction": A technical forecast summary
    - "report_date": "2026-04-08"
    """

    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Execute analysis for: {intent} {ticker}"}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        print("\nSUCCESS: Prediction Received from Mistral.")
        print(f"Asset: {result['asset']}")
        print(f"Status: {result['status']}")
        print(f"Regime: {result['regime']}")
        print(f"Prediction: {result['prediction']}")
        
        # Save to reports/metrics for the Dashboard to see
        os.makedirs("reports/metrics", exist_ok=True)
        save_path = f"reports/metrics/{ticker.lower()}.json"
        with open(save_path, "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"\nReport saved to {save_path}. You can now view this in the Dashboard REPORTS ENGINE.")
        
    except Exception as e:
        print(f"ERROR: Mistral API call failed: {e}")

if __name__ == "__main__":
    test_mistral_stock_analysis()
