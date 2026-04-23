"""Preflight: identify distal sections on the t0024 DSGC and log the diameter distribution.

Builds the DSGC cell once, identifies terminal-dendrite sections via
``identify_distal_sections_t0024`` (``cell.terminal_dends``), computes the topological depth from
soma to each leaf, snapshots baseline ``seg.diam``, and writes the result to
``logs/preflight/distal_sections.json``.

Validation gate (REQ-2) is WARN-ONLY on t0024, because ``RGCmodelGD.hoc`` differs from t0022's
``RGCmodel.hoc`` topology and the thresholds (50 count, depth 3) inherited from t0030 may need
recalibration. A human reviewer inspects the JSON before running the full sweep.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell
from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.constants import (
    DISTAL_IDENTIFICATION_RULE,
    DISTAL_MIN_COUNT,
    DISTAL_MIN_DEPTH,
)
from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.diameter_override_t0024 import (
    snapshot_distal_diameters,
)
from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.distal_selector_t0024 import (
    identify_distal_sections_t0024,
)
from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.paths import (
    DISTAL_SECTIONS_JSON,
    LOGS_PREFLIGHT_DIR,
)


def _soma_section_name(*, soma: Any) -> str:
    """Return the soma section name. On t0024 ``DSGCCell.soma`` is a single Section."""
    return str(soma.name())


def _compute_depth(*, h: Any, sec: Any, soma_name: str) -> int:
    """Return the topological depth from ``sec`` to the soma along the HOC section tree.

    Depth is the number of ``parent`` hops until a section whose name matches ``soma_name`` is
    reached. Returns -1 if the walk exhausts parents before reaching the soma.
    """
    current: Any = sec
    # Defensive upper bound for non-trivial trees.
    for step in range(1000):
        name: str = str(current.name())
        if name == soma_name:
            return step
        ref: Any = h.SectionRef(sec=current)
        if int(ref.has_parent()) == 0:
            return -1
        current = ref.parent
    return -1


def _median(*, values: list[int]) -> float:
    if len(values) == 0:
        return float("nan")
    sorted_vals: list[int] = sorted(values)
    n: int = len(sorted_vals)
    if n % 2 == 1:
        return float(sorted_vals[n // 2])
    return 0.5 * (sorted_vals[n // 2 - 1] + sorted_vals[n // 2])


def _median_float(*, values: list[float]) -> float:
    if len(values) == 0:
        return float("nan")
    sorted_vals: list[float] = sorted(values)
    n: int = len(sorted_vals)
    if n % 2 == 1:
        return float(sorted_vals[n // 2])
    return 0.5 * (sorted_vals[n // 2 - 1] + sorted_vals[n // 2])


def main() -> int:
    print("[preflight_distal] building t0024 DSGC cell...", flush=True)
    cell = build_dsgc_cell()
    h: Any = cell.h

    distals: list[Any] = identify_distal_sections_t0024(cell=cell)
    count: int = len(distals)
    print(f"[preflight_distal] distal section count = {count}", flush=True)

    soma_name: str = _soma_section_name(soma=cell.soma)
    depths: list[int] = []
    bad_walk: list[str] = []
    for sec in distals:
        depth: int = _compute_depth(h=h, sec=sec, soma_name=soma_name)
        if depth < 0:
            bad_walk.append(str(sec.name()))
            continue
        depths.append(depth)

    if len(bad_walk) > 0:
        preview: list[str] = bad_walk[:5]
        print(
            f"[preflight_distal] WARN: {len(bad_walk)} distal sections could not be walked to "
            f"soma: {preview!r}",
            flush=True,
        )

    min_depth: int = min(depths) if len(depths) > 0 else -1
    max_depth: int = max(depths) if len(depths) > 0 else -1
    median_depth_val: float = _median(values=depths)

    baseline_diam: dict[tuple[int, float], float] = snapshot_distal_diameters(
        h=h,
        distal_sections=distals,
    )
    diams_um: list[float] = sorted(baseline_diam.values())
    segment_count: int = len(diams_um)
    min_diam_um: float = diams_um[0] if segment_count > 0 else float("nan")
    max_diam_um: float = diams_um[-1] if segment_count > 0 else float("nan")
    mean_diam_um: float = sum(diams_um) / segment_count if segment_count > 0 else float("nan")
    median_diam_um: float = _median_float(values=diams_um)

    payload: dict[str, Any] = {
        "count": count,
        "segment_count": segment_count,
        "min_depth": min_depth,
        "median_depth": median_depth_val,
        "max_depth": max_depth,
        "min_diam_um": float(min_diam_um),
        "median_diam_um": float(median_diam_um),
        "max_diam_um": float(max_diam_um),
        "mean_diam_um": float(mean_diam_um),
        "identification_rule": DISTAL_IDENTIFICATION_RULE,
        "warn_count_threshold": DISTAL_MIN_COUNT,
        "warn_depth_threshold": DISTAL_MIN_DEPTH,
        "count_warning": bool(count < DISTAL_MIN_COUNT),
        "depth_warning": bool(min_depth < DISTAL_MIN_DEPTH),
        "unwalkable_count": len(bad_walk),
    }

    LOGS_PREFLIGHT_DIR.mkdir(parents=True, exist_ok=True)
    DISTAL_SECTIONS_JSON.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[preflight_distal] wrote {DISTAL_SECTIONS_JSON}", flush=True)
    print(f"[preflight_distal] payload = {payload!r}", flush=True)

    # Warn-only gates on t0024 (logged above in the JSON).
    if count < DISTAL_MIN_COUNT:
        print(
            f"[preflight_distal] WARN: distal count {count} < {DISTAL_MIN_COUNT} "
            "(t0024 threshold is advisory, not enforced)",
            flush=True,
        )
    if min_depth < DISTAL_MIN_DEPTH:
        print(
            f"[preflight_distal] WARN: distal min_depth {min_depth} < {DISTAL_MIN_DEPTH} "
            "(t0024 threshold is advisory, not enforced)",
            flush=True,
        )
    print("OK", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
