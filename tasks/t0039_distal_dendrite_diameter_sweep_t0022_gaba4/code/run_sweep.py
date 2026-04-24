"""t0030 distal-dendrite diameter sweep driver.

Iterates ``DIAMETER_MULTIPLIERS`` x 12 angles x ``N_TRIALS`` (10 by default) and writes a tidy CSV
with one row per trial plus a per-diameter canonical 12-angle curve CSV (accepted by the t0012
``tuning_curve_loss`` scorer). Structurally cloned from
``tasks/t0029_distal_dendrite_length_sweep_dsgc/code/run_length_sweep.py`` with the sweep grid
renamed to ``DIAMETER_MULTIPLIERS``, the first CSV column renamed to ``diameter_multiplier``, and
the override call swapped to ``set_distal_diameter_multiplier``.

CLI:
    --preflight                run 3 angles x 2 trials x 3 multipliers (0.5, 1.0, 2.0) instead of
                               the full 7 x 12 x 10 sweep (validation gate)
    --output <path>            override the tidy CSV output path
    --wall-time-output <path>  override the wall-time JSON output path

Expected full-sweep runtime: ~42-60 min on the local Windows workstation (840 trials). The sibling
t0029 length sweep completed in 2,541 s on the same workstation at the identical protocol.
Crash-recovery safe: ``fh.flush()`` runs after every row.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path
from typing import Any

from tasks.t0022_modify_dsgc_channel_testbed.code.constants import (
    ANGLE_STEP_DEG,
    N_ANGLES,
    N_TRIALS,
)
from tasks.t0039_distal_dendrite_diameter_sweep_t0022_gaba4.code.constants import (
    BASELINE_MULTIPLIER,
    DIAMETER_MULTIPLIERS,
    GABA_NULL_NS_VALUE,
    PREFLIGHT_ANGLES_DEG,
    PREFLIGHT_DIAMETER_MULTIPLIERS,
    PREFLIGHT_N_TRIALS,
    TIDY_CSV_HEADER,
)
from tasks.t0039_distal_dendrite_diameter_sweep_t0022_gaba4.code.diameter_override import (
    assert_distal_diameters,
    set_distal_diameter_multiplier,
)
from tasks.t0039_distal_dendrite_diameter_sweep_t0022_gaba4.code.gaba_override import (
    set_null_gaba_ns,
)
from tasks.t0039_distal_dendrite_diameter_sweep_t0022_gaba4.code.paths import (
    DATA_DIR,
    PER_DIAMETER_DIR,
    SWEEP_CSV,
    WALL_TIME_JSON,
    per_diameter_curve_csv,
)
from tasks.t0039_distal_dendrite_diameter_sweep_t0022_gaba4.code.trial_runner_diameter import (
    CellContext,
    build_cell_context,
    run_one_trial_diameter,
)


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="run 3 angles x 2 trials x 3 multipliers (validation gate)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="override tidy CSV output path",
    )
    parser.add_argument(
        "--wall-time-output",
        type=str,
        default=None,
        help="override wall-time JSON output path",
    )
    return parser.parse_args(argv)


def _select_sweep_grid(
    *,
    preflight: bool,
) -> tuple[tuple[float, ...], tuple[int, ...], int]:
    """Return (multipliers, angles_deg, n_trials) for the requested mode."""
    if preflight:
        return (
            PREFLIGHT_DIAMETER_MULTIPLIERS,
            PREFLIGHT_ANGLES_DEG,
            PREFLIGHT_N_TRIALS,
        )
    angles_deg: tuple[int, ...] = tuple(int(round(i * ANGLE_STEP_DEG)) for i in range(N_ANGLES))
    return (DIAMETER_MULTIPLIERS, angles_deg, N_TRIALS)


def _write_per_diameter_curve(
    *,
    multiplier: float,
    curve_rows: list[tuple[int, int, float]],
) -> Path:
    """Emit the per-diameter canonical 12-angle (or preflight 3-angle) CSV."""
    out_path: Path = per_diameter_curve_csv(multiplier=multiplier)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["angle_deg", "trial_seed", "firing_rate_hz"])
        for angle_deg, trial_seed, rate_hz in curve_rows:
            writer.writerow([int(angle_deg), int(trial_seed), f"{rate_hz:.6f}"])
    return out_path


def _run_one_diameter_point(
    *,
    ctx: CellContext,
    multiplier: float,
    angles_deg: tuple[int, ...],
    n_trials: int,
    tidy_writer: Any,
    tidy_fh: Any,
) -> list[tuple[int, int, float]]:
    """Run one full (angles x trials) inner loop at a fixed multiplier."""
    curve_rows: list[tuple[int, int, float]] = []
    for angle_idx, angle_deg in enumerate(angles_deg):
        for trial_idx in range(n_trials):
            trial_seed: int = 1000 * angle_idx + trial_idx + 1
            outcome = run_one_trial_diameter(
                ctx=ctx,
                angle_deg=float(angle_deg),
                trial_seed=trial_seed,
                multiplier=multiplier,
            )
            tidy_writer.writerow(
                [
                    f"{multiplier:.2f}",
                    trial_idx,
                    int(angle_deg),
                    outcome.spike_count,
                    f"{outcome.peak_mv:.3f}",
                    f"{outcome.firing_rate_hz:.6f}",
                ],
            )
            tidy_fh.flush()
            print(
                f"  D={multiplier:.2f}x  dir={int(angle_deg):3d}  trial={trial_idx}  "
                f"spikes={outcome.spike_count:3d}  rate={outcome.firing_rate_hz:6.2f}Hz  "
                f"peak={outcome.peak_mv:+.1f}mV",
                flush=True,
            )
            curve_rows.append(
                (int(angle_deg), int(trial_seed), float(outcome.firing_rate_hz)),
            )
    return curve_rows


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    multipliers, angles_deg, n_trials = _select_sweep_grid(preflight=args.preflight)

    out_csv: Path = Path(args.output) if args.output is not None else SWEEP_CSV
    out_wall: Path = (
        Path(args.wall_time_output) if args.wall_time_output is not None else WALL_TIME_JSON
    )

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PER_DIAMETER_DIR.mkdir(parents=True, exist_ok=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_wall.parent.mkdir(parents=True, exist_ok=True)

    print(f"[t0039 sweep] multipliers = {multipliers}", flush=True)
    print(f"[t0039 sweep] angles = {angles_deg}", flush=True)
    print(f"[t0039 sweep] n_trials per (multiplier, angle) = {n_trials}", flush=True)
    print(f"[t0039 sweep] GABA_NULL_NS = {GABA_NULL_NS_VALUE} (t0037 operational)", flush=True)
    print(f"[t0039 sweep] tidy CSV -> {out_csv}", flush=True)
    print(f"[t0039 sweep] per-diameter CSV dir -> {PER_DIAMETER_DIR}", flush=True)

    # Belt-and-braces: patch t0022 null-GABA at startup (trial_runner re-patches per trial too).
    set_null_gaba_ns(value_ns=GABA_NULL_NS_VALUE)

    print("[t0039 sweep] building DSGC cell + E-I pairs + distal snapshot...", flush=True)
    t_build_start: float = time.time()
    ctx = build_cell_context()
    t_build_end: float = time.time()
    print(
        f"[t0039 sweep] cell built in {t_build_end - t_build_start:.1f}s; "
        f"n_pairs = {len(ctx.pairs)}; n_distal = {len(ctx.distal_sections)}",
        flush=True,
    )

    wall_time_by_diameter: dict[str, float] = {}

    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(list(TIDY_CSV_HEADER))

        for multiplier in multipliers:
            t_d_start: float = time.time()
            curve_rows = _run_one_diameter_point(
                ctx=ctx,
                multiplier=float(multiplier),
                angles_deg=angles_deg,
                n_trials=n_trials,
                tidy_writer=writer,
                tidy_fh=fh,
            )
            curve_path: Path = _write_per_diameter_curve(
                multiplier=float(multiplier),
                curve_rows=curve_rows,
            )
            print(f"[t0039 sweep] wrote per-diameter curve -> {curve_path}", flush=True)

            t_d_end: float = time.time()
            wall_time_by_diameter[f"{multiplier:.2f}"] = t_d_end - t_d_start
            out_wall.write_text(
                json.dumps(wall_time_by_diameter, indent=2) + "\n",
                encoding="utf-8",
            )

    # Post-sweep guardrail: restore baseline seg.diam and confirm the override is idempotent.
    set_distal_diameter_multiplier(
        h=ctx.h,
        distal_sections=ctx.distal_sections,
        baseline_diam=ctx.baseline_diam,
        multiplier=BASELINE_MULTIPLIER,
    )
    assert_distal_diameters(
        h=ctx.h,
        distal_sections=ctx.distal_sections,
        baseline_diam=ctx.baseline_diam,
        multiplier=BASELINE_MULTIPLIER,
    )
    print("[t0039 sweep] baseline seg.diam restoration confirmed", flush=True)

    print(f"[t0039 sweep] wrote tidy CSV to {out_csv}", flush=True)
    print(f"[t0039 sweep] wrote wall-time JSON to {out_wall}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
