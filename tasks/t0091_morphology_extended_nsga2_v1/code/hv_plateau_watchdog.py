"""Adaptive HV-plateau termination for the t0091 joint 68-d NSGA-II run (REQ-6).

The watchdog observes the per-generation hypervolume trajectory written by
the t0091 NSGA-II driver after each generation and triggers termination when:

* At least ``HV_PLATEAU_MIN_HV_HISTORY = 4`` entries have been recorded
  (4-generation warm-up minimum before any plateau-driven stop).
* The mean of the last ``HV_PLATEAU_WINDOW = 2`` relative-delta values
  ``(hv_history[g] - hv_history[g - HV_PLATEAU_WINDOW]) / hv_history[g - HV_PLATEAU_WINDOW]``
  is below ``HV_PLATEAU_REL_THRESHOLD = 0.01`` (1% relative growth across a
  2-generation window after a 4-generation warm-up).

When combined with ``MaximumGenerationTermination(8)`` via
``TerminationCollection``, the overall stop condition is
(HV-plateau OR cost watchdog OR hard cap of 8 generations).
"""

from __future__ import annotations

import json
import sys

from pymoo.core.termination import Termination

from tasks.t0091_morphology_extended_nsga2_v1.code import paths

HV_PLATEAU_WINDOW: int = 2
HV_PLATEAU_REL_THRESHOLD: float = 0.01
HV_PLATEAU_MIN_HV_HISTORY: int = 4


def should_stop(hv_history: list[float]) -> bool:
    """Pure function for unit testing.

    Returns True when the HV trajectory has at least
    ``HV_PLATEAU_MIN_HV_HISTORY`` entries AND the mean of the last
    ``HV_PLATEAU_WINDOW`` relative-delta values (gen-N vs gen-(N - window))
    is below ``HV_PLATEAU_REL_THRESHOLD``.
    """
    n = len(hv_history)
    if n < HV_PLATEAU_MIN_HV_HISTORY:
        return False
    deltas: list[float] = []
    for offset in range(HV_PLATEAU_WINDOW):
        g = n - 1 - offset
        if g - HV_PLATEAU_WINDOW < 0:
            return False
        prev = hv_history[g - HV_PLATEAU_WINDOW]
        if prev <= 0.0:
            return False
        deltas.append((hv_history[g] - prev) / prev)
    mean_delta: float = sum(deltas) / len(deltas)
    return mean_delta < HV_PLATEAU_REL_THRESHOLD


def _load_hv_history() -> list[float]:
    """Read the HV trajectory file written by the t0091 driver.

    Returns an empty list if the file does not exist yet (first generation).
    """
    if not paths.HV_TRAJECTORY_JSON.exists():
        return []
    raw = json.loads(paths.HV_TRAJECTORY_JSON.read_text(encoding="utf-8"))
    traj = raw.get("trajectory", []) if isinstance(raw, dict) else raw
    return [float(t["hypervolume"]) for t in traj]


class HVPlateauTermination(Termination):
    """Pymoo Termination subclass driving the HV-plateau stop rule."""

    def _update(self, algorithm: object) -> float:  # type: ignore[override]
        hv_history = _load_hv_history()
        return 1.0 if should_stop(hv_history) else 0.0


def _run_unit_tests() -> int:
    # Case 1: 3 entries — below the 4-entry minimum, must NOT trigger.
    short = [1.0, 1.5, 1.7]
    assert should_stop(short) is False, "below min should not trigger"
    # Case 2: 4 entries flat — must trigger (mean delta = 0%).
    flat = [1.0, 1.0, 1.0, 1.0]
    assert should_stop(flat) is True, "flat 4-entry trajectory should trigger"
    # Case 3: 5% per-gen growth — well above 1%, should NOT trigger.
    growth = [1.0 * (1.05**i) for i in range(4)]
    assert should_stop(growth) is False, "5% growth should not trigger plateau"
    # Case 4: 0.1% per-gen growth — below 1%, should trigger.
    slow_growth = [1.0 * (1.001**i) for i in range(4)]
    assert should_stop(slow_growth) is True, "0.1% growth should trigger plateau"
    print("all unit tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(_run_unit_tests())
