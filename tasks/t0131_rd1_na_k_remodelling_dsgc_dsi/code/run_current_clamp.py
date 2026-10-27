"""Step 9: out-of-sample current clamp (+60 pA, 500 ms) and f-I curves, WT-like vs rd1-like."""

import argparse
import json
import time
from typing import Any

import pandas as pd

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_io import load_reference_cells
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    CC_AMPLITUDES_EXTENDED_PA,
    CC_AMPLITUDES_PA,
    CC_DELAY_MS,
    CC_DUR_MS,
    CC_SETTLE_MS,
    CC_TEST_AMP_PA,
    CC_TSTOP_MS,
    COLLAPSE_MAX_RD1_SPIKES,
    COLLAPSE_MIN_DIFFERENCE,
    MAX_WORKERS,
    V_INIT_CLAMP_MV,
    WT_MIN_SPIKES_INFORMATIVE,
    ScalingArm,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.current_clamp import (
    CcJob,
    run_current_clamp_job,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.fitted_io import load_fitted_scalings
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.parallel import run_jobs
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    CC_COLLAPSE_VERDICT_JSON,
    CC_STEP_SUMMARY_CSV,
    DATA_DIR,
    FI_CURVES_CSV,
    with_arm_suffix,
)

TRACE_AMPS_PA: list[float] = [0.0, 60.0, 200.0, 800.0]
COND_WT: str = "wt_like"
COND_RD1: str = "rd1_like"
TAIL_MS: float = CC_TSTOP_MS - CC_DELAY_MS - CC_DUR_MS


def collapse_verdict(*, wt_spikes: int, rd1_spikes: int) -> str:
    if wt_spikes < WT_MIN_SPIKES_INFORMATIVE:
        return "uninformative"
    if rd1_spikes <= COLLAPSE_MAX_RD1_SPIKES and wt_spikes - rd1_spikes >= COLLAPSE_MIN_DIFFERENCE:
        return "collapsed"
    return "not_collapsed"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--workers", type=int, default=MAX_WORKERS)
    ap.add_argument("--arm", type=str, default=str(ScalingArm.SOMA_AIS))
    ap.add_argument("--no-extended", action="store_true")
    args = ap.parse_args()
    arm: str = args.arm
    cells = load_reference_cells(limit=args.limit)
    fits = load_fitted_scalings(arm=arm)
    jobs: list[CcJob] = []
    for c in cells:
        for cond, sn, sk in (
            (COND_WT, 1.0, 1.0),
            (COND_RD1, fits[c.cell_id].s_na, fits[c.cell_id].s_k),
        ):
            for amp in CC_AMPLITUDES_PA + ([] if args.no_extended else CC_AMPLITUDES_EXTENDED_PA):
                jobs.append(
                    CcJob(
                        job_key=f"cc|{arm}|{c.cell_id}|{cond}|{amp:.0f}",
                        cell_id=c.cell_id,
                        vector_68d=c.vector_68d,
                        s_na=sn,
                        s_k=sk,
                        arm=arm,
                        amp_pa=amp,
                        delay_ms=CC_DELAY_MS,
                        dur_ms=CC_DUR_MS,
                        tail_ms=TAIL_MS,
                        settle_ms=CC_SETTLE_MS,
                        window_ms=CC_DUR_MS,
                        bias=None,
                        v_init_mv=V_INIT_CLAMP_MV,
                        save_trace=amp in TRACE_AMPS_PA,
                    )
                )
    t0 = time.time()
    rows = run_jobs(
        jobs=jobs,
        worker_fn=run_current_clamp_job,
        out_path=with_arm_suffix(path=DATA_DIR / "cc_rows.jsonl", arm=arm),
        key_of=lambda j: j.job_key,
        max_workers=args.workers,
        desc=f"current_clamp_{arm}",
    )
    print(f"cc wall time {time.time() - t0:.1f} s for {len(jobs)} runs", flush=True)
    recs: list[dict[str, Any]] = []
    for job in jobs:
        r = rows[job.job_key]
        cond = job.job_key.split("|")[3]
        recs.append(
            {
                "cell_id": job.cell_id,
                "arm": arm,
                "condition": cond,
                "s_na": job.s_na,
                "s_k": job.s_k,
                "amp_pa": job.amp_pa,
                "extended_amplitude": job.amp_pa in CC_AMPLITUDES_EXTENDED_PA,
                "n_spikes": r.get("n_spikes_window"),
                "rate_hz": r.get("rate_hz_window"),
                "first100_rate_hz": r.get("first100_rate_hz"),
                "last200_rate_hz": r.get("last200_rate_hz"),
                "adaptation_index": r.get("adaptation_index"),
                "spike_peak_mv": r.get("spike_peak_mv"),
                "spike_fwhm_ms": r.get("spike_fwhm_ms"),
                "rest_vm_mv": r.get("rest_vm_mv"),
                "v_max_mv": r.get("v_max_mv"),
                "error": r.get("error"),
            }
        )
    df = pd.DataFrame(recs)
    df.to_csv(with_arm_suffix(path=CC_STEP_SUMMARY_CSV, arm=arm), index=False)
    df[
        ["cell_id", "arm", "condition", "amp_pa", "extended_amplitude", "n_spikes", "rate_hz"]
    ].to_csv(with_arm_suffix(path=FI_CURVES_CSV, arm=arm), index=False)
    verdicts: dict[str, Any] = {}
    for c in cells:
        sub = df[(df.cell_id == c.cell_id) & (df.amp_pa == CC_TEST_AMP_PA)]
        wt = int(sub[sub.condition == COND_WT].n_spikes.iloc[0])
        rd = int(sub[sub.condition == COND_RD1].n_spikes.iloc[0])
        base = df[(df.cell_id == c.cell_id) & (df.amp_pa == 0.0)]
        verdicts[c.cell_id] = {
            "wt_spikes_60pa": wt,
            "rd1_spikes_60pa": rd,
            "verdict": collapse_verdict(wt_spikes=wt, rd1_spikes=rd),
            "wt_spikes_0pa": int(base[base.condition == COND_WT].n_spikes.iloc[0]),
            "rd1_spikes_0pa": int(base[base.condition == COND_RD1].n_spikes.iloc[0]),
        }
    n_collapsed = sum(1 for v in verdicts.values() if v["verdict"] == "collapsed")
    n_uninf = sum(1 for v in verdicts.values() if v["verdict"] == "uninformative")
    out = {
        "arm": arm,
        "per_cell": verdicts,
        "n_collapsed": n_collapsed,
        "n_uninformative": n_uninf,
        "n_cells": len(cells),
    }
    with_arm_suffix(path=CC_COLLAPSE_VERDICT_JSON, arm=arm).write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    pd.set_option("display.width", 220)
    print(
        df[df.amp_pa.isin([0.0, 60.0, 800.0])].pivot_table(
            index=["cell_id", "amp_pa"], columns="condition", values="n_spikes"
        )
    )
    print(json.dumps({k: v for k, v in out.items() if k != "per_cell"}))


if __name__ == "__main__":
    main()
