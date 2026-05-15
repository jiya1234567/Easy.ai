import os
import json

class ResourceManager:
    """
    Manages the 'Cognitive Metabolism' of the ASI framework.
    Enforces computational and attention constraints.
    """
    def __init__(self, compute_budget=1.0, attention_budget=1.0):
        self.compute_budget = compute_budget  # 0.0 to 1.0
        self.attention_budget = attention_budget # 0.0 to 1.0
        self.memory_pressure = 0.0

    def calculate_memory_pressure(self, node_count):
        """
        Determines memory pressure based on manifold complexity.
        """
        self.memory_pressure = min(1.0, node_count / 1000.0)
        return self.memory_pressure

    def get_pruning_threshold(self):
        """
        Calculates a threshold for pruning low-influence nodes.
        If attention budget is low, we prune more aggressively.
        """
        # Threshold moves between 0.1 and 0.5 based on attention budget
        return 0.1 + (1.0 - self.attention_budget) * 0.4

    def get_max_recursion_depth(self):
        """
        Determines how many loops we can afford.
        """
        return max(1, int(self.compute_budget * 10))

    def get_resource_state(self):
        """
        Returns the current mechanistic resource state.
        """
        return {
            "compute_budget": self.compute_budget,
            "attention_budget": self.attention_budget,
            "memory_pressure": self.memory_pressure,
            "compression_ratio": round(1.0 - (self.attention_budget * 0.5), 2)
        }

if __name__ == "__main__":
    rm = ResourceManager(compute_budget=0.5, attention_budget=0.3)
    print("Resource State:", rm.get_resource_state())
    print("Pruning Threshold:", rm.get_pruning_threshold())
    print("Max Depth:", rm.get_max_recursion_depth())
