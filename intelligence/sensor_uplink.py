import pandas as pd
import numpy as np
import json
import os

class SensorUplink:
    """
    Handles streaming data from Satellite (Thermal/Weather) and Drone (Multi-spectral) nodes.
    """
    def __init__(self, weather_data_path="reports/weather_test_a.csv", agri_data_path="reports/agri_test_suite.csv"):
        self.weather_path = weather_data_path
        self.agri_path = agri_data_path
        
    def get_satellite_hotspots(self):
        """
        Retrieves thermal anomalies from satellite telemetry.
        """
        df = pd.read_csv(self.weather_path)
        hotspots = df[['Region', 'Satellite_Hotspot_Count', 'Wind_Direction', 'Fire_Risk']]
        
        # Identity Critical Hotspots
        critical = hotspots[hotspots['Satellite_Hotspot_Count'] > 10].to_dict('records')
        
        return {
            "source": "Sentinel-2 / MODIS Uplink",
            "active_anomalies": len(critical),
            "telemetry": critical,
            "system_status": "MONITORING" if len(critical) < 5 else "CRITICAL_ALERT"
        }

    def get_drone_ndiv(self, plot_id="Field_001"):
        """
        Simulates high-resolution multispectral scanning from field drones.
        NDVI = (NIR - Red) / (NIR + Red)
        """
        # In our simulation, we reference the Chlorophyll_Index from the Agri dataset
        df = pd.read_csv(self.agri_path)
        plot_data = df[df['Plot_ID'] == plot_id].iloc[0]
        
        ndvi = plot_data['Chlorophyll_Index']
        
        # Add some simulated high-res noise
        jitter = np.random.normal(0, 0.02)
        current_ndvi = max(0, min(1.0, ndvi + jitter))
        
        status = "Healthy" if current_ndvi > 0.7 else "Stress Detected" if current_ndvi > 0.4 else "Critical Decay"
        
        return {
            "node": "Drone-04 (Field Segment Alpha)",
            "altitude_m": 45,
            "NDVI_mean": round(current_ndvi, 3),
            "status": status,
            "canopy_coverage": "88%",
            "timestamp": "2026-04-16T18:40:00Z"
        }

    def calculate_fire_propagation_vector(self, region="Perth"):
        """
        Calculates the expected fire spread based on hotspots and wind direction.
        """
        df = pd.read_csv(self.weather_path)
        data = df[df['Region'] == region].iloc[0]
        
        hotspots = data['Satellite_Hotspot_Count']
        wind_dir = data['Wind_Direction']
        wind_speed = data['Wind_kmh']
        
        # Simple vector magnitude for risk propagation
        propagation_force = (hotspots * 0.5) + (wind_speed * 1.2)
        
        return {
            "region": region,
            "vector_direction": wind_dir,
            "magnitude_index": round(propagation_force, 2),
            "impact_zone": "NE Quadrant" if 0 <= wind_dir <= 90 else "SE Quadrant" if 90 < wind_dir <= 180 else "SW Quadrant" if 180 < wind_dir <= 270 else "NW Quadrant"
        }

if __name__ == "__main__":
    uplink = SensorUplink()
    print("--- Satellite Hotspot Report ---")
    print(json.dumps(uplink.get_satellite_hotspots(), indent=2))
    print("\n--- Drone NDVI Scan (Field_001) ---")
    print(json.dumps(uplink.get_drone_ndiv(), indent=2))
