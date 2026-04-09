import pandas as pd
import numpy as np
import json
import os
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
try:
    import umap
except ImportError:
    umap = None
import networkx as nx
from sklearn.cluster import KMeans
from scipy.spatial import procrustes

class ScientificEngine:
    """
    Agent-based research system for multi-asset manifold learning.
    """
    def __init__(self, data_path="reports/multi_asset_data.csv", metadata_path="reports/asset_metadata.json"):
        self.data_path = data_path
        self.metadata_path = metadata_path
        self.data = None
        self.metadata = None
        
    # --- DataAgent ---
    def load_data(self):
        if not os.path.exists(self.data_path):
            return False, "Data file missing."
        self.data = pd.read_csv(self.data_path, index_col=0, parse_dates=True)
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, 'r') as f:
                self.metadata = json.load(f)
        return True, "Data loaded successfully."

    # --- ManifoldAgent ---
    def compute_manifold(self, method='PCA', n_components=3):
        if self.data is None: self.load_data()
        
        # Calculate log-returns as features for the assets
        returns = self.data.pct_change().dropna()
        # Transpose so assets are samples, and time is features
        X = returns.T.values
        
        if method == 'PCA':
            model = PCA(n_components=n_components)
            projection = model.fit_transform(X)
        elif method == 'TSNE':
            model = TSNE(n_components=n_components, random_state=42)
            projection = model.fit_transform(X)
        elif method == 'UMAP' and umap:
            model = umap.UMAP(n_components=n_components, random_state=42)
            projection = model.fit_transform(X)
        else:
            # Fallback to PCA
            model = PCA(n_components=n_components)
            projection = model.fit_transform(X)
            
        # Create a result dataframe
        df_proj = pd.DataFrame(projection, columns=[f'Dim_{i+1}' for i in range(n_components)])
        df_proj['Asset'] = returns.columns
        if self.metadata:
            df_proj['Type'] = [self.metadata.get(a, 'Unknown') for a in returns.columns]
        
        return df_proj

    # --- NetworkAgent ---
    def compute_network(self, threshold=0.5):
        if self.data is None: self.load_data()
        
        returns = self.data.pct_change().dropna()
        corr_matrix = returns.corr()
        
        G = nx.Graph()
        for i, asset_a in enumerate(corr_matrix.columns):
            for j, asset_b in enumerate(corr_matrix.columns):
                if i < j:
                    weight = corr_matrix.iloc[i, j]
                    if abs(weight) > threshold:
                        G.add_edge(asset_a, asset_b, weight=weight)
        
        return G

    # --- RegimeAgent ---
    def detect_regimes(self, n_clusters=3):
        if self.data is None: self.load_data()
        
        returns = self.data.pct_change().dropna()
        # Use PCA 2D for clustering regimes over time (rather than assets)
        model = PCA(n_components=2)
        time_projection = model.fit_transform(returns)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        regimes = kmeans.fit_predict(time_projection)
        
        return regimes, time_projection

    # --- DiscoveryAgent (NEW) ---
    def compute_stability(self, method='PCA', window_size=50):
        """
        Manifold Stability Test: Track drift between temporal slices.
        Returns a stability score [0, 1].
        """
        if self.data is None: self.load_data()
        returns = self.data.pct_change().dropna()
        
        if len(returns) < window_size * 2:
            return 1.0 # Not enough data to measure drift
            
        # Slice windows
        w1 = returns.iloc[:window_size].T.values
        w2 = returns.iloc[-window_size:].T.values
        
        # Projections
        model = PCA(n_components=3) if method == 'PCA' else None
        if not model: return 1.0
        
        try:
            p1 = model.fit_transform(w1)
            p2 = model.fit_transform(w2)
            # Procrustes Analysis: align p2 to p1 and return disparity
            _, _, disparity = procrustes(p1, p2)
            # Convert disparity to stability (0 to 1)
            stability = max(0, 1 - (disparity * 5)) # Scale for sensitivity
            return stability
        except:
            return 1.0

    def compute_sensitivity(self, epsilon=0.01):
        """
        Lyapunov-like Sensitivity Test: Measure manifold divergence under perturbation.
        """
        if self.data is None: self.load_data()
        returns = self.data.pct_change().dropna()
        X = returns.T.values
        
        model = PCA(n_components=3)
        p_orig = model.fit_transform(X)
        
        # Perturb
        X_perturbed = X + np.random.normal(0, epsilon, X.shape)
        p_perturbed = model.fit_transform(X_perturbed)
        
        # Measure divergence (Euclidean distance mean)
        try:
            _, _, disparity = procrustes(p_orig, p_perturbed)
            return disparity # Lower is more REducible (stable)
        except:
            return 0.0

    def compute_reducibility(self):
        """
        Compression Ratio Test: PCA explained variance ratio.
        """
        if self.data is None: self.load_data()
        returns = self.data.pct_change().dropna()
        X = returns.T.values
        
        model = PCA(n_components=min(3, X.shape[1]))
        model.fit(X)
        
        reducibility = np.sum(model.explained_variance_ratio_)
        return reducibility

    def simulate_shock(self, asset, target_value):
        """
        Selective Shock Simulation: Forcing a 'tear' in the manifold.
        Returns a distorted manifold projection.
        """
        if self.data is None: self.load_data()
        df_perturbed = self.data.copy()
        
        if asset in df_perturbed.columns:
            # Apply target value to the last few datapoints to simulate a sudden break
            df_perturbed.iloc[-5:, df_perturbed.columns.get_loc(asset)] = target_value
            
        # Re-calc returns and manifold
        returns = df_perturbed.pct_change().dropna()
        X = returns.T.values
        
        model = PCA(n_components=3)
        projection = model.fit_transform(X)
        
        df_proj = pd.DataFrame(projection, columns=['Dim_1', 'Dim_2', 'Dim_3'])
        df_proj['Asset'] = returns.columns
        if self.metadata:
            df_proj['Type'] = [self.metadata.get(a, 'Unknown') for a in returns.columns]
            
        return df_proj

    # --- SignalAgent ---
    def detect_anomalies(self):
        # Enhanced detection: High correlation + High sensitivity
        if self.data is None: self.load_data()
        returns = self.data.pct_change().dropna()
        avg_corr = returns.corr().mean().mean()
        sensitivity = self.compute_sensitivity()
        
        return avg_corr > 0.7 or sensitivity > 0.2

if __name__ == "__main__":
    engine = ScientificEngine()
    loaded, msg = engine.load_data()
    print(msg)
    if loaded:
        proj = engine.compute_manifold()
        print("Manifold Computed")
        print(proj.head())
        
        G = engine.compute_network()
        print(f"Network Nodes: {len(G.nodes)}, Edges: {len(G.edges)}")
