"""
OMEGA-CORE Stage 13 — State Tensor Engine
==========================================
The State Tensor Engine represents the multi-dimensional cognitive 
and physical state of the Universal Lab at any given moment.

Instead of tracking state as flat dictionaries, it embeds system 
parameters (causality, uncertainty, observation deltas) into 
N-dimensional mathematical tensors. This enables geometric computations, 
Euclidean distance metrics between reality branches, and loss 
calculations across continuous time trajectories.
"""
import time
import uuid
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class TensorSnapshot:
    id: str
    domain: str
    timestamp: float
    # Tensors are typically shape (Features, Branches, Time) or similar
    state_matrix: np.ndarray
    uncertainty_matrix: np.ndarray
    feature_names: List[str]
    metadata: Dict[str, Any]

class StateTensorEngine:
    """
    Maintains the N-dimensional state representation of the Universal Lab.
    """
    def __init__(self, history_limit: int = 1000):
        self._tensor_history: List[TensorSnapshot] = []
        self._history_limit = history_limit
        self._domain_registries: Dict[str, List[str]] = {}
        
    def register_domain_features(self, domain: str, features: List[str]):
        """Define the feature space axis (dimensions) for a specific domain."""
        self._domain_registries[domain] = features
        
    def embed_state(self, domain: str, state_dict: Dict[str, float], uncertainty_dict: Dict[str, float] = None) -> TensorSnapshot:
        """
        Embeds a flat state dictionary into the geometric N-dimensional tensor space.
        """
        if domain not in self._domain_registries:
            # Auto-register if not defined
            self.register_domain_features(domain, list(state_dict.keys()))
            
        features = self._domain_registries[domain]
        
        # Build 1D Tensors (Vectors) for the current snapshot
        state_vec = np.zeros(len(features))
        unc_vec = np.zeros(len(features))
        
        for i, feature in enumerate(features):
            state_vec[i] = state_dict.get(feature, 0.0)
            if uncertainty_dict:
                unc_vec[i] = uncertainty_dict.get(feature, 0.0)
                
        snapshot = TensorSnapshot(
            id=f"TSR-{uuid.uuid4().hex[:8].upper()}",
            domain=domain,
            timestamp=time.time(),
            state_matrix=state_vec,
            uncertainty_matrix=unc_vec,
            feature_names=features,
            metadata={"source": "embed_state"}
        )
        
        self._tensor_history.append(snapshot)
        if len(self._tensor_history) > self._history_limit:
            self._tensor_history.pop(0)
            
        return snapshot

    def calculate_branch_divergence(self, base_snapshot: TensorSnapshot, branch_snapshot: TensorSnapshot) -> float:
        """
        Calculates the Euclidean distance (L2 norm) between two reality branches
        in the tensor space, representing how far a counterfactual diverged.
        """
        if base_snapshot.domain != branch_snapshot.domain:
            raise ValueError("Cannot compute divergence across different domains.")
            
        # Euclidean distance
        diff = base_snapshot.state_matrix - branch_snapshot.state_matrix
        distance = np.linalg.norm(diff)
        return float(distance)
        
    def get_domain_trajectory_tensor(self, domain: str) -> np.ndarray:
        """
        Returns a 2D Tensor (Time x Features) tracking the domain's evolution.
        Useful for feeding into Transformer layers or LSTM models.
        """
        snapshots = [s for s in self._tensor_history if s.domain == domain]
        if not snapshots:
            return np.array([])
            
        return np.vstack([s.state_matrix for s in snapshots])
        
    def summary(self) -> Dict[str, Any]:
        return {
            "total_snapshots": len(self._tensor_history),
            "domains_tracked": list(self._domain_registries.keys()),
            "tensor_dimensions": {d: len(f) for d, f in self._domain_registries.items()}
        }

if __name__ == "__main__":
    ste = StateTensorEngine()
    ste.register_domain_features("finance", ["interest_rate", "gold", "tech_return", "vix"])
    
    # State t=0
    snap1 = ste.embed_state("finance", {"interest_rate": 4.0, "gold": 1950, "tech_return": 0.5, "vix": 14})
    # State t=1 (Regime shift)
    snap2 = ste.embed_state("finance", {"interest_rate": 5.0, "gold": 1880, "tech_return": -2.0, "vix": 25})
    
    div = ste.calculate_branch_divergence(snap1, snap2)
    print(f"Euclidean Tensor Divergence (L2 Norm): {div:.2f}")
    
    traj = ste.get_domain_trajectory_tensor("finance")
    print("Trajectory Tensor Shape (Time x Features):", traj.shape)
