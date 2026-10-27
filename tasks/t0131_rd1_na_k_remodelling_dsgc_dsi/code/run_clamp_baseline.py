"""Step 7: replicate the +100 mV somatic voltage step on every reference cell (WT-like)."""

import argparse
import time

import pandas as pd

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_io import RefCell, load_reference_cells
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.clamp import (
    RECORD_ALL,
    ClampJob,
    run_clamp_job,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    MAX_WORKERS,
    MIN_TRANSIENT_ABS_NA,
    V_HOLD_MV,
    V_STEP_ABS_SENSITIVITY_MV,
    V_STEP_DELTA_MV,
    ScalingArm,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.parallel import run_jobs
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    CLAMP_BASELINE_CSV,
    CLAMP_SENSITIVITY_CSV,
    DATA_DIR,
)

BASELINE_JSONL_NAME: str = "clamp_baseline_rows.jsonl"
SENS_JSONL_NAME: str = "clamp_sensitivity_rows.jsonl"
N_SENSITIVITY_CELLS: int = 2


def _job(*, cell: RefCell, v_step_mv: float, tag: str) -> ClampJob:
    return ClampJob(
        job_key=f"{tag}|{cell.cell_id}",
        cell_id=cell.cell_id,
        vector_68d=cell.vector_68d,
        s_na=1.0,
        s_k=1.0,
        arm=str(ScalingArm.SOMA_AIS),
        v_hold_mv=V_HOLD_MV,
        v_step_mv=v_step_mv,
        record_channels=RECORD_ALL,
        save_trace=True,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--workers", type=int, default=MAX_WORKERS)
    args = ap.parse_args()
    cells = load_reference_cells(limit=args.limit)
    t0 = time.time()
    jobs = [_job(cell=c, v_step_mv=V_HOLD_MV + V_STEP_DELTA_MV, tag="delta100") for c in cells]
    rows = run_jobs(
        jobs=jobs,
        worker_fn=run_clamp_job,
        out_path=DATA_DIR / BASELINE_JSONL_NAME,
        key_of=lambda j: j.job_key,
        max_workers=args.workers,
        desc="clamp_baseline",
    )
    print(f"baseline wall time {time.time() - t0:.1f} s for {len(jobs)} runs")
    df = pd.DataFrame([rows[j.job_key] for j in jobs])
    df["na_transient_ok"] = df["na_transient_na"].abs() > MIN_TRANSIENT_ABS_NA
    df["sustained_positive"] = df["sustained_na"] > 0.0
    df.to_csv(CLAMP_BASELINE_CSV, index=False)
    print(df[["cell_id", "baseline_na", "sustained_na", "na_transient_na", "total_early_min_na"]])
    sens_cells = cells[:N_SENSITIVITY_CELLS]
    sens_jobs = [_job(cell=c, v_step_mv=V_STEP_ABS_SENSITIVITY_MV, tag="abs40") for c in sens_cells]
    sens_rows = run_jobs(
        jobs=sens_jobs,
        worker_fn=run_clamp_job,
        out_path=DATA_DIR / SENS_JSONL_NAME,
        key_of=lambda j: j.job_key,
        max_workers=args.workers,
        desc="clamp_sensitivity",
    )
    pd.DataFrame([sens_rows[j.job_key] for j in sens_jobs]).to_csv(
        CLAMP_SENSITIVITY_CSV, index=False
    )


if __name__ == "__main__":
    main()
