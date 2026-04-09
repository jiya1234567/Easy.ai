from intelligence.scientific_engine import ScientificEngine
import pandas as pd

def test_shock_simulation():
    engine = ScientificEngine()
    engine.load_data()
    
    print("Running Selective Shock: USDJPY -> 160")
    shock_df = engine.simulate_shock("USDJPY", 160.0)
    
    print(f"Shock Manifold Nodes: {len(shock_df)}")
    print(shock_df.head())
    
    # Check if USDJPY is in the manifold result
    if "USDJPY" in shock_df['Asset'].values:
        pos = shock_df[shock_df['Asset'] == 'USDJPY'].iloc[0]
        print(f"USDJPY Latent Position: ({pos['Dim_1']:.2f}, {pos['Dim_2']:.2f}, {pos['Dim_3']:.2f})")
    
    # Calculate Stability
    stability = engine.compute_stability()
    print(f"Manifold Stability Index: {stability*100:.1f}%")
    
    # Calculate Sensitivity
    sensitivity = engine.compute_sensitivity()
    print(f"Lyapunov Sensitivity: {sensitivity:.4f}")

if __name__ == "__main__":
    test_shock_simulation()
