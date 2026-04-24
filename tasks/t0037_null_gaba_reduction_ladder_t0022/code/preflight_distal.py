"""Preflight: identify distal sections and confirm the GABA ladder rebind mechanism works.

Structural clone of ``tasks/t0036_rerun_t0030_halved_null_gaba/code/preflight_distal.py`` with
three substantive edits:

1. No import-time GABA patch. ``gaba_override`` is imported for the ``set_null_gaba_ns`` symbol
   (the function), not as a patching side-effect.
2. The 18-trial sanity subset iterates **3 GABA levels x 3 angles x 2 trials** (distal diameter
   locked at 1.0x) instead of t0036's 3 diameters x 3 angles x 2 trials.
3. Pre-condition gate is peak-Hz at the highest GABA level (4 nS), not null-Hz at baseline.

Validation gates (REQ-1, REQ-3, REQ-9):

* ``len(distal_sections) >= DISTAL_MIN_COUNT`` (50).
* ``min_depth >= DISTAL_MIN_DEPTH`` (3).
* 18 sanity trials complete without ``AssertionError`` from ``schedule_ei_onsets`` (validates
  that the per-trial rebind of ``GABA_CONDUCTANCE_NULL_NS`` works across 3 distinct GABA values).
* ``peak_hz >= PEAK_HZ_MIN_PRECONDITION_HZ`` (10) on the preferred-direction (0 deg) subset at
  4 nS (the highest GABA in the ladder).
* Null-Hz at each of the 3 GABA levels is reported (informational -- the pinning question IS
  the research question, not a pre-condition).

If any gate fails, an ``AssertionError`` is raised. The orchestrator is expected to translate
that into an intervention file.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

from tasks.t0037_null_gaba_reduction_ladder_t0022.code.constants import (
    DISTAL_IDENTIFICATION_RULE,
    DISTAL_MIN_COUNT,
    DISTAL_MIN_DEPTH,
    PEAK_HZ_MIN_PRECONDITION_HZ,
    PREFLIGHT_ANGLES_DEG,
    PREFLIGHT_GABA_LEVELS_NS,
    PREFLIGHT_N_TRIALS,
)
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.gaba_override import set_null_gaba_ns
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.paths import (
    DISTAL_SECTIONS_JSON,
    LOGS_PREFLIGHT_DIR,
)
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.trial_runner_gaba_ladder import (
    CellContext,
    build_cell_context,
    run_single_trial_gaba,
)

# Preferred-direction angle used for the peak-Hz gate at the highest GABA level.
_PREFERRED_ANGLE_DEG: int = 0

# Per-GABA sanity CSV naming template (debug aid).
_SANITY_CURVE_CSV_TEMPLATE: str = "sanity_tuning_curve_G{label}.csv"


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


def _gaba_label(*, value_ns: float) -> str:
    return f"{value_ns:.2f}".replace(".", "p")


def _write_sanity_curve_csv(
    *,
    curve_rows: list[tuple[int, int, float]],
    out_path: Path,
) -> None:
    """Write one GABA level's sanity subset as a canonical (sparse-angle) tuning-curve CSV."""
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
    """Return ``(peak_hz, null_hz)`` from a sparse-angle subset.

    Peak = max mean rate across observed angles; null = mean rate at the (peak_angle + 180)
    mod 360 angle if present, otherwise the minimum mean rate.
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


def _mean_rate_at_angle(
    *,
    rows: list[tuple[int, int, float]],
    angle_deg: int,
) -> float:
    """Return the mean firing rate at a specific angle, or NaN if angle absent."""
    mean_by_angle: dict[int, float] = _mean_rates_by_angle(rows=rows)
    if angle_deg not in mean_by_angle:
        return float("nan")
    return float(mean_by_angle[angle_deg])


def _run_sanity_subset(
    *,
    ctx: CellContext,
) -> tuple[dict[float, float], dict[float, float], dict[float, float], int]:
    """Run the 18-trial sanity subset.

    Returns ``(peak_hz_by_gaba, null_hz_by_gaba, peak_at_pref_by_gaba, trials_run)`` where each
    mapping is keyed by the GABA level in nS.
    """
    rows_per_gaba: dict[float, list[tuple[int, int, float]]] = {}
    trials_run: int = 0
    for gaba_ns in PREFLIGHT_GABA_LEVELS_NS:
        set_null_gaba_ns(value_ns=float(gaba_ns))
        rows: list[tuple[int, int, float]] = []
        for angle_idx, angle_deg in enumerate(PREFLIGHT_ANGLES_DEG):
            for trial_idx in range(PREFLIGHT_N_TRIALS):
                trial_seed: int = 1000 * angle_idx + trial_idx + 1
                outcome = run_single_trial_gaba(
                    ctx=ctx,
                    angle_deg=float(angle_deg),
                    trial_seed=trial_seed,
                    gaba_null_ns=float(gaba_ns),
                )
                rows.append(
                    (int(angle_deg), int(trial_seed), float(outcome.firing_rate_hz)),
                )
                trials_run += 1
                print(
                    f"  [sanity] G={gaba_ns:.2f}nS  dir={int(angle_deg):3d}  "
                    f"trial={trial_idx}  spikes={outcome.spike_count:3d}  "
                    f"rate={outcome.firing_rate_hz:6.2f}Hz",
                    flush=True,
                )
        rows_per_gaba[float(gaba_ns)] = rows
        LOGS_PREFLIGHT_DIR.mkdir(parents=True, exist_ok=True)
        sanity_csv: Path = LOGS_PREFLIGHT_DIR / _SANITY_CURVE_CSV_TEMPLATE.format(
            label=_gaba_label(value_ns=float(gaba_ns)),
        )
        _write_sanity_curve_csv(curve_rows=rows, out_path=sanity_csv)

    peak_hz_by_gaba: dict[float, float] = {}
    null_hz_by_gaba: dict[float, float] = {}
    peak_at_pref_by_gaba: dict[float, float] = {}
    for gaba_ns, rows in rows_per_gaba.items():
        peak_hz, null_hz = _peak_null_from_sparse_subset(rows=rows)
        peak_hz_by_gaba[float(gaba_ns)] = peak_hz
        null_hz_by_gaba[float(gaba_ns)] = null_hz
        peak_at_pref_by_gaba[float(gaba_ns)] = _mean_rate_at_angle(
            rows=rows,
            angle_deg=_PREFERRED_ANGLE_DEG,
        )
    return (peak_hz_by_gaba, null_hz_by_gaba, peak_at_pref_by_gaba, trials_run)


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

    total_surface_area_um2: float = 0.0
    for sec in distals:
        sec_L: float = float(sec.L)
        nseg: int = int(sec.nseg) if int(sec.nseg) > 0 else 1
        seg_L: float = sec_L / float(nseg)
        for seg in sec:
            total_surface_area_um2 += math.pi * seg_L * float(seg.diam)

    # Section-count gate first -- fail fast before the expensive sanity subset.
    assert count >= DISTAL_MIN_COUNT, (
        f"distal section count {count} < {DISTAL_MIN_COUNT} (REQ-1 gate failed); "
        "fallback to Strahler port required."
    )
    assert min_depth >= DISTAL_MIN_DEPTH, (
        f"distal min_depth {min_depth} < {DISTAL_MIN_DEPTH} (REQ-1 gate failed); "
        "fallback to Strahler port required."
    )

    # 18-trial sanity subset: 3 GABA levels x 3 angles x 2 trials.
    print(
        "[preflight_distal] running 18-trial sanity subset "
        "(3 GABA levels x 3 angles x 2 trials)...",
        flush=True,
    )
    (
        peak_hz_by_gaba,
        null_hz_by_gaba,
        peak_at_pref_by_gaba,
        trials_run,
    ) = _run_sanity_subset(ctx=ctx)

    # Pre-condition gate: preferred-direction peak firing at the HIGHEST GABA level (4 nS) must
    # clear 10 Hz. Use the explicit preferred-direction mean (angle=0) rather than the sparse
    # peak -- the sparse subset may coincidentally peak at a non-preferred angle if one trial
    # at 90 or 180 happens to fire.
    highest_gaba_ns: float = max(peak_hz_by_gaba.keys())
    peak_hz_preferred_at_highest: float = peak_at_pref_by_gaba[highest_gaba_ns]

    print(
        "[preflight_distal] sanity subset complete: "
        f"trials_run = {trials_run}, "
        f"peak_hz_preferred_at_{highest_gaba_ns:.1f}nS = "
        f"{peak_hz_preferred_at_highest:.3f}",
        flush=True,
    )
    for gaba_ns in sorted(null_hz_by_gaba.keys()):
        print(
            f"  G={gaba_ns:.2f}nS: peak_hz={peak_hz_by_gaba[gaba_ns]:.3f} "
            f"null_hz={null_hz_by_gaba[gaba_ns]:.3f} "
            f"peak_at_0deg={peak_at_pref_by_gaba[gaba_ns]:.3f}",
            flush=True,
        )

    payload: dict[str, Any] = {
        "count": count,
        "n_distal_segments": n_segs,
        "min_depth": min_depth,
        "max_depth": max_depth,
        "min_diam_um": float(min_diam_um),
        "median_diam_um": float(median_diam_um),
        "max_diam_um": float(max_diam_um),
        "total_surface_area_um2": float(total_surface_area_um2),
        "identification_rule": DISTAL_IDENTIFICATION_RULE,
        "preflight_gaba_levels_ns": [float(v) for v in PREFLIGHT_GABA_LEVELS_NS],
        "preflight_angles_deg": [int(a) for a in PREFLIGHT_ANGLES_DEG],
        "preflight_n_trials_per_angle": int(PREFLIGHT_N_TRIALS),
        "preflight_trials_run": int(trials_run),
        "preflight_peak_hz_by_gaba": {
            f"{k:.2f}": float(v) for k, v in sorted(peak_hz_by_gaba.items())
        },
        "preflight_null_hz_by_gaba": {
            f"{k:.2f}": float(v) for k, v in sorted(null_hz_by_gaba.items())
        },
        "preflight_peak_hz_at_pref_by_gaba": {
            f"{k:.2f}": float(v) for k, v in sorted(peak_at_pref_by_gaba.items())
        },
        "preflight_peak_hz_4ns_preferred": float(peak_hz_preferred_at_highest),
        "peak_hz_min_precondition_hz": float(PEAK_HZ_MIN_PRECONDITION_HZ),
        "preflight_pass": bool(
            peak_hz_preferred_at_highest >= PEAK_HZ_MIN_PRECONDITION_HZ,
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
    expected_trials: int = (
        len(PREFLIGHT_GABA_LEVELS_NS) * len(PREFLIGHT_ANGLES_DEG) * PREFLIGHT_N_TRIALS
    )
    assert trials_run == expected_trials, (
        f"sanity subset ran {trials_run} trials, expected {expected_trials} "
        "(schedule_ei_onsets assertion likely failed mid-loop)"
    )
    assert peak_hz_preferred_at_highest >= PEAK_HZ_MIN_PRECONDITION_HZ, (
        f"preflight peak_hz at preferred direction with GABA={highest_gaba_ns:.1f}nS = "
        f"{peak_hz_preferred_at_highest:.3f} Hz < {PEAK_HZ_MIN_PRECONDITION_HZ} Hz "
        "(REQ-9 gate failed); preferred-direction firing is broken by the override "
        "sequencing. Halt and debug trial_runner_gaba_ladder.py."
    )
    print("OK", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
