"""
sensor_loop.py
===============
Gap 1 fix: Continuous sensor loop with Live/Manual toggle.

LIVE mode:   automatically polls a data source every N seconds and
             triggers agent.run() without user interaction.
MANUAL mode: user pastes data and clicks Run (current behavior) —
             nothing changes for existing workflows.

Designed to run in a background thread inside Streamlit, controlled
by a simple on/off toggle in the UI.
"""

from __future__ import annotations
import time
import threading
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Callable, Optional, Any


@dataclass
class SensorLoopState:
    """Shared state between the UI thread and the background polling thread."""
    mode: str = "manual"          # "manual" | "live"
    interval_seconds: float = 60.0
    running: bool = False
    last_poll_time: Optional[float] = None
    last_result_summary: str = ""
    poll_count: int = 0
    error_count: int = 0
    last_error: str = ""


class SensorLoop:
    """
    Manages a background thread that periodically:
      1. Pulls data from a source function (e.g. read CSV, call API, read telemetry file)
      2. Feeds it to an agent.run() call
      3. Logs the result

    Usage:
        def my_data_source():
            # return a dict like {"temperature": [...], "pressure": [...]}
            return read_latest_telemetry()

        loop = SensorLoop(
            agent=my_agent,
            data_source_fn=my_data_source,
            query="Monitor for anomalies in real-time telemetry",
            interval_seconds=30,
        )
        loop.start_live()      # begins background polling
        ...
        loop.stop_live()       # returns to manual mode
        loop.state             # inspect current status
    """

    def __init__(
        self,
        agent: Any,                       # harness.Agent instance
        data_source_fn: Callable[[], dict],
        query: str,
        interval_seconds: float = 60.0,
        on_result: Optional[Callable[[Any], None]] = None,
        log_path: Optional[str] = None,
    ):
        self.agent = agent
        self.data_source_fn = data_source_fn
        self.query = query
        self.on_result = on_result
        self.log_path = Path(log_path) if log_path else None

        self.state = SensorLoopState(interval_seconds=interval_seconds)
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()

    def _log(self, entry: dict):
        if not self.log_path:
            return
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        existing = []
        if self.log_path.exists():
            try:
                existing = json.loads(self.log_path.read_text())
            except Exception:
                existing = []
        existing.append(entry)
        existing = existing[-200:]  # cap log size
        self.log_path.write_text(json.dumps(existing, indent=2))

    def _poll_once(self):
        try:
            data = self.data_source_fn()
            result = self.agent.run(self.query, data)

            with self._lock:
                self.state.last_poll_time = time.time()
                self.state.poll_count += 1
                self.state.last_result_summary = result.final_answer[:200]

            self._log({
                "timestamp": time.time(),
                "poll_count": self.state.poll_count,
                "run_id": result.run_id,
                "final_answer": result.final_answer[:500],
            })

            if self.on_result:
                self.on_result(result)

        except Exception as e:
            with self._lock:
                self.state.error_count += 1
                self.state.last_error = str(e)
            self._log({"timestamp": time.time(), "error": str(e)})

    def _run_loop(self):
        while not self._stop_event.is_set():
            self._poll_once()
            self._stop_event.wait(self.state.interval_seconds)

    def start_live(self):
        """Switch to LIVE mode — begins background polling immediately."""
        if self.state.running:
            return  # already running

        with self._lock:
            self.state.mode = "live"
            self.state.running = True

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop_live(self):
        """Switch back to MANUAL mode — stops background polling."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)

        with self._lock:
            self.state.mode = "manual"
            self.state.running = False

    def manual_trigger(self, data: Optional[dict] = None, query: Optional[str] = None):
        """
        Run one cycle manually (used when mode == "manual").
        Optionally override the data source and query for this single call.
        """
        original_source = self.data_source_fn
        original_query = self.query

        if data is not None:
            self.data_source_fn = lambda: data
        if query is not None:
            self.query = query

        try:
            self._poll_once()
        finally:
            self.data_source_fn = original_source
            self.query = original_query

    def status(self) -> dict:
        with self._lock:
            s = self.state
            return {
                "mode": s.mode,
                "running": s.running,
                "interval_seconds": s.interval_seconds,
                "last_poll_time": s.last_poll_time,
                "last_result_summary": s.last_result_summary,
                "poll_count": s.poll_count,
                "error_count": s.error_count,
                "last_error": s.last_error,
            }


# ── Self-test ─────────────────────────────────────────────────────
if __name__ == "__main__":
    class FakeResult:
        def __init__(self, n):
            self.run_id = f"run{n}"
            self.final_answer = f"Test answer #{n}"

    class FakeAgent:
        def __init__(self):
            self.n = 0
        def run(self, query, data):
            self.n += 1
            return FakeResult(self.n)

    def fake_source():
        return {"temp": [20, 21, 22]}

    agent = FakeAgent()
    loop = SensorLoop(agent, fake_source, "test query", interval_seconds=0.3)

    print("Starting live mode...")
    loop.start_live()
    time.sleep(1.0)
    loop.stop_live()
    print("Status after live run:", loop.status())

    print("\nManual trigger...")
    loop.manual_trigger(data={"temp": [99]})
    print("Status after manual trigger:", loop.status())
