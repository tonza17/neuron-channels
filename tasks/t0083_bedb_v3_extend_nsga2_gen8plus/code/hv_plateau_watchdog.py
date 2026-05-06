"""Adaptive HV-plateau termination for the t0083 NSGA-II continuation (REQ-4).

The watchdog observes the per-generation hypervolume trajectory written by
t0080's ``_save_hv_trajectory`` after each generation and triggers termination
when:

* At least ``HV_PLATEAU_MIN_HV_HISTORY`` entries have been recorded
  (``len(hv_history) >= 13``: 8 generations from t0081 [gens 0..7] + 5 new
  generations [gens 8..12]). This guarantees a minimum of 5 additional
  generations are run before any plateau-driven stop.
* The mean of the last 3 relative-delta values
  ``(hv_history[g] - hv_history[g - HV_PLATEAU_WINDOW]) / hv_history[g - HV_PLATEAU_WINDOW]``
  for ``g in (N-3, N-2, N-1)`` is below ``HV_PLATEAU_REL_THRESHOLD = 0.01``
  (1% relative growth averaged over the trailing window).

When combined with ``MaximumGenerationTermination(10)`` via
``TerminationCollection``, the overall stop condition is (HV-plateau OR
hard cap of 10 additional generations).
"""

from __future__ import annotations

import json
import sys

from pymoo.core.termination import Termination

from tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code import paths

# 8 t0081 generations (0..7) + 5 additional new generations (8..12) = 13.
# Earliest stop = end of gen 12 with len(hv_history) == 13, evaluating
# delta windows at gens 10/11/12 against gens 7/8/9.
HV_PLATEAU_WINDOW: int = 3
HV_PLATEAU_REL_THRESHOLD: float = 0.01
HV_PLATEAU_MIN_GENS_AFTER_RESUME: int = 5
T0081_HV_HISTORY_LEN: int = 8
HV_PLATEAU_MIN_HV_HISTORY: int = T0081_HV_HISTORY_LEN + HV_PLATEAU_MIN_GENS_AFTER_RESUME  # 13


def should_stop(hv_history: list[float]) -> bool:
    """Pure function for unit testing.

    Returns True when the HV trajectory has at least
    ``HV_PLATEAU_MIN_HV_HISTORY`` entries AND the mean of the last 3
    relative-delta values (gen-N vs gen-(N - window)) is below
    ``HV_PLATEAU_REL_THRESHOLD``.
    """
    n = len(hv_history)
    if n < HV_PLATEAU_MIN_HV_HISTORY:
        return False
    deltas: list[float] = []
    for offset in range(HV_PLATEAU_WINDOW):
        g = n - 1 - offset
        prev = hv_history[g - HV_PLATEAU_WINDOW]
        if prev <= 0.0:
            return False
        deltas.append((hv_history[g] - prev) / prev)
    mean_delta: float = sum(deltas) / len(deltas)
    return mean_delta < HV_PLATEAU_REL_THRESHOLD


def _load_hv_history() -> list[float]:
    """Read the HV trajectory file written by ``_save_hv_trajectory``.

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
    # Case 1: only 8 entries (t0081's trajectory) — below 13-entry minimum,
    # must NOT trigger.
    t0081_traj = [6.59, 8.99, 9.24, 11.08, 11.57, 13.14, 15.22, 16.33]
    assert should_stop(t0081_traj) is False, (
        f"should_stop returned True on len={len(t0081_traj)} (below {HV_PLATEAU_MIN_HV_HISTORY})"
    )
    # Case 2: perfectly flat 13-entry trajectory — must trigger (delta 0%).
    flat = [16.33] * HV_PLATEAU_MIN_HV_HISTORY
    assert should_stop(flat) is True, "flat 13-entry trajectory should trigger"
    # Case 3: 0.1% per-gen geometric growth — over a 3-gen lookback window
    # this gives mean delta ~= 0.3% (well below 1% threshold), should trigger.
    grow_01 = [16.33 * (1.001**i) for i in range(HV_PLATEAU_MIN_HV_HISTORY)]
    assert should_stop(grow_01) is True, (
        "0.1% per-gen growth (~0.3% over 3-gen window) should trigger (< 1%)"
    )
    # Case 4: 1% per-gen geometric growth — over a 3-gen lookback window
    # this gives mean delta ~= 3.03% (well above 1% threshold), should NOT trigger.
    grow_1 = [16.33 * (1.01**i) for i in range(HV_PLATEAU_MIN_HV_HISTORY)]
    assert should_stop(grow_1) is False, (
        "1% per-gen growth (~3% over 3-gen window) should NOT trigger"
    )
    # Case 5: trajectory just one short of the minimum — must NOT trigger.
    flat_short = [16.33] * (HV_PLATEAU_MIN_HV_HISTORY - 1)
    assert should_stop(flat_short) is False, (
        f"len={len(flat_short)} below {HV_PLATEAU_MIN_HV_HISTORY} should NOT trigger"
    )
    # Case 6: t0081 trajectory padded with 5 flat entries (simulating gens
    # 8..12 with no improvement) — should trigger.
    padded = list(t0081_traj) + [16.33] * 5
    assert should_stop(padded) is True, "8 t0081 + 5 flat new generations should trigger plateau"
    print("all unit tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(_run_unit_tests())
