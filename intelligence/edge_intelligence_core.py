import json
import time
import asyncio
import threading
import uuid
import numpy as np
from typing import Any, Callable, Optional, Dict, List
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

# Import base classes from the OMEGA harness
from harness import MemoryLayer, MemoryEntry, Agent, AgentResult

# ─────────────────────────────────────────────────────────────────
# GAP 2: VECTOR MEMORY LAYER
# ─────────────────────────────────────────────────────────────────
class VectorMemoryLayer(MemoryLayer):
    """
    Upgraded Memory Layer with Semantic Vector Search.
    Fixes Gap 2 by finding conceptually similar memories rather than just exact keywords.
    (Uses TF-IDF + Cosine Similarity as a lightweight, native ChromaDB/FAISS alternative)
    """
    def __init__(self, path: str = "memory"):
        super().__init__(path)
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def recall_semantic(self, agent: str, query: str, n: int = 5) -> List[MemoryEntry]:
        """Semantic vector search for conceptually similar memories."""
        entries = self._load(agent)
        if not entries:
            return []
            
        texts = [e.content for e in entries]
        try:
            # Fit TF-IDF on all memories and transform query
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            query_vec = self.vectorizer.transform([query])
            
            # Calculate cosine similarity
            similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
            
            # Sort by highest similarity
            top_indices = similarities.argsort()[::-1]
            
            # Filter matches with a similarity threshold > 0.05
            scored = [(similarities[i], entries[i]) for i in top_indices if similarities[i] > 0.05]
            
            # Sort by score then timestamp
            scored.sort(key=lambda x: (-x[0], -x[1].timestamp))
            return [e for _, e in scored[:n]]
        except Exception as e:
            # Fallback to keyword search if vectorization fails
            print(f"Vector search failed: {e}. Falling back to keyword recall.")
            return super().recall(agent, query, n)

# ─────────────────────────────────────────────────────────────────
# GAP 3: UNCERTAINTY QUANTIFICATION
# ─────────────────────────────────────────────────────────────────
class UncertaintyQuantifier:
    """
    Calculates Epistemic Uncertainty via Ensemble Disagreement.
    Compares Mistral (Primary) and Phi3 (Challenger) outputs to compute calibrated confidence.
    """
    @staticmethod
    def calculate_disagreement(primary_text: str, challenger_text: str) -> float:
        if not challenger_text:
            return 0.5  # Neutral uncertainty if no challenger
            
        # Use difflib sequence matcher to calculate similarity ratio
        # Lower similarity = Higher disagreement = Higher uncertainty
        matcher = difflib.SequenceMatcher(None, primary_text.lower(), challenger_text.lower())
        similarity = matcher.ratio()
        
        # Uncertainty is the inverse of similarity
        uncertainty_score = 1.0 - similarity
        
        # Calibrate: 0.0 (total agreement) to 1.0 (total disagreement)
        return round(max(0.0, min(1.0, uncertainty_score)), 3)

# ─────────────────────────────────────────────────────────────────
# GAP 4: REALITY VALIDATOR (GROUND TRUTH FEEDBACK)
# ─────────────────────────────────────────────────────────────────
class RealityValidator:
    """
    Reality anchor that closes the loop back to ground truth.
    Compares predicted outcomes with actual sensor readings.
    """
    def __init__(self, memory_layer: VectorMemoryLayer):
        self.memory = memory_layer
        self.pending_hypotheses: Dict[str, Dict] = {}

    def register_prediction(self, agent: str, prediction_text: str, target_metric: str, expected_direction: str):
        """Registers a prediction to be validated later."""
        pid = uuid.uuid4().hex[:8]
        self.pending_hypotheses[pid] = {
            "agent": agent,
            "prediction": prediction_text,
            "target_metric": target_metric, # e.g. "temperature"
            "expected_direction": expected_direction, # "up", "down", "stable"
            "timestamp": time.time(),
            "confidence": 1.0 # Will be adjusted based on reality
        }
        return pid

    def validate_against_reality(self, current_sensor_data: Dict[str, Any]) -> List[Dict]:
        """Checks pending predictions against actual reality data."""
        results = []
        resolved_pids = []
        
        for pid, hyp in self.pending_hypotheses.items():
            metric = hyp["target_metric"]
            if metric in current_sensor_data:
                actual_value = current_sensor_data[metric]
                expected = hyp["expected_direction"]
                
                # Simplified evaluation logic
                is_correct = False
                if expected == "up" and actual_value > 0: is_correct = True
                elif expected == "down" and actual_value < 0: is_correct = True
                elif expected == "stable" and abs(actual_value) < 0.1: is_correct = True
                
                # Adjust confidence
                adjusted_confidence = min(1.0, hyp["confidence"] + 0.2) if is_correct else max(0.0, hyp["confidence"] - 0.3)
                
                result = {
                    "pid": pid,
                    "agent": hyp["agent"],
                    "prediction": hyp["prediction"],
                    "actual": actual_value,
                    "is_correct": is_correct,
                    "adjusted_confidence": adjusted_confidence
                }
                results.append(result)
                
                # Write back to memory
                status = "CONFIRMED" if is_correct else "PRUNED"
                self.memory.write(
                    hyp["agent"], 
                    "reality_feedback", 
                    f"[{status}] Hypothesis: {hyp['prediction']} | Actual: {actual_value} | New Confidence: {adjusted_confidence}",
                    metadata={"pid": pid, "is_correct": is_correct}
                )
                
                resolved_pids.append(pid)
                
        # Remove resolved
        for pid in resolved_pids:
            del self.pending_hypotheses[pid]
            
        return results

