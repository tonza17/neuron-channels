"""Adaptive HV-plateau termination for the t0099 per-seed NSGA-II runs.

The watchdog observes the per-generation hypervolume trajectory written by
the t0099 NSGA-II driver after each generation and triggers termination when:

* At least ``HV_PLATEAU_MIN_HV_HISTORY = 4`` entries have been recorded.
* The mean of the last ``HV_PLATEAU_WINDOW = 2`` relative-delta values is
  below ``HV_PLATEAU_REL_THRESHOLD = 0.01``.

Because each seed writes its own trajectory file (`hv_trajectory_seed{s}.json`),
``HVPlateauTermination`` accepts a seed at construction time and reads the
appropriate per-seed file.
"""

from __future__ import annotations

import json
import sys

from pymoo.core.termination import Termination

from tasks.t0128_t0127_rerun_dsi_atp_3seeds.code.paths import hv_trajectory_json

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


def _load_hv_history(*, seed: int) -> list[float]:
    """Read the per-seed HV trajectory file. Empty list if not yet written."""
    path = hv_trajectory_json(seed=seed)
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    traj = raw.get("trajectory", []) if isinstance(raw, dict) else raw
    return [float(t["hypervolume"]) for t in traj]


class HVPlateauTermination(Termination):
    """Pymoo Termination subclass driving the HV-plateau stop rule for one seed."""

    def __init__(self, *, seed: int) -> None:
        super().__init__()
        self._seed = seed

    def _update(self, algorithm: object) -> float:  # type: ignore[override]
        hv_history = _load_hv_history(seed=self._seed)
        return 1.0 if should_stop(hv_history) else 0.0


def _run_unit_tests() -> int:
    short = [1.0, 1.5, 1.7]
    assert should_stop(short) is False, "below min should not trigger"
    flat = [1.0, 1.0, 1.0, 1.0]
    assert should_stop(flat) is True, "flat 4-entry trajectory should trigger"
    growth = [1.0 * (1.05**i) for i in range(4)]
    assert should_stop(growth) is False, "5% growth should not trigger plateau"
    slow_growth = [1.0 * (1.001**i) for i in range(4)]
    assert should_stop(slow_growth) is True, "0.1% growth should trigger plateau"
    print("all unit tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(_run_unit_tests())
