"""Preflight: identify distal sections and confirm the halved null-GABA unpinned null firing.

Structural clone of
``tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/preflight_distal.py`` with two additions:

1. Line 1 imports ``gaba_override`` so the 6.0 nS patch fires before the t0022 driver is imported.
2. After the distal-section identification gate, runs a 3-angle x 2-trial x 3-diameter sanity
   subset (18 trials) to confirm (a) the ``schedule_ei_onsets`` assertion at
   ``run_tuning_curve.py:327`` accepts ``gaba_null_pref_ratio = 2.0`` without raising, (b) the
   cell still fires normally at 1.0x baseline (``peak_hz >= 10``), and (c) reports the mean
   null-Hz at 1.0x baseline so the orchestrator can confirm the pre-condition.

Validation gates (REQ-1, REQ-2, REQ-3):

* ``len(distal_sections) >= DISTAL_MIN_COUNT`` (50)
* ``min_depth >= DISTAL_MIN_DEPTH`` (3)
* 18 sanity trials complete without ``AssertionError`` from ``schedule_ei_onsets``.
* ``peak_hz >= 10`` on the 1.0x preferred subset.
* Null-Hz at 1.0x is reported (informational; the partial-result flag is decided later in
  ``classify_slope.py``).

If any gate fails, an ``AssertionError`` is raised. The orchestrator is expected to translate
that into an intervention file.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

import tasks.t0036_rerun_t0030_halved_null_gaba.code.gaba_override  # noqa: F401  # MUST run first
from tasks.t0036_rerun_t0030_halved_null_gaba.code.constants import (
    DISTAL_IDENTIFICATION_RULE,
    DISTAL_MIN_COUNT,
    DISTAL_MIN_DEPTH,
    GABA_CONDUCTANCE_NULL_NS_OVERRIDE,
    NULL_HZ_MIN_PRECONDITION_HZ,
)
from tasks.t0036_rerun_t0030_halved_null_gaba.code.paths import (
    DISTAL_SECTIONS_JSON,
    LOGS_PREFLIGHT_DIR,
)
from tasks.t0036_rerun_t0030_halved_null_gaba.code.trial_runner_diameter import (
    build_cell_context,
    run_one_trial_diameter,
)

# Sanity subset: 3 angles x 2 trials x 3 multipliers = 18 trials.
_SANITY_ANGLES_DEG: tuple[int, ...] = (0, 120, 240)
_SANITY_N_TRIALS: int = 2
_SANITY_MULTIPLIERS: tuple[float, ...] = (0.5, 1.0, 2.0)
_SANITY_PEAK_HZ_MIN: float = 10.0
_SANITY_CURVE_CSV: Path = LOGS_PREFLIGHT_DIR / "sanity_tuning_curve_1p0x.csv"


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


def _write_sanity_curve_csv(
    *,
    curve_rows: list[tuple[int, int, float]],
    out_path: Path,
) -> None:
    """Write the 1.0x sanity subset as a canonical tuning-curve CSV (3-angle subset)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    import csv

    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["angle_deg", "trial_seed", "firing_rate_hz"])
        for angle_deg, trial_seed, rate_hz in curve_rows:
            writer.writerow([int(angle_deg), int(trial_seed), f"{rate_hz:.6f}"])


def _mean_rates_by_angle(
    *,
    rows: list[tuple[int, int, float]],
) -> dict[int, float]:
    """Group per-trial firing rates by angle and return the per-angle mean."""
    grouped: dict[int, list[float]] = {}
    for angle_deg, _trial_seed, rate_hz in rows:
        grouped.setdefault(int(angle_deg), []).append(float(rate_hz))
    return {angle: sum(rates) / len(rates) for angle, rates in grouped.items() if len(rates) > 0}


def _peak_null_from_sparse_subset(
    *,
    rows: list[tuple[int, int, float]],
) -> tuple[float, float]:
    """Return (peak_hz, null_hz) from a sparse-angle subset.

    The canonical t0012 scorer requires 12 evenly spaced angles, which the 3-angle sanity
    subset does not provide. For the preflight readout we compute peak = max mean rate across
    observed angles and null = mean rate at the (peak_angle + 180) mod 360 angle if present,
    falling back to the minimum mean rate otherwise.
    """
    mean_by_angle: dict[int, float] = _mean_rates_by_angle(rows=rows)
    if len(mean_by_angle) == 0:
        return (float("nan"), float("nan"))
    peak_angle: int = max(mean_by_angle.keys(), key=lambda a: mean_by_angle[a])
    peak_hz: float = float(mean_by_angle[peak_angle])
    null_angle: int = (peak_angle + 180) % 360
    if null_angle in mean_by_angle:
        null_hz: float = float(mean_by_angle[null_angle])
    else:
        null_hz = float(min(mean_by_angle.values()))
    return (peak_hz, null_hz)


