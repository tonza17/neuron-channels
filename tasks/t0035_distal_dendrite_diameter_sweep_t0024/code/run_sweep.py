"""t0035 distal-dendrite diameter sweep driver (t0024 DSGC testbed).

Iterates ``DIAMETER_MULTIPLIERS`` x 12 angles x ``N_TRIALS_T0024`` and writes a tidy CSV with one
row per trial plus a per-diameter canonical 12-angle curve CSV (accepted by the t0012
``tuning_curve_loss`` scorer). Structurally cloned from
``tasks/t0034_distal_dendrite_length_sweep_t0024/code/run_sweep.py`` with the sweep grid renamed to
``DIAMETER_MULTIPLIERS``, the tidy-CSV first column renamed to ``diameter_multiplier``, and the
override call swapped to ``set_distal_diameter_multiplier``.

CLI:
    --preflight          run 3 angles x 2 trials x 3 multipliers (0.5, 1.0, 2.0) instead of the
                         full 7 x 12 x 10 sweep (validation gate)
    --output <path>      override the tidy CSV output path
    --wall-time-output <path>  override the wall-time JSON path

Expected full-sweep runtime: ~2.8-3 h on the local Windows workstation (840 trials at ~12 s/trial
plus ~10-15% overhead at thinner diameters per t0030 observation). Crash-recovery safe:
``fh.flush()`` runs after every row.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path
from typing import Any

from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C
from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.constants import (
    AR2_RHO,
    BASELINE_MULTIPLIER,
    DIAMETER_ASSERT_TOL_UM,
    DIAMETER_MULTIPLIERS,
    N_TRIALS_T0024,
    PREFLIGHT_ANGLES_DEG,
    PREFLIGHT_DIAMETER_MULTIPLIERS,
    PREFLIGHT_N_TRIALS,
    SEED_ANGLE_STRIDE,
    SEED_DIAMETER_STRIDE,
    TIDY_CSV_HEADER,
)
from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.diameter_override_t0024 import (
    assert_distal_diameters,
    set_distal_diameter_multiplier,
)
from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.paths import (
    DATA_DIR,
    PER_DIAMETER_DIR,
    SWEEP_CSV,
    WALL_TIME_JSON,
    per_diameter_curve_csv,
)
from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.trial_runner_diameter_t0024 import (
    CellContextT0024Diameter,
    build_cell_context,
    run_one_trial_diameter,
)

# AR(2) rho guard -- confirms the t0024 library constant has not been edited since planning.
assert C.AR2_CROSS_CORR_RHO_CORRELATED == AR2_RHO, (
    f"t0024 AR2_CROSS_CORR_RHO_CORRELATED drift: "
    f"expected {AR2_RHO}, got {C.AR2_CROSS_CORR_RHO_CORRELATED}"
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
    return (DIAMETER_MULTIPLIERS, C.ANGLES_12ANG_DEG, N_TRIALS_T0024)


def _write_per_diameter_curve(
    *,
    multiplier: float,
    curve_rows: list[tuple[int, int, float]],
) -> Path:
    """Emit the per-diameter canonical (12-angle or preflight 3-angle) CSV."""
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
    ctx: CellContextT0024Diameter,
    diameter_idx: int,
    multiplier: float,
    angles_deg: tuple[int, ...],
    n_trials: int,
    tidy_writer: Any,
    tidy_fh: Any,
    seed_set: set[int],
) -> list[tuple[int, int, float]]:
    """Run one full (angles x trials) inner loop at a fixed multiplier.

    ``set_distal_diameter_multiplier`` is NOT called here -- the outer ``main`` function does it
    once per sweep point before calling this helper.
    """
    curve_rows: list[tuple[int, int, float]] = []
    for angle_idx, angle_deg in enumerate(angles_deg):
        for trial_idx in range(n_trials):
            trial_seed: int = (
                diameter_idx * SEED_DIAMETER_STRIDE + SEED_ANGLE_STRIDE * angle_idx + trial_idx + 1
            )
            if trial_seed in seed_set:
                raise AssertionError(
                    f"trial_seed collision: {trial_seed} (diameter_idx={diameter_idx}, "
                    f"angle_idx={angle_idx}, trial_idx={trial_idx})",
                )
            seed_set.add(trial_seed)
            outcome = run_one_trial_diameter(
                ctx=ctx,
                direction_deg=float(angle_deg),
                trial_seed=trial_seed,
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

    print(f"[t0035 sweep] multipliers = {multipliers}", flush=True)
    print(f"[t0035 sweep] angles = {angles_deg}", flush=True)
    print(f"[t0035 sweep] n_trials per (multiplier, angle) = {n_trials}", flush=True)
    print(f"[t0035 sweep] AR2 rho = {AR2_RHO}", flush=True)
    print(f"[t0035 sweep] tidy CSV -> {out_csv}", flush=True)
    print(f"[t0035 sweep] per-diameter CSV dir -> {PER_DIAMETER_DIR}", flush=True)

    print(
        "[t0035 sweep] building t0024 DSGC cell + synapse bundle + distal snapshot...",
        flush=True,
    )
    t_build_start: float = time.time()
    ctx = build_cell_context()
    t_build_end: float = time.time()
    print(
        f"[t0035 sweep] cell built in {t_build_end - t_build_start:.1f}s; "
        f"n_terminals = {len(ctx.cell.terminal_dends)}; "
        f"n_distal = {len(ctx.distal_sections)}",
        flush=True,
    )

    wall_time_by_diameter: dict[str, float] = {}
    seed_set: set[int] = set()

    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(list(TIDY_CSV_HEADER))

        for diameter_idx, multiplier in enumerate(multipliers):
            # Apply the distal-diameter override ONCE per outer sweep iteration.
            set_distal_diameter_multiplier(
                h=ctx.cell.h,
                distal_sections=ctx.distal_sections,
                baseline_diam=ctx.baseline_diam,
                multiplier=float(multiplier),
            )
            assert_distal_diameters(
                h=ctx.cell.h,
                distal_sections=ctx.distal_sections,
                baseline_diam=ctx.baseline_diam,
                multiplier=float(multiplier),
                tol=DIAMETER_ASSERT_TOL_UM,
            )
            ctx.current_multiplier = float(multiplier)
            print(
                f"[t0035 sweep] applied distal diam x {multiplier:.2f} to "
                f"{len(ctx.distal_sections)} sections",
                flush=True,
            )

            t_d_start: float = time.time()
            curve_rows = _run_one_diameter_point(
                ctx=ctx,
                diameter_idx=diameter_idx,
                multiplier=float(multiplier),
                angles_deg=angles_deg,
                n_trials=n_trials,
                tidy_writer=writer,
                tidy_fh=fh,
                seed_set=seed_set,
            )
            curve_path: Path = _write_per_diameter_curve(
                multiplier=float(multiplier),
                curve_rows=curve_rows,
            )
            print(f"[t0035 sweep] wrote per-diameter curve -> {curve_path}", flush=True)

            t_d_end: float = time.time()
            wall_time_by_diameter[f"{multiplier:.2f}"] = t_d_end - t_d_start
            out_wall.write_text(
                json.dumps(wall_time_by_diameter, indent=2) + "\n",
                encoding="utf-8",
            )

    # Post-sweep guardrail: restore baseline seg.diam and confirm the override is idempotent.
    set_distal_diameter_multiplier(
        h=ctx.cell.h,
        distal_sections=ctx.distal_sections,
        baseline_diam=ctx.baseline_diam,
        multiplier=BASELINE_MULTIPLIER,
    )
    assert_distal_diameters(
        h=ctx.cell.h,
        distal_sections=ctx.distal_sections,
        baseline_diam=ctx.baseline_diam,
        multiplier=BASELINE_MULTIPLIER,
        tol=DIAMETER_ASSERT_TOL_UM,
    )
    ctx.current_multiplier = BASELINE_MULTIPLIER
    print("[t0035 sweep] baseline seg.diam restoration confirmed", flush=True)

    # Seed uniqueness guardrail.
    expected_trial_count: int = len(multipliers) * len(angles_deg) * n_trials
    if len(seed_set) != expected_trial_count:
        raise AssertionError(
            f"seed uniqueness violation: expected {expected_trial_count} unique seeds, "
            f"got {len(seed_set)}",
        )
    print(
        f"[t0035 sweep] seed uniqueness confirmed ({len(seed_set)} unique seeds)",
        flush=True,
    )

    print(f"[t0035 sweep] wrote tidy CSV to {out_csv}", flush=True)
    print(f"[t0035 sweep] wrote wall-time JSON to {out_wall}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
