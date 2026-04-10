import pandas as pd
import numpy as np
import os
import time

def generate_1m_nodes(n_assets=100, n_days=10000):
    """
    Generates 1,000,000 nodes (100 assets * 10,000 days).
    """
    print(f"Generating {n_assets * n_days:,} data nodes...")
    start = time.time()
    
    np.random.seed(42)
    dates = pd.date_range(end='2026-04-08', periods=n_days, freq='H') # Hourly to get more days in a year
    
    data = {}
    for i in range(n_assets):
        ticker = f"ASSET_{i:03d}"
        # Random walk
        returns = np.random.normal(0, 0.01, n_days)
        prices = 100 * np.exp(np.cumsum(returns))
        data[ticker] = prices
        
    df = pd.DataFrame(data, index=dates)
    
    elapsed = time.time() - start
    print(f"Generated in {elapsed:.2f}s")
    
    os.makedirs("reports", exist_ok=True)
    df.to_csv("reports/large_scale_data.csv")
    print(f"Saved to reports/large_scale_data.csv ({os.path.getsize('reports/large_scale_data.csv') / (1024*1024):.2f} MB)")
    return "reports/large_scale_data.csv"

if __name__ == "__main__":
    generate_1m_nodes()
