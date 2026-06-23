"""
self_improve.py
=================
Gap 6 fix: Self-improvement loop.

Tracks which theories/predictions were confirmed vs pruned, and uses
that history to append calibration notes to an agent's prompt
blueprint -- a lightweight, auditable form of learning from outcomes.

This does NOT silently rewrite prompts (that would be unsafe and
unauditable). It proposes specific, human-reviewable additions based
on concrete evidence, and requires explicit approval to apply.
"""

from __future__ import annotations
import json
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class CalibrationNote:
    id: str
    agent: str
    created_at: float
    evidence_summary: str
    proposed_addition: str
    based_on_n_predictions: int
    approved: bool = False
    applied: bool = False

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, d: dict) -> "CalibrationNote":
        return cls(**d)


class SelfImprovementEngine:
    """
    Reviews RealityAnchor prediction history per agent and proposes
    calibration notes -- short, specific additions to that agent's
    prompt blueprint reflecting what's been empirically confirmed
    or refuted.

    Usage:
        engine = SelfImprovementEngine(path="memory/calibration")
        notes = engine.propose_calibrations(reality_anchor, agent="finance")
        for note in notes:
            print(note.proposed_addition)
            engine.approve(note.id)   # human-in-the-loop approval

        updated_blueprint = engine.apply_approved(agent="finance", base_blueprint=original_prompt)
    """

    MIN_PREDICTIONS_FOR_CALIBRATION = 3

    def __init__(self, path: str = "memory/calibration"):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self._notes: dict[str, CalibrationNote] = {}
        self._load()

    def _file(self) -> Path:
        return self.path / "calibration_notes.json"

    def _load(self):
        f = self._file()
        if f.exists():
            raw = json.loads(f.read_text())
            self._notes = {k: CalibrationNote.from_dict(v) for k, v in raw.items()}

    def _save(self):
        self._file().write_text(
            json.dumps({k: v.to_dict() for k, v in self._notes.items()}, indent=2)
        )

    def propose_calibrations(self, reality_anchor, agent: str) -> list[CalibrationNote]:
        """
        Examine validated predictions for this agent and propose
        calibration notes if there's a clear accuracy pattern.
        """
        validated = [
            p for p in reality_anchor._predictions.values()
            if p.agent == agent and p.validated and p.accuracy_score is not None
        ]

        if len(validated) < self.MIN_PREDICTIONS_FOR_CALIBRATION:
            return []

        avg_accuracy = sum(p.accuracy_score for p in validated) / len(validated)
        new_notes = []

        if avg_accuracy < 0.5:
            note = CalibrationNote(
                id=f"cal_{agent}_{int(time.time())}",
                agent=agent,
                created_at=time.time(),
                evidence_summary=(
                    f"Last {len(validated)} validated predictions averaged "
                    f"{avg_accuracy:.0%} accuracy -- below the 50% threshold."
                ),
                proposed_addition=(
                    f"CALIBRATION NOTE: Recent predictions from this agent have shown "
                    f"low accuracy ({avg_accuracy:.0%} over {len(validated)} validated "
                    f"predictions). Express lower confidence and flag more hypotheses "
                    f"as requiring further validation before treating them as reliable."
                ),
                based_on_n_predictions=len(validated),
            )
            new_notes.append(note)

        elif avg_accuracy > 0.85:
            note = CalibrationNote(
                id=f"cal_{agent}_{int(time.time())}",
                agent=agent,
                created_at=time.time(),
                evidence_summary=(
                    f"Last {len(validated)} validated predictions averaged "
                    f"{avg_accuracy:.0%} accuracy -- strong track record."
                ),
                proposed_addition=(
                    f"CALIBRATION NOTE: This agent's predictions have been highly "
                    f"accurate ({avg_accuracy:.0%} over {len(validated)} validated "
                    f"predictions). Current reasoning approach is well-calibrated; "
                    f"maintain current confidence levels."
                ),
                based_on_n_predictions=len(validated),
            )
            new_notes.append(note)

        var_errors: dict[str, list[float]] = {}
        for p in validated:
            for var, predicted in p.predicted_variables.items():
                if var in p.actual_values and predicted != 0:
                    err = abs(predicted - p.actual_values[var]) / abs(predicted)
                    var_errors.setdefault(var, []).append(err)

        for var, errors in var_errors.items():
            if len(errors) >= self.MIN_PREDICTIONS_FOR_CALIBRATION:
                avg_err = sum(errors) / len(errors)
                if avg_err > 0.3:
                    note = CalibrationNote(
                        id=f"cal_{agent}_{var}_{int(time.time())}",
                        agent=agent,
                        created_at=time.time(),
                        evidence_summary=(
                            f"Predictions for '{var}' averaged {avg_err:.0%} error "
                            f"across {len(errors)} instances."
                        ),
                        proposed_addition=(
                            f"CALIBRATION NOTE: Predictions involving '{var}' have shown "
                            f"high error ({avg_err:.0%} average) in past validated runs. "
                            f"Treat hypotheses about this variable with extra caution."
                        ),
                        based_on_n_predictions=len(errors),
                    )
                    new_notes.append(note)

        for note in new_notes:
            self._notes[note.id] = note
        self._save()

        return new_notes

    def approve(self, note_id: str):
        if note_id in self._notes:
            self._notes[note_id].approved = True
            self._save()

    def reject(self, note_id: str):
        if note_id in self._notes:
            del self._notes[note_id]
            self._save()

    def pending_review(self, agent: Optional[str] = None) -> list[CalibrationNote]:
        notes = [n for n in self._notes.values() if not n.approved]
        if agent:
            notes = [n for n in notes if n.agent == agent]
        return sorted(notes, key=lambda n: -n.created_at)

    def apply_approved(self, agent: str, base_blueprint: str) -> str:
        to_apply = [
            n for n in self._notes.values()
            if n.agent == agent and n.approved and not n.applied
        ]
        if not to_apply:
            return base_blueprint

        additions = "\n\n".join(n.proposed_addition for n in to_apply)
        updated = f"{base_blueprint}\n\n--- LEARNED CALIBRATIONS ---\n{additions}"

        for n in to_apply:
            n.applied = True
        self._save()

        return updated

    def history_for(self, agent: str) -> list[CalibrationNote]:
        return sorted(
            [n for n in self._notes.values() if n.agent == agent],
            key=lambda n: -n.created_at,
        )


if __name__ == "__main__":
    import tempfile, sys
    sys.path.insert(0, ".")
    from reality_anchor import RealityAnchor

    with tempfile.TemporaryDirectory() as tmp:
        anchor = RealityAnchor(path=tmp + "/reality")
        engine = SelfImprovementEngine(path=tmp + "/calibration")

        for i in range(4):
            pid = anchor.record_prediction(
                agent="finance",
                prediction_text=f"Test prediction {i}",
                predicted_variables={"gold": 2000.0},
                horizon_seconds=0,
            )
            time.sleep(0.05)
            anchor.validate(pid, actual={"gold": 600.0})  # 70% error -> ~30% accuracy

        notes = engine.propose_calibrations(anchor, agent="finance")
        print(f"Proposed {len(notes)} calibration note(s):")
        for n in notes:
            print(f"\n  ID: {n.id}")
            print(f"  Evidence: {n.evidence_summary}")
            print(f"  Proposed: {n.proposed_addition}")

        if notes:
            engine.approve(notes[0].id)
            updated = engine.apply_approved("finance", "You are the Finance Agent.")
            print(f"\n=== Updated blueprint ===\n{updated}")
