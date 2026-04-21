"""Generate polar + Cartesian PNG plots for the t0024 DSGC port.

Plan step 14: produces ``results/images/tuning_curve_12ang.png`` plus the
uncorrelated counterpart and matching Cartesian plots from the 12-angle sweep
CSVs (correlated and uncorrelated). 8-direction plots are skipped because the
t0011/t0012 plotting library hard-codes a 12-angle grid; 8-direction data is
still used by ``score_envelope.py`` for the paper-match port-fidelity gate.

Inputs are the raw ``run_tuning_curve.py`` CSVs with columns
``trial,direction_deg,spike_count,peak_mv``. They are converted in-memory to
the canonical t0011/t0012 schema ``angle_deg,trial_seed,firing_rate_hz`` before
being handed to the t0011 plotting library.
"""

from __future__ import annotations

import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from tasks.t0011_response_visualization_library.code.tuning_curve_viz.cartesian import (
    plot_cartesian_tuning_curve,
)
from tasks.t0011_response_visualization_library.code.tuning_curve_viz.polar import (
    plot_polar_tuning_curve,
)
from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C
from tasks.t0024_port_de_rosenroll_2026_dsgc.code import paths as P

# Raw run_tuning_curve.py columns.
TRIAL_COL: str = "trial"
DIRECTION_COL: str = "direction_deg"
SPIKE_COUNT_COL: str = "spike_count"

# Canonical t0011/t0012 columns.
ANGLE_COL_OUT: str = "angle_deg"
TRIAL_SEED_COL_OUT: str = "trial_seed"
FIRING_RATE_COL_OUT: str = "firing_rate_hz"


@dataclass(frozen=True, slots=True)
class PlotJob:
    raw_csv: Path
    polar_png: Path
    cartesian_png: Path
    label: str


def _to_canonical_csv(*, raw_csv: Path, out_csv: Path) -> None:
    """Convert a raw run_tuning_curve.py CSV to the canonical schema."""
    df_raw = pd.read_csv(filepath_or_buffer=raw_csv)
    duration_s = C.TSTOP_MS / 1000.0
    df_out = pd.DataFrame(
        {
            ANGLE_COL_OUT: df_raw[DIRECTION_COL].astype(float),
            TRIAL_SEED_COL_OUT: df_raw[TRIAL_COL].astype(int),
            FIRING_RATE_COL_OUT: df_raw[SPIKE_COUNT_COL].astype(float) / duration_s,
        }
    )
    df_out.to_csv(path_or_buf=out_csv, index=False)


def _render_one(*, job: PlotJob, work_dir: Path) -> None:
    canonical_csv = work_dir / f"{job.raw_csv.stem}.canonical.csv"
    _to_canonical_csv(raw_csv=job.raw_csv, out_csv=canonical_csv)

    job.polar_png.parent.mkdir(parents=True, exist_ok=True)
    job.cartesian_png.parent.mkdir(parents=True, exist_ok=True)

    plot_polar_tuning_curve(curve_csv=canonical_csv, out_png=job.polar_png)
    print(f"[{job.label}] wrote polar -> {job.polar_png}")

    plot_cartesian_tuning_curve(curve_csv=canonical_csv, out_png=job.cartesian_png)
    print(f"[{job.label}] wrote cartesian -> {job.cartesian_png}")


def main() -> int:
    jobs: list[PlotJob] = [
        PlotJob(
            raw_csv=P.TUNING_CURVE_12ANG_CORR_CSV,
            polar_png=P.IMAGES_DIR / "tuning_curve_12ang.png",
            cartesian_png=P.IMAGES_DIR / "tuning_curve_12ang_cartesian.png",
            label="12ang/correlated",
        ),
        PlotJob(
            raw_csv=P.TUNING_CURVE_12ANG_UNCORR_CSV,
            polar_png=P.IMAGES_DIR / "tuning_curve_12ang_uncorrelated.png",
            cartesian_png=P.IMAGES_DIR / "tuning_curve_12ang_uncorrelated_cartesian.png",
            label="12ang/uncorrelated",
        ),
    ]

    missing: list[Path] = [j.raw_csv for j in jobs if not j.raw_csv.exists()]
    if len(missing) > 0:
        for m in missing:
            print(f"ERROR: missing input CSV: {m}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as td:
        work_dir = Path(td)
        for job in jobs:
            _render_one(job=job, work_dir=work_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
