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
        self.causal_graph = None # Persistent intelligence state
        
    # --- DataAgent ---
    def load_data(self):
        if not os.path.exists(self.data_path):
            return False, "Data file missing."
        # Load data with dayfirst=True to avoid dateutil warnings on Windows
        self.data = pd.read_csv(self.data_path, index_col=0, parse_dates=True, dayfirst=True)
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

    # --- Universal Ontology (NEW) ---
    def get_ontology_map(self):
        """
        Maps domain-specific columns to Universal Scientific Roles.
        """
        if self.data is None: self.load_data()
        cols = self.data.columns.tolist()
        
        # Universal Role Definitions
        ontology = {
            "DRIVER": ["Atomic_Structure", "Grain_Size", "Nano_Coating", "Pressure_Processing", "Interest_Rate", "Market_Sentiment", "Mutation_Level", "Magnetic_Bias", "Pulse_Duration", "Vacuum_Pressure", "Atomic_Spin", "Patch_Level", "Open_Ports", "User_Privilege_Level", "External_Connections", "Energy_Demand", "Traffic_Load", "Water_Consumption", "Packet_Rate", "Temperature_C", "Humidity", "Wind_kmh", "Rain_mm", "Pressure_hPa", "Drought_Index", "Soil_Nitrogen", "Soil_Moisture", "Irrigation_Volume", "Fertilizer_Type"],
            "PROPERTY": ["Conductivity", "Strength", "Elasticity", "Thermal_Stability", "Defect_Score", "RSI", "Price", "Expression_Level", "Coherence_Time", "Fidelity", "Qubit_Stability", "Phase_Shift", "Energy_State", "Traffic_Volume", "Packet_Entropy", "Failed_Logins", "CPU_Usage", "Anomaly_Score", "Grid_Frequency", "Voltage_Level", "Traffic_Flow_Rate", "Water_Pressure", "Comms_Latency", "Fire_Risk", "Storm_Risk", "Flood_Risk", "Ignition_Risk", "Population_Exposure", "Fire_Size_ha", "Electricity_Demand", "Grid_Stress", "Power_Outage_Risk", "Economic_Loss_Million", "Projected_Yield", "Crop_Health_Score", "Disease_Severity", "Smoke_Index", "PM25", "Hospital_Load", "Respiratory_Risk", "Evacuation_Risk"],
            "INTERVENTION": ["Treatment_Temperature", "Treatment_Time", "Doping_Level", "Asset_Allocation", "Dosage", "Laser_Intensity", "Cryo_Temperature", "Microwave_Frequency", "Attack_Type", "Payload_Intensity", "Mitigation_Action", "Load_Shedding", "Signal_Timing", "Valve_Control", "Route_Reoptimization", "Throttle_Bandwidth", "Containment"],
            "DYNAMICS": ["Time_Cycle", "Degradation_Rate", "Performance_After_Stress", "Volatility", "Half_Life", "Decoherence_Rate", "Relaxation_Time", "Measurement_Count", "Anomaly_Growth", "System_Degradation", "Failure_Spread_Rate", "Recovery_Metric", "System_Inertia"],
            "NETWORK": ["Composite_Mix_Ratio", "Interface_Bond_Strength", "Layer_Depth", "Centrality", "Connectivity", "Entanglement_Entropy", "Coupler_Strength", "Qubit_Connectivity", "Lateral_Movement_Risk", "Connected_Nodes", "Influence_Score", "Grid_Topology", "Backhaul_Connectivity", "Pipeline_Adjacency"],
            "UNCERTAINTY": ["Measurement_Error", "Confidence_Score", "Standard_Deviation", "P_Value", "Readout_Error", "Quantum_Noise", "Gate_Fidelity_Error", "False_Positive_Rate", "Sensor_Noise", "Detection_Confidence", "Sensor_Bias", "Telemetry_Noise"]
        }
        
        mapping = {k: [c for c in cols if any(keyword in c for keyword in v)] for k, v in ontology.items()}
        return mapping

    def discover_causality(self, threshold=0.4):
        """
        Probabilistic Causal Discovery.
        Adjusts weights based on Uncertainty (Measurement Error / Confidence).
        """
        if self.data is None: self.load_data()
        numeric_df = self.data.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()
        ontology = self.get_ontology_map()
        
        # Extract uncertainty weights if available
        u_cols = ontology.get("UNCERTAINTY", [])
        u_weight = 1.0
        if u_cols:
            # Average confidence score as a global multiplier for weights
            if "Confidence_Score" in u_cols:
                u_weight = self.data["Confidence_Score"].mean()
            elif "Measurement_Error" in u_cols:
                u_weight = 1.0 - self.data["Measurement_Error"].mean()

        causal_graph = nx.DiGraph()
        cols = corr_matrix.columns
        for i in range(len(cols)):
            for j in range(len(cols)):
                if i != j:
                    u, v = cols[i], cols[j]
                    c = corr_matrix.iloc[i, j]
                    
                    # Apply Probabilistic Weighting
                    prob_weight = c * u_weight
                    
                    if abs(prob_weight) > threshold:
                        # Ontology-based Directionality
                        is_causal = False
                        if u in ontology["DRIVER"] and v in ontology["PROPERTY"]: is_causal = True
                        elif u in ontology["INTERVENTION"] and (v in ontology["PROPERTY"] or v in ontology["DYNAMICS"]): is_causal = True
                        elif u in ontology["NETWORK"] and v in ontology["PROPERTY"]: is_causal = True
                        elif abs(prob_weight) > threshold + 0.3: is_causal = True
                        
                        if is_causal:
                            # Store both the weight and the uncertainty (1 - u_weight)
                            causal_graph.add_edge(u, v, weight=prob_weight, uncertainty=1.0 - u_weight)
                            
        self.causal_graph = causal_graph
        return causal_graph

    # --- Learning Loop Agent (NEW) ---
    def learn_from_ground_truth(self, target_node="Projected_Yield", ground_truth_node="Actual_Yield"):
        """
        Adjusts causal weights based on the delta between predicted and ground truth.
        Implements a simple Bayesian update style for weight refinement.
        """
        if self.data is None: self.load_data()
        if self.causal_graph is None: self.discover_causality()
        
        if ground_truth_node not in self.data.columns:
            return False, f"Ground truth node {ground_truth_node} missing from dataset."
            
        # Calculate global prediction error
        error = (self.data[target_node] - self.data[ground_truth_node]).mean()
        error_norm = error / self.data[target_node].mean()
        
        # Back-propagate adjustment to all drivers of the target node
        drivers = [u for u, v in self.causal_graph.edges() if v == target_node]
        
        audit_trail = []
        for u in drivers:
            old_weight = self.causal_graph[u][target_node]['weight']
            # Adjust weight: if predicted > actual, we over-estimated the driver's positive impact
            # Learning rate 0.1
            adjustment = -0.1 * error_norm * old_weight
            new_weight = old_weight + adjustment
            self.causal_graph[u][target_node]['weight'] = new_weight
            
            audit_trail.append({
                "driver": u,
                "old_weight": round(old_weight, 4),
                "new_weight": round(new_weight, 4),
                "delta": round(adjustment, 4)
            })
            
        return True, audit_trail

    # --- Probabilistic Causal Engine (NEW) ---
    def simulate_intervention(self, target_node, intervention_value, graph=None):
        """
        Simulates an intervention with PROBABILISTIC UNCERTAINTY PROPAGATION.
        Returns: {node: {"old": X, "new": Y, "delta": Z, "uncertainty": U}}
        """
        if self.data is None: self.load_data()
        if graph is None:
            graph = self.discover_causality()
            
        if target_node not in graph.nodes:
            return None, f"Node {target_node} not in causal graph."
            
        baseline = self.data.select_dtypes(include=[np.number]).iloc[-1].to_dict()
        if target_node not in baseline:
            return None, f"Node {target_node} not found in dataset."
            
        projected_state = baseline.copy()
        delta = intervention_value - baseline[target_node]
        projected_state[target_node] = intervention_value
        
        # Propagation with Uncertainty
        impacted_nodes = list(graph.successors(target_node))
        results = {"intervention": {"node": target_node, "value": intervention_value, "delta": delta}, "projections": {}}
        
        for node in impacted_nodes:
            edge_data = graph[target_node][node]
            weight = edge_data['weight']
            # Causal Uncertainty = Base Edge Uncertainty + Variable Variance
            edge_uncertainty = edge_data.get('uncertainty', 0.1)
            
            projected_state[node] += delta * weight
            
            results["projections"][node] = {
                "old": baseline[node],
                "new": projected_state[node],
                "delta": projected_state[node] - baseline[node],
                "uncertainty_level": f"±{abs(delta * edge_uncertainty):.4f}"
            }
            
        return results, "Probabilistic intervention simulated successfully."

    def compute_silhouette(self, n_clusters=2):
        from sklearn.metrics import silhouette_score
        if self.data is None: self.load_data()
        numeric_df = self.data.select_dtypes(include=[np.number])
        ontology = self.get_ontology_map()
        cluster_df = numeric_df.drop(columns=ontology.get("UNCERTAINTY", []), errors='ignore')

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(cluster_df)
        score = silhouette_score(cluster_df, labels)
        return score

    def compute_stability(self, method='PCA', window_size=50):
        if self.data is None: self.load_data()
        numeric_df = self.data.select_dtypes(include=[np.number])
        returns = numeric_df.diff().dropna()
        if len(returns) < window_size * 2: return 1.0
        w1 = returns.iloc[:window_size].T.values
        w2 = returns.iloc[-window_size:].T.values
        model = PCA(n_components=min(3, w1.shape[1], w2.shape[1]))
        try:
            p1 = model.fit_transform(w1)
            p2 = model.fit_transform(w2)
            _, _, disparity = procrustes(p1, p2)
            return max(0, 1 - (disparity * 5))
        except: return 1.0

    def compute_sensitivity(self, epsilon=0.01):
        if self.data is None: self.load_data()
        numeric_df = self.data.select_dtypes(include=[np.number])
        X = numeric_df.T.values
        model = PCA(n_components=min(3, X.shape[1]))
        try:
            p_orig = model.fit_transform(X)
            X_perturbed = X + np.random.normal(0, epsilon, X.shape)
            p_perturbed = model.fit_transform(X_perturbed)
            _, _, disparity = procrustes(p_orig, p_perturbed)
            return disparity
        except: return 0.0

    def compute_reducibility(self):
        if self.data is None: self.load_data()
        numeric_df = self.data.select_dtypes(include=[np.number])
        X = numeric_df.T.values
        model = PCA(n_components=min(3, X.shape[1]))
        try:
            model.fit(X)
            return np.sum(model.explained_variance_ratio_)
        except: return 1.0

    def simulate_shock(self, asset, target_value):
        if self.data is None: self.load_data()
        df_perturbed = self.data.copy()
        numeric_cols = df_perturbed.select_dtypes(include=[np.number]).columns
        if asset in numeric_cols:
            df_perturbed.iloc[-5:, df_perturbed.columns.get_loc(asset)] = target_value
        returns = df_perturbed[numeric_cols].diff().dropna()
        X = returns.T.values
        model = PCA(n_components=min(3, X.shape[1]))
        projection = model.fit_transform(X)
        df_proj = pd.DataFrame(projection, columns=['Dim_1', 'Dim_2', 'Dim_3'])
        df_proj['Asset'] = returns.columns
        if self.metadata:
            df_proj['Type'] = [self.metadata.get(a, 'Unknown') for a in returns.columns]
        return df_proj

if __name__ == "__main__":
    engine = ScientificEngine(data_path="reports/materials_test.csv")
    loaded, msg = engine.load_data()
    print(msg)
    if loaded:
        print("Universal Ontology Map:", engine.get_ontology_map())
        G = engine.discover_causality()
        print(f"Probabilistic Discovery: {len(G.edges())} paths found.")
        
        # Test Probabilistic Intervention
        if "Treatment_Temperature" in G.nodes:
            res, m = engine.simulate_intervention("Treatment_Temperature", 1000.0, graph=G)
            print("Intervention Result (with Uncertainty):")
            for node, data in res["projections"].items():
                print(f"  {node}: Delta={data['delta']:.2f} | Uncertainty={data['uncertainty_level']}")
