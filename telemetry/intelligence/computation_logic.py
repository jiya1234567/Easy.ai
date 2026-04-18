class IrreducibilityAuditor:
    def check_complexity(self, iq, steps_count):
        """Determines if the problem is 'Reducible' (Simulatable) or 'Irreducible' (Must be Lived)."""
        if iq > 180:
            return "REDUCIBLE: High-IQ shortcut found. Skipping to result."
        return "IRREDUCIBLE: Quantum complexity detected. All 90 steps must be executed."
