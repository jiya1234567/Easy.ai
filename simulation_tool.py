import os
import json
import asyncio
from google import genai
from google.genai import types

# Load API Key from environment
API_KEY = os.environ.get("GEMINI_API_KEY")

async def run_simulation(oil_price: float):
    """
    Runs a high-fidelity simulation of a global economic shock.
    """
    client = genai.Client(api_key=API_KEY)
    
    model_id = "gemini-3-flash-preview"
    
    system_instruction = """
    You are the OMEGA-CORE SIMULATOR. 
    You analyze global hypergraph nodes for economic stability.
    
    Current Scenario:
    - Brent Oil Price: ${oil_price}
    - Pivot Point: 4.25%
    - Systemic Depression Probability (Baseline): 12%
    
    Your task is to:
    1. Calculate the new Systemic Depression Probability.
    2. Identify the primary node of failure.
    3. Provide a 3-line summary of the outcome.
    4. Provide a 2-line strategic suggestion.
    
    Output JSON format:
    {
      "depression_probability": "XX%",
      "failure_node": "string",
      "summary": ["line 1", "line 2", "line 3"],
      "suggestions": ["line 1", "line 2"]
    }
    """
    
    prompt = f"Execute Stress Test: Brent Oil at ${oil_price}. Analyze hypergraph bifurcation."
    
    print(f"--- INITIATING SIMULATION: OIL @ ${oil_price} ---")
    
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction.format(oil_price=oil_price),
                response_mime_type="application/json",
            ),
        )
        
        result = json.loads(response.text)
        
        print("\n[SIMULATION RESULTS]")
        print(f"DEPRESSION PROBABILITY: {result['depression_probability']}")
        print(f"PRIMARY FAILURE NODE: {result['failure_node']}")
        
        print("\n[MISSION SUMMARY]")
        for line in result['summary']:
            print(f"- {line}")
            
        print("\n[STRATEGIC SUGGESTIONS]")
        for line in result['suggestions']:
            print(f"- {line}")
            
    except Exception as e:
        print(f"Error during simulation: {e}")

if __name__ == "__main__":
    # Run the $130 Oil Test
    asyncio.run(run_simulation(130.0))
