import pandas as pd
import numpy as np
import os
import json

def generate_weather_fire_data():
    os.makedirs("reports", exist_ok=True)
    
    # A. Weather Test Data (Regional)
    weather_data = {
        "Region": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Canberra", "Darwin", "Hobart"],
        "Temperature_C": [31, 24, 34, 39, 37, 29, 33, 19],
        "Humidity": [42, 60, 48, 22, 28, 35, 80, 72],
        "Wind_kmh": [18, 12, 22, 35, 32, 20, 18, 14],
        "Rain_mm": [0, 4, 1, 0, 0, 0, 22, 6],
        "Pressure_hPa": [1008, 1015, 1005, 1002, 1004, 1009, 1006, 1018],
        "Drought_Index": [0.55, 0.30, 0.62, 0.88, 0.82, 0.60, 0.10, 0.18],
        "Satellite_Hotspot_Count": [2, 0, 1, 15, 12, 4, 0, 0],
        "Wind_Direction": [45, 180, 220, 315, 290, 10, 90, 180], # Degrees
        "Storm_Risk": [0.20, 0.10, 0.25, 0.15, 0.18, 0.12, 0.65, 0.08],
        "Flood_Risk": [0.05, 0.08, 0.10, 0.02, 0.03, 0.04, 0.70, 0.05],
        "Fire_Risk": [0.35, 0.12, 0.45, 0.85, 0.78, 0.50, 0.08, 0.05]
    }
    pd.DataFrame(weather_data).to_csv("reports/weather_test_a.csv", index=False)
    
    # B. Temporal Weather Propagation
    temporal_data = {
        "Day": [1, 2, 3, 4, 5, 6, 7],
        "Sydney_Temp": [31, 33, 35, 38, 40, 37, 34],
        "Perth_Temp": [39, 41, 43, 45, 46, 42, 38],
        "Adelaide_Temp": [37, 39, 41, 44, 45, 40, 36],
        "Brisbane_Temp": [34, 35, 36, 38, 39, 36, 33],
        "National_Fire_Risk": [0.42, 0.55, 0.68, 0.82, 0.91, 0.74, 0.50]
    }
    pd.DataFrame(temporal_data).to_csv("reports/weather_propagation_b.csv", index=False)
    
    # C. Fire Test Data
    fire_data = {
        "Location": ["Blue_Mountains", "Perth_Hills", "Adelaide_Hills", "Brisbane_West", "Canberra_Bushland"],
        "Vegetation": ["Forest", "Scrub", "Forest", "Grassland", "Forest"],
        "Dryness": [0.85, 0.95, 0.90, 0.72, 0.82],
        "Fuel_Load": [0.90, 0.88, 0.86, 0.68, 0.80],
        "Wind_kmh": [28, 42, 38, 24, 30],
        "Ignition_Risk": [0.78, 0.95, 0.88, 0.55, 0.72],
        "Population_Exposure": [0.65, 0.55, 0.70, 0.40, 0.50],
        "Fire_Size_ha": [1200, 3500, 2200, 600, 900],
        "Containment": [0.45, 0.20, 0.30, 0.65, 0.50]
    }
    pd.DataFrame(fire_data).to_csv("reports/fire_test_c.csv", index=False)
    
    # F. Weather <-> Energy <-> Economy
    econ_data = {
        "Region": ["Sydney", "Perth", "Adelaide", "Brisbane"],
        "Temperature_C": [40, 46, 45, 39],
        "Electricity_Demand": [0.82, 0.95, 0.91, 0.80],
        "Grid_Stress": [0.70, 0.92, 0.88, 0.72],
        "Power_Outage_Risk": [0.20, 0.55, 0.48, 0.18],
        "Economic_Loss_Million": [15, 65, 48, 12]
    }
    pd.DataFrame(econ_data).to_csv("reports/energy_economy_f.csv", index=False)

def generate_agri_data():
    # Agriculture ASI Test Suite
    agri_data = {
        "Plot_ID": ["Field_001", "Field_002", "Field_003", "Field_004", "Field_005"],
        "Crop": ["Corn", "Corn", "Wheat", "Soybean", "Cotton"],
        "Soil_Nitrogen": [42, 18, 55, 30, 25], # mg/kg
        "Soil_Moisture": [0.12, 0.08, 0.25, 0.35, 0.20], # %
        "Drought_Index": [0.85, 0.92, 0.30, 0.15, 0.40],
        "Pest_Pressure": [0.20, 0.15, 0.80, 0.10, 0.12],
        "Chlorophyll_Index": [0.45, 0.38, 0.75, 0.82, 0.65], # NDVI-like
        "Fertilizer_Cost": [150, 150, 120, 100, 180], # $/ha
        "Projected_Yield": [140, 110, 55, 45, 800], # Bu/Ac or Lbs/Ac
        "Actual_Yield": [138, 105, 52, 44, 790], # Historical Ground Truth
        "Irrigation_Efficiency": [0.85, 0.80, 0.92, 0.95, 0.88],
        "Fire_Buffer_Distance": [50, 20, 100, 200, 30] # meters
    }
    pd.DataFrame(agri_data).to_csv("reports/agri_test_suite.csv", index=False)
    
    # Add metadata for Scientific Engine
    meta = {
        "Temperature_C": "DRIVER", "Humidity": "DRIVER", "Wind_kmh": "DRIVER",
        "Drought_Index": "DRIVER", "Soil_Nitrogen": "DRIVER", "Soil_Moisture": "DRIVER",
        "Satellite_Hotspot_Count": "DRIVER", "Wind_Direction": "DRIVER",
        "Fire_Risk": "PROPERTY", "Economic_Loss_Million": "PROPERTY", "Projected_Yield": "PROPERTY",
        "Actual_Yield": "UNCERTAINTY", "Crop_Health_Score": "PROPERTY", "Electricity_Demand": "PROPERTY"
    }
    with open("reports/omega_test_metadata.json", "w") as f:
        json.dump(meta, f, indent=2)

if __name__ == "__main__":
    print("Generating OMEGA-CORE Weather, Fire & Agri Data Suite...")
    generate_weather_fire_data()
    generate_agri_data()
    print("Success. All datasets saved to reports/")
