"""Loaders for NSGA-II evaluation dumps and HV trajectories.

Reuses the canonical patterns from t0115 ``build_results.py`` (the suffix-
branching JSON / gzipped-JSON reader and the ``_is_legit_joint_pass``
predicate) but in a focused module with explicit type aliases.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path
from typing import Any

from tasks.t0121_5seed_substrate_rate_canonical_report.code.constants import (
    DSI_THRESHOLD,
    LEGIT_DSI_CEILING,
    PD_RATE_THRESHOLD_HZ,
)

# Module-level assertions: the thresholds copied into constants.py match
# the t0115 upstream values bit-for-bit. If a future edit drifts these,
# the import fails loudly rather than silently producing wrong numbers.
assert DSI_THRESHOLD == 0.5, "DSI threshold is 0.5"
assert PD_RATE_THRESHOLD_HZ == 30.0, "PD-rate threshold is 30 Hz"
assert LEGIT_DSI_CEILING == 0.9999, "LEGIT DSI ceiling is 0.9999"

type EvalRecord = dict[str, Any]
type HvRecord = dict[str, Any]
type ParetoCell = dict[str, Any]


def load_evaluations(*, path: Path) -> list[EvalRecord]:
    """Load an NSGA-II all-evaluations dump (plain or gzipped JSON).

    The top-level payload is either ``{"evaluations": [...]}`` (most source
    tasks) or a bare list (legacy). Both shapes return the inner list.
    """
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as f:
            data: object = json.load(f)
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        evals: object = data["evaluations"]
        assert isinstance(evals, list), "evaluations payload is a list"
        return evals
    assert isinstance(data, list), "top-level evaluations payload is a list"
    return data


def load_hv(*, path: Path) -> list[HvRecord]:
    """Load an NSGA-II HV trajectory JSON.

    The payload is either ``{"trajectory": [...]}`` (canonical) or a bare
    list (legacy). Returns the inner list of HV records.
    """
    data: object = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        traj: object = data.get("trajectory", data)
    else:
        traj = data
    assert isinstance(traj, list), "HV trajectory payload is a list"
    return traj


def load_pareto_cells(*, path: Path) -> list[ParetoCell]:
    """Load a strict-Pareto ``pareto_front_seed<N>.json`` payload."""
    data: object = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "pareto payload is an object"
    cells: object = data["cells"]
    assert isinstance(cells, list), "pareto cells is a list"
    return cells


def is_legit_joint_pass(*, dsi: float, pd_rate_hz: float) -> bool:
    """Canonical LEGIT joint-pass predicate.

    ``DSI >= 0.5 AND PD-rate >= 30 Hz AND DSI < 0.9999``. The upper bound
    excludes silence-guard / single-spike evaluator artefacts at DSI = 1.0.
    Copied verbatim from t0115 ``_is_legit_joint_pass``.
    """
    return dsi >= DSI_THRESHOLD and pd_rate_hz >= PD_RATE_THRESHOLD_HZ and dsi < LEGIT_DSI_CEILING


def cell_vector_key(*, vector_68d: list[float]) -> tuple[float, ...]:
    """Hashable dedup key for an evaluation record.

    Source tasks do not carry an explicit ``cell_id`` field on raw evaluation
    records, so the canonical t0115 dedup convention uses the 68-d parameter
    vector as the cell identity. This helper makes that explicit.
    """
    return tuple(vector_68d)
