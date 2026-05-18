import pandas as pd
import numpy as np
import os
import json

def generate_relativity_datasets():
    os.makedirs("reports/relativity", exist_ok=True)
    c = 299792458  # Speed of light in m/s

    # Phase 1: Classical Newtonian Motion
    # Observers measure relative velocities that add classically.
    classical_data = {
        "Observer": ["A", "B", "C", "D"],
        "Observer_Velocity_mps": [0, 20, 100, 500],
        "Measured_Length_m": [10.0, 10.0, 10.0, 10.0],
        "Measured_Time_s": [5.0, 5.0, 5.0, 5.0],
        "Expected_Relative_V_to_A": [0, 20, 100, 500],
        "Observed_Relative_V_to_A": [0, 20, 100, 500]
    }
    pd.DataFrame(classical_data).to_csv("reports/relativity/phase1_classical.csv", index=False)

    # Phase 2: Constant Light-Speed Injection
    # The anomaly: c is constant regardless of observer velocity.
    light_speed_data = {
        "Observer_Velocity_mps": [0, 100000, 200000, c/2, c*0.9],
        "Expected_Light_Speed_Classical": [c, c + 100000, c + 200000, c + c/2, c + c*0.9],
        "Observed_Light_Speed": [c, c, c, c, c]
    }
    pd.DataFrame(light_speed_data).to_csv("reports/relativity/phase2_constant_c.csv", index=False)

    # Phase 3: Time Dilation Emergence
    # t' = t / sqrt(1 - v^2/c^2)
    velocities_frac_c = np.array([0.0, 0.1, 0.5, 0.866, 0.99])
    earth_time = 10.0
    gamma = 1 / np.sqrt(1 - velocities_frac_c**2)
    traveler_time = earth_time / gamma
    
    time_dilation_data = {
        "Velocity_Fraction_c": velocities_frac_c,
        "Earth_Time_s": [earth_time]*len(velocities_frac_c),
        "Traveler_Time_s": traveler_time,
        "Classical_Expected_Time_s": [earth_time]*len(velocities_frac_c)
    }
    pd.DataFrame(time_dilation_data).to_csv("reports/relativity/phase3_time_dilation.csv", index=False)

    # Phase 4: Length Contraction
    # L = L0 * sqrt(1 - v^2/c^2)
    rest_length = 100.0
    observed_length = rest_length * np.sqrt(1 - velocities_frac_c**2)
    
    length_contraction_data = {
        "Velocity_Fraction_c": velocities_frac_c,
        "Rest_Length_m": [rest_length]*len(velocities_frac_c),
        "Observed_Length_m": observed_length,
        "Classical_Expected_Length_m": [rest_length]*len(velocities_frac_c)
    }
    pd.DataFrame(length_contraction_data).to_csv("reports/relativity/phase4_length_contraction.csv", index=False)

    # Phase 5: Relativity of Simultaneity
    simultaneity_data = {
        "Observer": ["Stationary", "Moving_Right_0.5c", "Moving_Left_0.5c"],
        "Event_A_Time": [5.0, 3.0, 7.0],
        "Event_B_Time": [5.0, 7.0, 3.0],
        "Judged_Simultaneous": [True, False, False]
    }
    pd.DataFrame(simultaneity_data).to_csv("reports/relativity/phase5_simultaneity.csv", index=False)
    
    print("Successfully generated Relativity Discovery datasets in reports/relativity/")

if __name__ == "__main__":
    generate_relativity_datasets()
