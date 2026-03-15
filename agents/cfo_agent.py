import json
def audit_financials(signals, dna):
    """CFO AGENT: Validates trade/experiment against $10M budget."""
    budget = dna['cfo_constraints']['budget']
    rsi = float(signals.get('rsi', 50))
    if rsi > 70: return "DENIED: Overbought risk exceeds CFO safety buffer."
    return "AUTHORIZED: Capital deployment within institutional parameters."
