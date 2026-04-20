"""Run the 12-angle x 20-trial drifting-bar tuning curve.

Emits a canonical-schema CSV at ``data/tuning_curves/curve_modeldb_189347.csv``
with columns ``(angle_deg, trial_seed, firing_rate_hz)`` — the exact schema
that the t0012 ``tuning_curve_loss`` library expects.

The cell is built once and reused for all 240 trials. Each trial:

  1. sets per-trial seed and restores baseline synapse coords,
  2. rotates coords to the target angle,
  3. reruns ``update()`` + ``placeBIP()``,
  4. calls ``h.finitialize`` + ``h.continuerun(tstop)``,
  5. counts soma upward threshold crossings -> firing rate (Hz).

Angles: 0, 30, 60, ..., 330 deg (12 angles, 30 deg step).
Trial seeds: 1..20 (matches the 20-trial envelope protocol).
"""

from __future__ import annotations

import csv
import sys

from tqdm import tqdm

from tasks.t0008_port_modeldb_189347.code.build_cell import (
    build_dsgc,
    get_cell_summary,
    read_synapse_coords,
    run_one_trial,
)
from tasks.t0008_port_modeldb_189347.code.constants import (
    ANGLE_STEP_DEG,
    N_ANGLES,
    N_TRIALS,
)
from tasks.t0008_port_modeldb_189347.code.paths import (
    TUNING_CURVE_MODELDB_CSV,
    TUNING_CURVES_DIR,
)


def main() -> int:
    print("Building DSGC for tuning-curve sweep...", flush=True)
    h = build_dsgc()
    summary = get_cell_summary(h=h)
    baseline = read_synapse_coords(h=h)
    print(
        f"  countON={summary.num_on_sections} numsyn={summary.num_synapses}",
        flush=True,
    )

    TUNING_CURVES_DIR.mkdir(parents=True, exist_ok=True)

    total_trials = N_ANGLES * N_TRIALS
    bar = tqdm(total=total_trials, desc="trials", unit="trial")
    rows: list[tuple[int, int, float]] = []
    for angle_idx in range(N_ANGLES):
        angle_deg = angle_idx * ANGLE_STEP_DEG
        for trial_idx in range(N_TRIALS):
            seed = trial_idx + 1
            rate = run_one_trial(
                h=h,
                angle_deg=angle_deg,
                seed=seed,
                baseline_coords=baseline,
            )
            rows.append((int(angle_deg), seed, rate))
            bar.update(1)
    bar.close()

    with TUNING_CURVE_MODELDB_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["angle_deg", "trial_seed", "firing_rate_hz"])
        for angle_deg_val, seed_val, rate_val in rows:
            writer.writerow([angle_deg_val, seed_val, f"{rate_val:.6f}"])

    # Per-angle mean for quick inspection.
    print("", flush=True)
    for angle_idx in range(N_ANGLES):
        angle_deg = int(angle_idx * ANGLE_STEP_DEG)
        rates_at_angle = [r[2] for r in rows if r[0] == angle_deg]
        mean_rate = sum(rates_at_angle) / len(rates_at_angle)
        n_trials = len(rates_at_angle)
        print(
            f"  angle={angle_deg:3d} deg  mean={mean_rate:6.2f} Hz  (n={n_trials})",
            flush=True,
        )

    print(f"\nWrote {TUNING_CURVE_MODELDB_CSV}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
