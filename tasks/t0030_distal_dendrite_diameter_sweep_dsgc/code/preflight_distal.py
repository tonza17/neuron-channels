"""Preflight: identify distal sections and log the distribution.

Builds the DSGC cell once, identifies HOC leaf-dendrite sections on the ON arbor, computes the
minimum topological depth from soma to each leaf, and writes the result to
``logs/preflight/distal_sections.json``.

Validation gate (REQ-2):

* ``len(distal_sections) >= DISTAL_MIN_COUNT`` (50)
* ``min_depth >= DISTAL_MIN_DEPTH`` (3)

If either check fails, an ``AssertionError`` is raised. The orchestrator is expected to translate
that into an intervention file.

Structurally cloned from
``tasks/t0029_distal_dendrite_length_sweep_dsgc/code/preflight_distal.py`` with the baseline
snapshot and logged fields switched from ``sec.L`` to ``seg.diam``, and with a total distal surface
area diagnostic (Sigma pi * L * d) appended.
"""

from __future__ import annotations

import json
import math
import sys
from typing import Any

from tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code.constants import (
    DISTAL_IDENTIFICATION_RULE,
    DISTAL_MIN_COUNT,
    DISTAL_MIN_DEPTH,
)
from tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code.paths import (
    DISTAL_SECTIONS_JSON,
    LOGS_PREFLIGHT_DIR,
)
from tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code.trial_runner_diameter import (
    build_cell_context,
)


def _soma_section_names(*, h: Any) -> set[str]:
    """Return the set of soma section names on this morphology."""
    names: set[str] = set()
    soma: Any = h.RGC.soma
    name_attr: Any = getattr(soma, "name", None)
    if callable(name_attr):
        names.add(str(soma.name()))
        return names
    for sec in soma:
        names.add(str(sec.name()))
    return names


def _compute_depth(*, h: Any, sec: Any, soma_names: set[str]) -> int:
    """Return the topological depth from ``sec`` to the nearest soma section.

    Depth is the number of ``parent`` hops along the HOC section tree until a section whose name
    is in ``soma_names`` is reached. Returns -1 if the walk hits a cycle or exhausts parents
    before reaching the soma.
    """
    current: Any = sec
    for step in range(1000):
        name: str = str(current.name())
        if name in soma_names:
            return step
        ref: Any = h.SectionRef(sec=current)
        if int(ref.has_parent()) == 0:
            return -1
        current = ref.parent
    return -1


def _median(values: list[float]) -> float:
    n: int = len(values)
    if n == 0:
        return float("nan")
    ordered: list[float] = sorted(values)
    if n % 2 == 1:
        return ordered[n // 2]
    return 0.5 * (ordered[n // 2 - 1] + ordered[n // 2])


def main() -> int:
    print("[preflight_distal] building DSGC cell...", flush=True)
    ctx = build_cell_context()
    h: Any = ctx.h

    distals: list[Any] = ctx.distal_sections
    count: int = len(distals)
    print(f"[preflight_distal] distal section count = {count}", flush=True)

    soma_names: set[str] = _soma_section_names(h=h)
    depths: list[int] = []
    bad_walk: list[str] = []
    for sec in distals:
        depth: int = _compute_depth(h=h, sec=sec, soma_names=soma_names)
        if depth < 0:
            bad_walk.append(str(sec.name()))
            continue
        depths.append(depth)

    if len(bad_walk) > 0:
        preview: list[str] = bad_walk[:5]
        raise AssertionError(
            f"{len(bad_walk)} distal sections could not be walked to soma: {preview!r}",
        )

    min_depth: int = min(depths) if len(depths) > 0 else -1
    max_depth: int = max(depths) if len(depths) > 0 else -1

    diam_um_values: list[float] = [float(seg.diam) for sec in distals for seg in sec]
    n_segs: int = len(diam_um_values)
    min_diam_um: float = min(diam_um_values) if n_segs > 0 else float("nan")
    max_diam_um: float = max(diam_um_values) if n_segs > 0 else float("nan")
    median_diam_um: float = _median(diam_um_values)

    # Total distal surface area Sigma(pi * L * d) across all distal (sec, seg).
    total_surface_area_um2: float = 0.0
    for sec in distals:
        sec_L: float = float(sec.L)
        nseg: int = int(sec.nseg) if int(sec.nseg) > 0 else 1
        seg_L: float = sec_L / float(nseg)
        for seg in sec:
            total_surface_area_um2 += math.pi * seg_L * float(seg.diam)

    # Diagnostic: sec.L / sec.lambda_f at baseline (flags d_lambda violations at 2.0x later).
    # lambda_f at 100 Hz — use the standard NEURON idiom if available.
    l_over_lambda: list[float] = []
    for sec in distals:
        try:
            lam: float = float(h.lambda_f(100, sec=sec))
            if lam > 0.0:
                l_over_lambda.append(float(sec.L) / lam)
        except Exception:  # noqa: BLE001 -- lambda_f is an optional NEURON helper.
            continue

    payload: dict[str, Any] = {
        "count": count,
        "n_distal_segments": n_segs,
        "min_depth": min_depth,
        "max_depth": max_depth,
        "min_diam_um": float(min_diam_um),
        "median_diam_um": float(median_diam_um),
        "max_diam_um": float(max_diam_um),
        "total_surface_area_um2": float(total_surface_area_um2),
        "l_over_lambda_at_baseline_max": (
            float(max(l_over_lambda)) if len(l_over_lambda) > 0 else None
        ),
        "identification_rule": DISTAL_IDENTIFICATION_RULE,
    }

    LOGS_PREFLIGHT_DIR.mkdir(parents=True, exist_ok=True)
    DISTAL_SECTIONS_JSON.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[preflight_distal] wrote {DISTAL_SECTIONS_JSON}", flush=True)
    print(f"[preflight_distal] payload = {payload!r}", flush=True)

    # Validation gates.
    assert count >= DISTAL_MIN_COUNT, (
        f"distal section count {count} < {DISTAL_MIN_COUNT} (REQ-2 gate failed); "
        "fallback to Strahler port required."
    )
    assert min_depth >= DISTAL_MIN_DEPTH, (
        f"distal min_depth {min_depth} < {DISTAL_MIN_DEPTH} (REQ-2 gate failed); "
        "fallback to Strahler port required."
    )
    print("OK", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