# ─────────────────────────────────────────────────────────────────
# GAP 6: SELF-IMPROVEMENT LOOP (BLUEPRINT MUTATION)
# ─────────────────────────────────────────────────────────────────
class BlueprintMutator:
    """
    Updates the agent's prompt blueprint based on reality feedback history.
    """
    def __init__(self, memory_layer: VectorMemoryLayer):
        self.memory = memory_layer
        
    def mutate_blueprint(self, agent: str, current_blueprint: str) -> str:
        """Adapts the prompt based on past failures and successes."""
        recent_feedback = [e for e in self.memory.recent(agent, n=20) if e.role == "reality_feedback"]
        
        if len(recent_feedback) < 3:
            return current_blueprint # Not enough data to mutate
            
        pruned_count = sum(1 for e in recent_feedback if "PRUNED" in e.content)
        confirmed_count = sum(1 for e in recent_feedback if "CONFIRMED" in e.content)
        
        mutation_note = ""
        if pruned_count > confirmed_count:
            mutation_note = "\n\n[SYSTEM ADAPTATION]: Your recent hypotheses have failed reality checks. Be more conservative, rely heavily on actual data, and avoid speculative leaps."
        elif confirmed_count >= pruned_count and confirmed_count > 0:
            mutation_note = "\n\n[SYSTEM ADAPTATION]: Your predictive accuracy is high. Continue leveraging causal chains and expanding hypothesis scope."
            
        # Avoid duplicate notes
        if "[SYSTEM ADAPTATION]" in current_blueprint:
            base = current_blueprint.split("\n\n[SYSTEM ADAPTATION]")[0]
            return base + mutation_note
        else:
            return current_blueprint + mutation_note

# ─────────────────────────────────────────────────────────────────
# GAP 5: AGENT COLONY PARALLELISM
# ─────────────────────────────────────────────────────────────────
class EdgeAgentColony:
    """
    Multi-threaded agent executor with message bus for inter-agent communication.
    """
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.message_bus = asyncio.Queue()
        self.results: Dict[str, AgentResult] = {}
        
    def add_agent(self, agent: Agent):
        self.agents[agent.name] = agent
        
    async def _run_agent_async(self, agent: Agent, query: str, context_data: Dict[str, Any]):
        """Runs an agent in a background thread to prevent blocking."""
        loop = asyncio.get_event_loop()
        # Execute the synchronous agent.run in a thread pool
        result = await loop.run_in_executor(None, agent.run, query, context_data)
        self.results[agent.name] = result
        
        # Publish finding to the message bus
        await self.message_bus.put({
            "from": agent.name,
            "finding": result.final_answer,
            "timestamp": time.time()
        })
        return result
        
    async def execute_parallel(self, missions: Dict[str, tuple[str, Dict[str, Any]]]):
        """Runs multiple agents in parallel."""
        tasks = []
        for agent_name, (query, context_data) in missions.items():
            if agent_name in self.agents:
                task = asyncio.create_task(self._run_agent_async(self.agents[agent_name], query, context_data))
                tasks.append(task)
                
        await asyncio.gather(*tasks)
        return self.results

