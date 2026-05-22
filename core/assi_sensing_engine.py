class ASSISensingEngine:
    """
    Adaptive System State Intelligence (ASSI) Engine.
    Part of the OMEGA-CORE framework.
    Provides ontological classification of environments for agents and robots
    based on sensory entropy, predictability, and manifold instability.
    """
    
    @staticmethod
    def classify_system(entropy, predictability, instability):
        """
        Standard single-modality classification for general domains.
        """
        if entropy < 0.3 and predictability > 0.8 and instability < 0.2:
            return "Reducible"
        elif entropy > 0.7 and predictability < 0.3 and instability > 0.7:
            return "Irreducible"
        elif entropy >= 0.7 and predictability >= 0.4 and 0.2 < instability < 0.8:
            return "Emergent / Biological"
        elif 0.3 <= entropy <= 0.7 and 0.3 <= predictability <= 0.8:
            return "Hybrid (Transitioning)"
        else:
            return "Unknown / Unclassified"

    @staticmethod
    def classify_robotic_system(vision_entropy, touch_entropy, smell_entropy):
        """
        Multi-modal classification for robotic scientific discovery.
        Fuses Vision, Touch, and Smell (Chemical) data.
        """
        # Fuse multi-modal entropies into a global state
        global_entropy = (vision_entropy * 0.4) + (touch_entropy * 0.3) + (smell_entropy * 0.3)
        
        # Variance measures divergence between sensors
        variance = abs(vision_entropy - touch_entropy) + abs(touch_entropy - smell_entropy)
        
        predictability = max(0.1, 1.0 - (global_entropy * 0.8) - (variance * 0.8))
        instability = min(1.0, global_entropy * (1.0 + (variance * 2.0)))

        # Classification Logic
        if global_entropy < 0.3 and predictability > 0.7:
            return "Reducible", global_entropy, predictability, instability
        elif global_entropy >= 0.7 and variance < 0.25:
            # High entropy but sensors are aligned in their complexity (Biological/Emergent)
            return "Emergent / Biological", global_entropy, predictability, instability
        elif global_entropy > 0.7 and variance >= 0.25:
            return "Irreducible", global_entropy, predictability, instability
        elif 0.3 <= global_entropy <= 0.7:
            return "Hybrid (Transitioning)", global_entropy, predictability, instability
        else:
            return "Unknown / Unclassified", global_entropy, predictability, instability

    @staticmethod
    def detect_phase_transition(timeseries_records, threshold=0.15):
        """
        Detects phase transitions in a time-series of ASSI records.

        A phase transition occurs when the rate of change of coherence (dC/dt)
        exceeds the threshold, indicating the system is crossing a stability boundary.

        Args:
            timeseries_records (list): List of dicts, each containing at minimum
                                       'coherence', 'entropy', 'timestep'.
            threshold (float): dC/dt threshold to trigger a transition event.

        Returns:
            dict: Summary of transition events with timestamps, states, and overall verdict.
        """
        events = []
        prev_coherence = None

        for record in timeseries_records:
            coh = record.get("coherence", 1.0)
            ent = record.get("entropy", 0.0)
            ts  = record.get("timestep", "?")
            state = record.get("state", "Unknown")

            dC_dt = abs(coh - prev_coherence) if prev_coherence is not None else 0.0
            prev_coherence = coh

            if dC_dt > threshold:
                events.append({
                    "timestep": ts,
                    "state_at_event": state,
                    "coherence": round(coh, 4),
                    "entropy": round(ent, 4),
                    "dC_dt": round(dC_dt, 4),
                    "alert": "⚠️ PHASE TRANSITION DETECTED"
                })

        # Final verdict
        if not events:
            verdict = "STABLE — No phase transitions detected."
        elif len(events) == 1:
            verdict = f"TRANSITIONING — 1 boundary crossing at {events[0]['timestep']}."
        else:
            verdict = f"CRITICAL — {len(events)} phase transitions detected. System is highly dynamic."

        return {
            "transition_count": len(events),
            "verdict": verdict,
            "events": events
        }

    @staticmethod
    def summarize_domain(domain_dataset):
        """
        Generates a high-level summary of a single domain's benchmark timeseries.

        Args:
            domain_dataset (dict): A single domain dict from universal_emergent_benchmark.json.

        Returns:
            dict: Summary with domain name, category, final state, and transition analysis.
        """
        ts = domain_dataset.get("timeseries", [])
        if not ts:
            return {"error": "No timeseries data found."}

        final = ts[-1]
        transition_summary = ASSISensingEngine.detect_phase_transition(ts)

        return {
            "domain": domain_dataset.get("domain", "Unknown"),
            "company_inspiration": domain_dataset.get("company_inspiration", "Unknown"),
            "category": domain_dataset.get("category", "Unknown"),
            "total_timesteps": len(ts),
            "initial_state": ts[0].get("state", "Unknown"),
            "final_state": final.get("state", "Unknown"),
            "final_entropy": final.get("entropy", 0),
            "final_coherence": final.get("coherence", 0),
            "transition_analysis": transition_summary
        }
