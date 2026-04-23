"""t0037 null-GABA reduction ladder sweep driver.

Iterates ``GABA_LEVELS_NS`` x 12 angles x ``N_TRIALS`` (10 by default) and writes a tidy CSV with
one row per trial plus a per-GABA canonical 12-angle curve CSV (accepted by the t0012
``tuning_curve_loss`` scorer). Structural clone of
``tasks/t0036_rerun_t0030_halved_null_gaba/code/run_sweep.py`` with the outer-loop parameter
changed from distal diameter multiplier to null-GABA conductance (nS), and no diameter override
(distal diameter is locked at 1.0x baseline).

CLI:
    --preflight                run 3 GABA levels x 3 angles x 2 trials = 18 trials instead of
                               the full 5 x 12 x 10 = 600 trial sweep (validation gate)
    --output <path>            override the tidy CSV output path
    --wall-time-output <path>  override the wall-time JSON output path

Expected full-sweep runtime: ~20-30 min on the local Windows workstation (600 trials).
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
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.constants import (
    GABA_LEVELS_NS,
    PREFLIGHT_ANGLES_DEG,
    PREFLIGHT_GABA_LEVELS_NS,
    PREFLIGHT_N_TRIALS,
    TIDY_CSV_HEADER,
)
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.gaba_override import set_null_gaba_ns
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.paths import (
    DATA_DIR,
    PER_GABA_DIR,
    SWEEP_CSV,
    WALL_TIME_JSON,
    per_gaba_curve_csv,
)
from tasks.t0037_null_gaba_reduction_ladder_t0022.code.trial_runner_gaba_ladder import (
    CellContext,
    build_cell_context,
    run_single_trial_gaba,
)


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="run 3 GABA levels x 3 angles x 2 trials (validation gate)",
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
    """Return ``(gaba_levels_ns, angles_deg, n_trials)`` for the requested mode."""
    if preflight:
        return (
            PREFLIGHT_GABA_LEVELS_NS,
            PREFLIGHT_ANGLES_DEG,
            PREFLIGHT_N_TRIALS,
        )
    angles_deg: tuple[int, ...] = tuple(int(round(i * ANGLE_STEP_DEG)) for i in range(N_ANGLES))
    return (GABA_LEVELS_NS, angles_deg, N_TRIALS)


def _write_per_gaba_curve(
    *,
    gaba_null_ns: float,
    curve_rows: list[tuple[int, int, float]],
) -> Path:
    """Emit the per-GABA canonical 12-angle (or preflight 3-angle) CSV."""
    out_path: Path = per_gaba_curve_csv(gaba_null_ns=gaba_null_ns)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["angle_deg", "trial_seed", "firing_rate_hz"])
        for angle_deg, trial_seed, rate_hz in curve_rows:
            writer.writerow([int(angle_deg), int(trial_seed), f"{rate_hz:.6f}"])
    return out_path


def _run_one_gaba_point(
    *,
    ctx: CellContext,
    gaba_null_ns: float,
    angles_deg: tuple[int, ...],
    n_trials: int,
    tidy_writer: Any,
    tidy_fh: Any,
) -> list[tuple[int, int, float]]:
    """Run one full (angles x trials) inner loop at a fixed GABA conductance."""
    curve_rows: list[tuple[int, int, float]] = []
    for angle_idx, angle_deg in enumerate(angles_deg):
        for trial_idx in range(n_trials):
            trial_seed: int = 1000 * angle_idx + trial_idx + 1
            outcome = run_single_trial_gaba(
                ctx=ctx,
                angle_deg=float(angle_deg),
                trial_seed=trial_seed,
                gaba_null_ns=gaba_null_ns,
            )
            tidy_writer.writerow(
                [
                    f"{gaba_null_ns:.2f}",
                    trial_idx,
                    int(angle_deg),
                    outcome.spike_count,
                    f"{outcome.peak_mv:.3f}",
                    f"{outcome.firing_rate_hz:.6f}",
                ],
            )
            tidy_fh.flush()
            print(
                f"  G={gaba_null_ns:.2f}nS  dir={int(angle_deg):3d}  trial={trial_idx}  "
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

    gaba_levels, angles_deg, n_trials = _select_sweep_grid(preflight=args.preflight)

    out_csv: Path = Path(args.output) if args.output is not None else SWEEP_CSV
    out_wall: Path = (
        Path(args.wall_time_output) if args.wall_time_output is not None else WALL_TIME_JSON
    )

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PER_GABA_DIR.mkdir(parents=True, exist_ok=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_wall.parent.mkdir(parents=True, exist_ok=True)

    print(f"[t0037 sweep] gaba_levels_ns = {gaba_levels}", flush=True)
    print(f"[t0037 sweep] angles = {angles_deg}", flush=True)
    print(f"[t0037 sweep] n_trials per (GABA, angle) = {n_trials}", flush=True)
    print(f"[t0037 sweep] tidy CSV -> {out_csv}", flush=True)
    print(f"[t0037 sweep] per-GABA CSV dir -> {PER_GABA_DIR}", flush=True)

    print("[t0037 sweep] building DSGC cell + E-I pairs + distal snapshot...", flush=True)
    t_build_start: float = time.time()
    ctx = build_cell_context()
    t_build_end: float = time.time()
    print(
        f"[t0037 sweep] cell built in {t_build_end - t_build_start:.1f}s; "
        f"n_pairs = {len(ctx.pairs)}; n_distal = {len(ctx.distal_sections)}",
        flush=True,
    )

    wall_time_by_gaba: dict[str, float] = {}

    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(list(TIDY_CSV_HEADER))

        for gaba_ns in gaba_levels:
            # Outer-loop GABA patch (belt-and-braces; every trial also calls set_null_gaba_ns).
            set_null_gaba_ns(value_ns=float(gaba_ns))
            t_g_start: float = time.time()
            curve_rows = _run_one_gaba_point(
                ctx=ctx,
                gaba_null_ns=float(gaba_ns),
                angles_deg=angles_deg,
                n_trials=n_trials,
                tidy_writer=writer,
                tidy_fh=fh,
            )
            curve_path: Path = _write_per_gaba_curve(
                gaba_null_ns=float(gaba_ns),
                curve_rows=curve_rows,
            )
            print(f"[t0037 sweep] wrote per-GABA curve -> {curve_path}", flush=True)

            t_g_end: float = time.time()
            wall_time_by_gaba[f"{gaba_ns:.2f}"] = t_g_end - t_g_start
            out_wall.write_text(
                json.dumps(wall_time_by_gaba, indent=2) + "\n",
                encoding="utf-8",
            )

    print(f"[t0037 sweep] wrote tidy CSV to {out_csv}", flush=True)
    print(f"[t0037 sweep] wrote wall-time JSON to {out_wall}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
