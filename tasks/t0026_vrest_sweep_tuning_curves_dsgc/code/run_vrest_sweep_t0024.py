"""t0024 V_rest sweep driver (correlated AR(2), rho = 0.6).

Iterates ``V_REST_VALUES_MV`` x ``ANGLES_DEG`` x ``N_TRIALS_T0024`` and writes a
tidy CSV plus a per-V_rest wall-time JSON log. Always uses the correlated
condition (``AR2_RHO_T0024 = 0.6``).

CLI:
    --limit-vrest <mv>   restrict the sweep to a single V_rest value
    --limit-trials <n>   cap the trial count (default: N_TRIALS_T0024)
    --output <path>      override the tidy CSV output path
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

from tasks.t0026_vrest_sweep_tuning_curves_dsgc.code.constants import (
    ANGLES_DEG,
    AR2_RHO_T0024,
    CSV_COLUMNS,
    DATA_T0024_DIR,
    N_TRIALS_T0024,
    V_REST_VALUES_MV,
    VREST_TIDY_T0024,
    WALL_TIME_T0024,
)
from tasks.t0026_vrest_sweep_tuning_curves_dsgc.code.trial_runner_t0024 import (
    build_cell_context,
    run_one_trial_vrest,
)


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit-vrest",
        type=float,
        default=None,
        help="restrict sweep to a single V_rest value in mV",
    )
    parser.add_argument(
        "--limit-trials",
        type=int,
        default=None,
        help="cap trial count per angle (default: N_TRIALS_T0024)",
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


def _select_vrest_values(
    *,
    full_values: tuple[float, ...],
    limit_value: float | None,
) -> tuple[float, ...]:
    if limit_value is None:
        return full_values
    match = [v for v in full_values if abs(v - limit_value) < 1e-9]
    if len(match) == 0:
        raise ValueError(
            f"--limit-vrest={limit_value} not in V_REST_VALUES_MV {full_values!r}",
        )
    return tuple(match)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    vrest_values: tuple[float, ...] = _select_vrest_values(
        full_values=V_REST_VALUES_MV,
        limit_value=args.limit_vrest,
    )
    n_trials: int = (
        N_TRIALS_T0024 if args.limit_trials is None else min(args.limit_trials, N_TRIALS_T0024)
    )

    out_csv: Path = Path(args.output) if args.output is not None else VREST_TIDY_T0024
    out_wall: Path = (
        Path(args.wall_time_output) if args.wall_time_output is not None else WALL_TIME_T0024
    )

    DATA_T0024_DIR.mkdir(parents=True, exist_ok=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_wall.parent.mkdir(parents=True, exist_ok=True)

    print(f"[t0024 sweep] V_rest values = {vrest_values}", flush=True)
    print(f"[t0024 sweep] angles = {ANGLES_DEG}", flush=True)
    print(f"[t0024 sweep] n_trials per (V_rest, angle) = {n_trials}", flush=True)
    print(f"[t0024 sweep] rho = {AR2_RHO_T0024}", flush=True)
    print(f"[t0024 sweep] tidy CSV -> {out_csv}", flush=True)

    print("[t0024 sweep] building DSGC cell + synapse bundle (one-time)...", flush=True)
    t_build_start: float = time.time()
    ctx = build_cell_context()
    t_build_end: float = time.time()
    print(
        f"[t0024 sweep] cell built in {t_build_end - t_build_start:.1f}s; "
        f"n_terminals = {len(ctx.cell.terminal_dends)}",
        flush=True,
    )

    wall_time_by_vrest: dict[str, float] = {}

    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(list(CSV_COLUMNS))

        for v_rest_mv in vrest_values:
            t_vrest_start: float = time.time()
            for _angle_idx, angle_deg in enumerate(ANGLES_DEG):
                for trial_idx in range(n_trials):
                    seed: int = 3000 + trial_idx * 10_007 + int(angle_deg) * 13
                    outcome = run_one_trial_vrest(
                        ctx=ctx,
                        direction_deg=float(angle_deg),
                        rho=AR2_RHO_T0024,
                        seed=seed,
                        v_rest_mv=v_rest_mv,
                    )
                    writer.writerow(
                        [
                            f"{v_rest_mv:.1f}",
                            trial_idx,
                            int(angle_deg),
                            outcome.spike_count,
                            f"{outcome.peak_mv:.3f}",
                            f"{outcome.firing_rate_hz:.6f}",
                        ],
                    )
                    fh.flush()
                    print(
                        f"  V={v_rest_mv:+.1f}mV  dir={int(angle_deg):3d}  "
                        f"trial={trial_idx:2d}  spikes={outcome.spike_count:3d}  "
                        f"rate={outcome.firing_rate_hz:6.2f}Hz  peak={outcome.peak_mv:+.1f}mV",
                        flush=True,
                    )
            t_vrest_end: float = time.time()
            wall_time_by_vrest[f"{v_rest_mv:.1f}"] = t_vrest_end - t_vrest_start
            out_wall.write_text(
                json.dumps(wall_time_by_vrest, indent=2) + "\n",
                encoding="utf-8",
            )

    print(f"[t0024 sweep] wrote tidy CSV to {out_csv}", flush=True)
    print(f"[t0024 sweep] wrote wall-time JSON to {out_wall}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
