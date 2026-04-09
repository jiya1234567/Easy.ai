import pandas as pd
import numpy as np
import os
import json

def generate_financial_data(n_days=500):
    """
    Generates stable, correlated multi-asset financial data.
    Uses log-returns with factor loadings to ensure stability.
    """
    np.random.seed(42)
    
    # 1. Asset Groups
    asset_metadata = {
        'SPY': 'Equity', 'QQQ': 'Equity', 'TSLA': 'Equity', 'AAPL': 'Equity', 'NVDA': 'Equity',
        'TLT': 'Bond', 'IEF': 'Bond', 'BND': 'Bond',
        'EURUSD': 'FX', 'USDJPY': 'FX', 'GBPUSD': 'FX',
        'GLD': 'Commodity', 'USO': 'Commodity', 'DBA': 'Commodity',
        'CDX_IG': 'Credit', 'CDX_HY': 'Credit'
    }
    
    all_tickers = list(asset_metadata.keys())
    n_assets = len(all_tickers)
    
    # 2. Simulate Factors (Daily Returns)
    # Market, Rates, Vol
    factors = np.random.normal(0, 0.005, (n_days, 3))
    
    # 3. Factor Loadings
    loadings = {
        'SPY': [1.0, -0.1, 0.2],
        'QQQ': [1.2, -0.2, 0.3],
        'TSLA': [1.8, -0.4, 0.8],
        'AAPL': [1.1, -0.1, 0.2],
        'NVDA': [2.0, -0.3, 0.5],
        'TLT': [-0.1, 1.0, -0.2],
        'IEF': [-0.05, 0.8, -0.1],
        'BND': [0.0, 0.7, 0.0],
        'EURUSD': [0.1, -0.2, 0.1],
        'USDJPY': [-0.1, 0.3, -0.1],
        'GBPUSD': [0.1, -0.2, 0.1],
        'GLD': [0.0, -0.3, 0.3],
        'USO': [0.4, 0.1, 0.2],
        'DBA': [0.2, 0.0, 0.1],
        'CDX_IG': [-0.2, 0.1, -0.5],
        'CDX_HY': [-0.5, 0.2, -1.0],
    }
    
    df = pd.DataFrame(index=pd.date_range(end='2026-04-08', periods=n_days, freq='B'))
    
    for ticker in all_tickers:
        l = np.array(loadings[ticker])
        # Returns = Factor Contribution + Specific Risk
        ret = (factors @ l) + np.random.normal(0, 0.01, n_days)
        # Scale to realistic daily volatility
        ret = ret * 0.5 # 50% scaling
        # Prices
        prices = 100 * np.exp(np.cumsum(ret))
        df[ticker] = prices
        
    return df, asset_metadata

if __name__ == "__main__":
    print("Generating Stable Multi-Asset Data...")
    data, metadata = generate_financial_data()
    
    os.makedirs("reports", exist_ok=True)
    data.to_csv("reports/multi_asset_data.csv")
    
    with open("reports/asset_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
        
    print("Data & Metadata saved successfully.")
