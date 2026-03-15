import json
class BayesianGuard:
    def update_belief(self, prior, evidence_confidence):
        """Bayesian Inference: P(H|E). Updates system belief based on new photo/data."""
        # Simple Bayesian Update: Adjusts prior belief based on signal strength
        likelihood = evidence_confidence 
        unnormalized_posterior = prior * likelihood
        return round(min(0.99, unnormalized_posterior + (prior * 0.1)), 4)