# ─────────────────────────────────────────────────────────────────
# GAP 1: CONTINUOUS SENSOR LOOP
# ─────────────────────────────────────────────────────────────────
class EdgeIntelligenceModule:
    """
    The fully integrated Edge Intelligence Module resolving all 6 gaps.
    """
    def __init__(self, memory_path: str = "memory"):
        self.vector_memory = VectorMemoryLayer(path=memory_path)
        self.reality_validator = RealityValidator(self.vector_memory)
        self.mutator = BlueprintMutator(self.vector_memory)
        self.colony = EdgeAgentColony()
        
        self.is_live = False
        self._sensor_thread: Optional[threading.Thread] = None
        self._loop_interval = 30 # seconds
        
        # Core state
        self.latest_sensor_data: Dict[str, Any] = {}
        
    def toggle_live_mode(self, active: bool, interval_sec: int = 30, sensor_callback: Optional[Callable] = None):
        """Switches between manual and continuous live sensor loop."""
        self.is_live = active
        self._loop_interval = interval_sec
        
        if self.is_live:
            if self._sensor_thread is None or not self._sensor_thread.is_alive():
                self._sensor_thread = threading.Thread(target=self._continuous_loop, args=(sensor_callback,), daemon=True)
                self._sensor_thread.start()
                print("âœ… Live Sensor Loop STARTED.")
        else:
            print("â›” Live Sensor Loop STOPPED (Manual Mode).")

    def _continuous_loop(self, sensor_callback: Optional[Callable]):
        """Background thread executing the full discovery loop."""
        while self.is_live:
            print(f"\n[{time.strftime('%H:%M:%S')}] Executing Autonomous Edge Loop...")
            
            # 1. Fetch live data
            if sensor_callback:
                self.latest_sensor_data = sensor_callback()
            else:
                # Simulated telemetry if no callback provided
                self.latest_sensor_data = {
                    "temperature": np.random.normal(25, 2),
                    "system_load": np.random.uniform(10, 90),
                    "anomaly_score": np.random.uniform(0.0, 1.0)
                }
            
            # 2. Reality Feedback Loop (Gap 4)
            validation_results = self.reality_validator.validate_against_reality(self.latest_sensor_data)
            for res in validation_results:
                print(f"  Reality Check [{res['agent']}]: {'âœ…' if res['is_correct'] else 'â Œ'} {res['adjusted_confidence']:.2f}")

            # 3. Parallel Colony Execution (Gap 5)
            # In a real scenario, missions would be dynamically generated
            # Here we just run any agents currently in the colony
            if self.colony.agents:
                missions = {
                    name: ("Analyze current sensor telemetry and identify causal anomalies.", self.latest_sensor_data)
                    for name in self.colony.agents.keys()
                }
                
                # Apply Blueprint Mutation (Gap 6) before running
                for name, agent in self.colony.agents.items():
                    agent.prompt_blueprint = self.mutator.mutate_blueprint(name, agent.prompt_blueprint)

                # Run parallel execution in an isolated event loop for the thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(self.colony.execute_parallel(missions))
                loop.close()
                
                # 4. Uncertainty Quantification (Gap 3)
                for name, result in results.items():
                    uncertainty = UncertaintyQuantifier.calculate_disagreement(
                        result.primary_reasoning, 
                        result.challenger_reasoning
                    )
                    print(f"  Agent [{name}] Uncertainty Score: {uncertainty:.2f} (0=Certain, 1=Uncertain)")
                    
                    # Register new hypothesis for next cycle reality check
                    # (Assuming the answer predicts temperature movement for demo)
                    self.reality_validator.register_prediction(
                        name, result.final_answer, "temperature", "stable" 
                    )
                    
            time.sleep(self._loop_interval)

    def manual_feed(self, missions: Dict[str, tuple[str, Dict[str, Any]]]):
        """Manual trigger for the full loop."""
        print("\n--- Executing Manual Discovery Feed ---")
        
        # Validation
        for _, (_, data) in missions.items():
            self.reality_validator.validate_against_reality(data)
            
        # Apply Mutation
        for name in missions.keys():
            if name in self.colony.agents:
                agent = self.colony.agents[name]
                agent.prompt_blueprint = self.mutator.mutate_blueprint(name, agent.prompt_blueprint)

        # Execute Parallel
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we are already in an event loop (e.g. jupyter, uvicorn)
            task = asyncio.create_task(self.colony.execute_parallel(missions))
            # Just return the task or await it if allowed. For sync wrapper, we'd need nested loop handling.
            # In standard scripts, we usually run_until_complete.
            return task
        else:
            return loop.run_until_complete(self.colony.execute_parallel(missions))

if __name__ == "__main__":
    print("Edge Intelligence Module Ready.")
    # Quick Demo
    from harness import ToolRegistry
    
    # Initialize the integrated module
    edge_module = EdgeIntelligenceModule(memory_path="memory")
    
    # Create dummy agents
    mem = edge_module.vector_memory
    tools = ToolRegistry()
    
    agent1 = Agent(name="finance_agent", prompt_blueprint="You are a financial analyst.", memory=mem, tools=tools)
    agent2 = Agent(name="climate_agent", prompt_blueprint="You are a climate expert.", memory=mem, tools=tools)
    
    edge_module.colony.add_agent(agent1)
    edge_module.colony.add_agent(agent2)
    
    # Execute a manual run
    missions = {
        "finance_agent": ("What is the market impact?", {"temperature": 30.5, "system_load": 45}),
        "climate_agent": ("How does this affect climate models?", {"temperature": 30.5, "system_load": 45})
    }
    
    print("\n--- Running Manual Feed Demo ---")
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(edge_module.colony.execute_parallel(missions))
    for name, res in results.items():
        print(f"[{name}] Output: {res.final_answer[:100]}...")

