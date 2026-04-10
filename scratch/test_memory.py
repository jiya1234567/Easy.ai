import sys, os, json
sys.path.append(os.getcwd())
from kernel import CognitiveMemory, record_outcome

test_file = "intelligence/test_experience.json"
if os.path.exists(test_file): os.remove(test_file)

print("--- Testing Cognitive Memory ---")
# Step 1: Store an episode
mem = CognitiveMemory(test_file)
ctx = {"regime": "Analytical Baseline"}
dec = {"markov": "STABLE"}
eid = mem.store(ctx, dec)
print(f"Stored episode: {eid}")

# Step 2: Record Outcome (updates file)
print("\n--- Recording Success in File ---")
record_outcome(eid, "Success", test_file)

# Step 3: Recall in a NEW instance (simulating next app run)
print("\n--- Testing Recall in NEW instance ---")
mem2 = CognitiveMemory(test_file)
bias, rate = mem2.recall("Analytical Baseline")
print(f"Recall: Bias={bias}, Rate={rate}")

if bias == "Aggressive":
    print("\nSUCCESS: Cognitive adaptation verified.")
else:
    print("\nFAILURE: Cognitive adaptation failed.")
