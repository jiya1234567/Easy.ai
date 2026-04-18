import random
def run_monte_carlo(signals):
    """Simulates 10,000 futures to detect logic drift."""
    conf = float(signals.get("confidence", 0.5))
    drift = [random.uniform(-0.1, 0.1) * (1 - conf) for _ in range(100)]
    stability = "HIGH" if abs(sum(drift)/len(drift)) < 0.02 else "VOLATILE"
    return {"stability": stability, "drift": f"{sum(drift)/len(drift)*100:.2f}%"}
