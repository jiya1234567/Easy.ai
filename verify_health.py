from intelligence.scientific_engine import ScientificEngine

def test_health_manifold():
    print("Testing Health Domain (Cancer Bio-Data)...")
    engine = ScientificEngine(data_path="reports/cancer_bio_data.csv", metadata_path="reports/bio_metadata.json")
    loaded, msg = engine.load_data()
    print(msg)
    
    if loaded:
        print("Computing Bio-Manifold...")
        df = engine.compute_manifold(n_components=2)
        print(f"Bio-Manifold Agents detected: {len(df)}")
        print(df)
        
        # Stability of Bio-Data
        stability = engine.compute_stability()
        print(f"Bio-Manifold Stability Index: {stability*100:.1f}%")

if __name__ == "__main__":
    test_health_manifold()
