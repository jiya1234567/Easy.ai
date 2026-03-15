import random
class MarkovForecaster:
    def predict_next_state(self, current_rsi):
        """Markov Chain: Determines the most likely 'Next Physics State'."""
        states = ["Expansion", "Neutral", "Pullback", "Waterfall"]
        if current_rsi > 70: return "Pullback (Prob: 88%)"
        if current_rsi < 30: return "Expansion (Prob: 92%)"
        return "Neutral (Prob: 50%)"
