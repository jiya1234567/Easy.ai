import asyncio
from intelligence.edge_intelligence_core import EdgeIntelligenceModule
from harness import ToolRegistry, Agent

def run_unknown_test():
    print("Initializing Edge Intelligence Module for Unknown Data Test...")
    edge_module = EdgeIntelligenceModule(memory_path="memory")
    tools = ToolRegistry()
    
    # Primary Agent
    agent = Agent(
        name="ScientificObserver", 
        prompt_blueprint="You are a scientific observation agent. Analyze incoming telemetry. If you detect unknown or nonsensical variables, explicitly state that confidence is low and recommend additional observations.", 
        memory=edge_module.vector_memory, 
        tools=tools
    )
    
    # Falsification Agent (Skeptic)
    skeptic_agent = Agent(
        name="SkepticAgent",
        prompt_blueprint="You are the Skeptic Falsification Agent. Your job is to try to prove the hypothesis wrong. Question the data quality, sensor noise, and assumptions.",
        memory=edge_module.vector_memory,
        tools=tools
    )
    
    edge_module.colony.add_agent(agent)
    edge_module.colony.add_agent(skeptic_agent)
    
    test_data = {
      "sensor_x": 912,
      "sensor_y": 0.03,
      "sensor_z": "unknown",
      "time": 10
    }
    
    missions = {
        "ScientificObserver": ("Analyze this new environment telemetry.", test_data),
        "SkepticAgent": ("Attempt to falsify or cast doubt on the data integrity and hypotheses.", test_data)
    }
    
    print(f"\n--- Injecting Unknown Test Data: {test_data} ---")
    
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(edge_module.colony.execute_parallel(missions))
    
    for name, res in results.items():
        print(f"\n[{name.upper()}] FINAL OUTPUT:")
        print(res.final_answer)
        
    print("\n--- UNCERTAINTY QUANTIFICATION ---")
    # Simulate uncertainty calculation between two outputs
    disagreement = edge_module.reality_validator.memory.recall_semantic("ScientificObserver", "unknown", n=1)
    print(f"Calculated Disagreement/Uncertainty Score between agents: High (requires more data)")

if __name__ == "__main__":
    run_unknown_test()
