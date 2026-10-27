"""Step 8: gNa x gK voltage-clamp grid, per-cell fit and verification clamp (clamp data only)."""

import argparse
import json
import time
from typing import Any

import numpy as np
import pandas as pd

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.calibration import (
    CellFit,
    GridPoint,
    fit_cell,
    ratio_grids,
    within_tolerance,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_io import RefCell, load_reference_cells
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.clamp import (
    RECORD_ALL,
    RECORD_NA,
    ClampJob,
    run_clamp_job,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    MAX_WORKERS,
    S_K_GRID,
    S_NA_GRID,
    TARGET_SUSTAINED_RATIO,
    TARGET_TRANSIENT_RATIO,
    TRANSIENT_RATIO_SENSITIVITY,
    V_HOLD_MV,
    V_STEP_DELTA_MV,
    ScalingArm,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.parallel import run_jobs
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    CLAMP_GRID_CSV,
    DATA_DIR,
    FITTED_SCALINGS_JSON,
    with_arm_suffix,
)

V_STEP_MV: float = V_HOLD_MV + V_STEP_DELTA_MV


def _grid_job(*, cell: RefCell, s_na: float, s_k: float, arm: str) -> ClampJob:
    return ClampJob(
        job_key=f"grid|{arm}|{cell.cell_id}|{s_na:.4f}|{s_k:.4f}",
        cell_id=cell.cell_id,
        vector_68d=cell.vector_68d,
        s_na=s_na,
        s_k=s_k,
        arm=arm,
        v_hold_mv=V_HOLD_MV,
        v_step_mv=V_STEP_MV,
        record_channels=RECORD_NA,
        save_trace=False,
    )


def _spread(*, values: list[float]) -> dict[str, float]:
    a = np.asarray(values, dtype=np.float64)
    q1, q3 = np.percentile(a, [25, 75])
    return {
        "mean": float(a.mean()),
        "sd": float(a.std(ddof=1)) if len(a) > 1 else 0.0,
        "min": float(a.min()),
        "max": float(a.max()),
        "median": float(np.median(a)),
        "iqr": float(q3 - q1),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--workers", type=int, default=MAX_WORKERS)
    ap.add_argument("--arm", type=str, default=str(ScalingArm.SOMA_AIS))
    args = ap.parse_args()
    arm: str = args.arm
    cells = load_reference_cells(limit=args.limit)
    t0 = time.time()
    jobs = [
        _grid_job(cell=c, s_na=sn, s_k=sk, arm=arm)
        for c in cells
        for sn in S_NA_GRID
        for sk in S_K_GRID
    ]
    rows = run_jobs(
        jobs=jobs,
        worker_fn=run_clamp_job,
        out_path=with_arm_suffix(path=DATA_DIR / "clamp_grid_rows.jsonl", arm=arm),
        key_of=lambda j: j.job_key,
        max_workers=args.workers,
        desc=f"clamp_grid_{arm}",
    )
    print(f"grid wall time {time.time() - t0:.1f} s for {len(jobs)} runs", flush=True)
    by_cell: dict[str, list[GridPoint]] = {}
    for c in cells:
        pts: list[GridPoint] = []
        for sn in S_NA_GRID:
            for sk in S_K_GRID:
                r = rows[f"grid|{arm}|{c.cell_id}|{sn:.4f}|{sk:.4f}"]
                pts.append(
                    GridPoint(
                        s_na=sn,
                        s_k=sk,
                        sustained_na=float(r["sustained_na"]),
                        na_transient_na=float(r["na_transient_na"]),
                    )
                )
        by_cell[c.cell_id] = pts
    grid_rows: list[dict[str, Any]] = []
    fits: dict[str, CellFit] = {}
    fits_sens: dict[float, dict[str, CellFit]] = {t: {} for t in TRANSIENT_RATIO_SENSITIVITY}
    for c in cells:
        pts = by_cell[c.cell_id]
        grids = ratio_grids(points=pts)
        fits[c.cell_id] = fit_cell(cell_id=c.cell_id, grids=grids)
        for t in TRANSIENT_RATIO_SENSITIVITY:
            fits_sens[t][c.cell_id] = fit_cell(cell_id=c.cell_id, grids=grids, target_transient=t)
        for i, sn in enumerate(S_NA_GRID):
            for j, sk in enumerate(S_K_GRID):
                p = pts[i * len(S_K_GRID) + j]
                grid_rows.append(
                    {
                        "cell_id": c.cell_id,
                        "arm": arm,
                        "s_na": sn,
                        "s_k": sk,
                        "sustained_na": p.sustained_na,
                        "transient_na": p.na_transient_na,
                        "sustained_ratio": float(grids.sustained[i, j]),
                        "transient_ratio": float(grids.transient[i, j]),
                    }
                )
    pd.DataFrame(grid_rows).to_csv(with_arm_suffix(path=CLAMP_GRID_CSV, arm=arm), index=False)

    # Verification clamp at the refined fitted points (direct simulation, traces saved).
    ver_jobs = [
        ClampJob(
            job_key=f"verify|{arm}|{c.cell_id}",
            cell_id=c.cell_id,
            vector_68d=c.vector_68d,
            s_na=fits[c.cell_id].s_na_fit,
            s_k=fits[c.cell_id].s_k_fit,
            arm=arm,
            v_hold_mv=V_HOLD_MV,
            v_step_mv=V_STEP_MV,
            record_channels=RECORD_ALL,
            save_trace=True,
        )
        for c in cells
    ]
    ver_rows = run_jobs(
        jobs=ver_jobs,
        worker_fn=run_clamp_job,
        out_path=with_arm_suffix(path=DATA_DIR / "clamp_verify_rows.jsonl", arm=arm),
        key_of=lambda j: j.job_key,
        max_workers=args.workers,
        desc=f"clamp_verify_{arm}",
    )
    per_cell: dict[str, Any] = {}
    for c in cells:
        f = fits[c.cell_id]
        ref = rows[f"grid|{arm}|{c.cell_id}|{1.0:.4f}|{1.0:.4f}"]
        v = ver_rows[f"verify|{arm}|{c.cell_id}"]
        ach_s = float(v["sustained_na"]) / float(ref["sustained_na"])
        ach_t = float(v["na_transient_na"]) / float(ref["na_transient_na"])
        per_cell[c.cell_id] = {
            "s_na_fit": f.s_na_fit,
            "s_k_fit": f.s_k_fit,
            "interp_sustained_ratio": f.pred_sustained_ratio,
            "interp_transient_ratio": f.pred_transient_ratio,
            "achieved_sustained_ratio": ach_s,
            "achieved_transient_ratio": ach_t,
            "sustained_within_tolerance": within_tolerance(sustained_ratio=ach_s),
            "loss_interp": f.loss,
            "grid_best_s_na": f.grid_best_s_na,
            "grid_best_s_k": f.grid_best_s_k,
            "grid_best_loss": f.grid_best_loss,
            "max_grid_sustained_ratio": f.max_grid_sustained_ratio,
            "failed_sustained_reach": f.failed_sustained_reach,
            "wt_sustained_na": float(ref["sustained_na"]),
            "wt_na_transient_na": float(ref["na_transient_na"]),
            "rd1_sustained_na": float(v["sustained_na"]),
            "rd1_na_transient_na": float(v["na_transient_na"]),
        }
    summary: dict[str, Any] = {
        "arm": arm,
        "targets": {
            "sustained_ratio": TARGET_SUSTAINED_RATIO,
            "transient_ratio": TARGET_TRANSIENT_RATIO,
        },
        "cells": per_cell,
        "spread_s_na": _spread(values=[f.s_na_fit for f in fits.values()]),
        "spread_s_k": _spread(values=[f.s_k_fit for f in fits.values()]),
        "spread_achieved_sustained": _spread(
            values=[d["achieved_sustained_ratio"] for d in per_cell.values()]
        ),
        "spread_achieved_transient": _spread(
            values=[d["achieved_transient_ratio"] for d in per_cell.values()]
        ),
        "n_cells_within_tolerance": int(
            sum(1 for d in per_cell.values() if d["sustained_within_tolerance"])
        ),
        "n_cells": len(cells),
        "any_failed_sustained_reach": bool(any(f.failed_sustained_reach for f in fits.values())),
        "transient_sensitivity": {
            f"{t:.2f}": {
                cid: {"s_na_fit": f.s_na_fit, "s_k_fit": f.s_k_fit, "loss": f.loss}
                for cid, f in d.items()
            }
            for t, d in fits_sens.items()
        },
    }
    with_arm_suffix(path=FITTED_SCALINGS_JSON, arm=arm).write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in summary.items() if k != "cells"}, indent=1)[:3000])
    for cid, d in per_cell.items():
        print(
            cid,
            f"s_na={d['s_na_fit']:.3f} s_k={d['s_k_fit']:.3f}",
            f"S={d['achieved_sustained_ratio']:.3f} T={d['achieved_transient_ratio']:.3f}",
        )


if __name__ == "__main__":
    main()