def _run_sanity_subset(
    *,
    ctx: Any,
) -> tuple[float, float, int]:
    """Run the 18-trial sanity subset and return ``(peak_hz_1p0x, null_hz_1p0x, trials_run)``.

    Also writes ``logs/preflight/sanity_tuning_curve_1p0x.csv`` for future debugging.
    """
    rows_per_multiplier: dict[float, list[tuple[int, int, float]]] = {}
    trials_run: int = 0
    for multiplier in _SANITY_MULTIPLIERS:
        rows: list[tuple[int, int, float]] = []
        for angle_idx, angle_deg in enumerate(_SANITY_ANGLES_DEG):
            for trial_idx in range(_SANITY_N_TRIALS):
                trial_seed: int = 1000 * angle_idx + trial_idx + 1
                outcome = run_one_trial_diameter(
                    ctx=ctx,
                    angle_deg=float(angle_deg),
                    trial_seed=trial_seed,
                    multiplier=float(multiplier),
                )
                rows.append(
                    (int(angle_deg), int(trial_seed), float(outcome.firing_rate_hz)),
                )
                trials_run += 1
                print(
                    f"  [sanity] D={multiplier:.2f}x  dir={int(angle_deg):3d}  "
                    f"trial={trial_idx}  spikes={outcome.spike_count:3d}  "
                    f"rate={outcome.firing_rate_hz:6.2f}Hz",
                    flush=True,
                )
        rows_per_multiplier[float(multiplier)] = rows

    # Read peak/null from the sparse 3-angle 1.0x subset (t0012 loader requires 12 angles).
    rows_1p0: list[tuple[int, int, float]] = rows_per_multiplier[1.0]
    LOGS_PREFLIGHT_DIR.mkdir(parents=True, exist_ok=True)
    _write_sanity_curve_csv(curve_rows=rows_1p0, out_path=_SANITY_CURVE_CSV)
    peak_hz, null_hz = _peak_null_from_sparse_subset(rows=rows_1p0)
    return (peak_hz, null_hz, trials_run)


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
    l_over_lambda: list[float] = []
    for sec in distals:
        try:
            lam: float = float(h.lambda_f(100, sec=sec))
            if lam > 0.0:
                l_over_lambda.append(float(sec.L) / lam)
        except Exception:  # noqa: BLE001 -- lambda_f is an optional NEURON helper.
            continue

    # Section-count gate first -- fail fast before the expensive sanity subset.
    assert count >= DISTAL_MIN_COUNT, (
        f"distal section count {count} < {DISTAL_MIN_COUNT} (REQ-3 gate failed); "
        "fallback to Strahler port required."
    )
    assert min_depth >= DISTAL_MIN_DEPTH, (
        f"distal min_depth {min_depth} < {DISTAL_MIN_DEPTH} (REQ-3 gate failed); "
        "fallback to Strahler port required."
    )

    # Null-Hz sanity subset: 18 trials (3 angles x 2 trials x 3 multipliers).
    print(
        "[preflight_distal] running 18-trial sanity subset "
        "(3 angles x 2 trials x 3 multipliers)...",
        flush=True,
    )
    peak_hz_1p0, null_hz_1p0, trials_run = _run_sanity_subset(ctx=ctx)
    print(
        f"[preflight_distal] sanity subset complete: trials_run = {trials_run}, "
        f"peak_hz_1p0x = {peak_hz_1p0:.3f}, null_hz_1p0x = {null_hz_1p0:.3f}",
        flush=True,
    )

    gaba_null_pref_ratio_asserted: float = 2.0
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
        "gaba_conductance_null_ns_effective": float(GABA_CONDUCTANCE_NULL_NS_OVERRIDE),
        "gaba_null_pref_ratio_asserted": gaba_null_pref_ratio_asserted,
        "preflight_peak_hz_1p0x": float(peak_hz_1p0),
        "preflight_null_hz_1p0x": float(null_hz_1p0),
        "preflight_sanity_trials_run": int(trials_run),
        "preflight_null_hz_precondition_threshold_hz": float(NULL_HZ_MIN_PRECONDITION_HZ),
        "preflight_null_hz_precondition_pass_informational": bool(
            null_hz_1p0 >= NULL_HZ_MIN_PRECONDITION_HZ,
        ),
    }

    LOGS_PREFLIGHT_DIR.mkdir(parents=True, exist_ok=True)
    DISTAL_SECTIONS_JSON.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[preflight_distal] wrote {DISTAL_SECTIONS_JSON}", flush=True)
    print(f"[preflight_distal] payload = {payload!r}", flush=True)

    # Sanity gates.
    assert trials_run == len(_SANITY_MULTIPLIERS) * len(_SANITY_ANGLES_DEG) * _SANITY_N_TRIALS, (
        f"sanity subset ran {trials_run} trials, expected "
        f"{len(_SANITY_MULTIPLIERS) * len(_SANITY_ANGLES_DEG) * _SANITY_N_TRIALS} "
        "(schedule_ei_onsets assertion likely failed mid-loop)"
    )
    assert peak_hz_1p0 >= _SANITY_PEAK_HZ_MIN, (
        f"sanity peak_hz at 1.0x baseline = {peak_hz_1p0:.3f} Hz < "
        f"{_SANITY_PEAK_HZ_MIN} Hz (REQ-1 gate failed); the GABA override may have broken "
        "preferred-direction firing. Halt and debug trial_runner_diameter.py."
    )
    if null_hz_1p0 < NULL_HZ_MIN_PRECONDITION_HZ:
        print(
            "[preflight_distal] WARNING: null_hz at 1.0x baseline = "
            f"{null_hz_1p0:.3f} Hz < {NULL_HZ_MIN_PRECONDITION_HZ} Hz "
            "pre-condition threshold. Full sweep may still recover with 10 trials/angle, "
            "but a further reduction of GABA_CONDUCTANCE_NULL_NS (e.g. 4 nS) may be needed.",
            flush=True,
        )
    print("OK", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
