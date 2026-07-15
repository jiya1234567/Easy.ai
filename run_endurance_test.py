import time
from omega_bridge_v2 import get_harness_v2
from auto_chain import AutoChain

def main():
    print("Starting 100+ Autonomous Runs Endurance Test...")
    h = get_harness_v2()
    agent = h["agents"]["scientific_discovery"]
    
    chain = AutoChain(
        agent=agent,
        memory=h["memory"],
        reality_anchor=h["reality"],
        context_data_fn=lambda: {"temperature": [20, 21, 22], "humidity": [50, 52, 51], "pressure": [1013, 1013, 1013]},
        planner=h["planner"],
        on_cycle_complete=lambda c: print(f"Cycle {c.cycle_number} completed in {c.duration_seconds}s. Type: {c.question_type}")
    )
    
    chain.start(max_cycles=20)
    chain.state.max_cycles = 100  # override max cycles limit
    
    with open("endurance_test_results.log", "w") as f:
        f.write("Starting Endurance Test - Target: 100 cycles\n")
    
    for i in range(100):
        if not chain.state.running:
            print("Chain stopped unexpectedly.")
            break
            
        print(f"Running cycle {i+1}...")
        cycle = chain.run_next_cycle()
        
        if cycle:
            with open("endurance_test_results.log", "a") as f:
                f.write(f"Cycle {cycle.cycle_number} | Query: {cycle.suggestion_query} | Duration: {cycle.duration_seconds}s\n")
        else:
            print("Cycle returned None, stopping.")
            break
            
    print("Endurance Test Finished.")

if __name__ == "__main__":
    main()
