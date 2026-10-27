"""Step 10: spontaneous activity at rest and tonic-bias tuning (tuned on rd1-like cells only)."""

import argparse
import json
from typing import Any

import numpy as np
import pandas as pd

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.bias import BiasSpec
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_io import RefCell, load_reference_cells
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    BIAS_GRID_EXTENDED_PA,
    BIAS_GRID_PA,
    BIAS_MIN_ISI_CV,
    BIAS_TARGET_RATE_HZ,
    BIAS_TUNING_N_CELLS,
    MAX_WORKERS,
    NOISE_GRID_EXTENDED_PA,
    NOISE_GRID_PA,
    SPONT_DT_RUN_MS,
    SPONT_DUR_MS,
    SPONT_NOISE_SEEDS,
    SPONT_SETTLE_MS,
    TRIGGER_C_RATE_MAX_HZ,
    TRIGGER_C_RATE_MIN_HZ,
    TRIGGER_C_WT_MAX_HZ,
    V_INIT_MV,
    ScalingArm,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.current_clamp import (
    CcJob,
    run_current_clamp_job,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.fitted_io import (
    FittedScaling,
    load_fitted_scalings,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.parallel import run_jobs
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    BIAS_TUNING_CSV,
    CHOSEN_BIAS_JSON,
    DATA_DIR,
    SPONTANEOUS_SUMMARY_CSV,
    with_arm_suffix,
)

COND_WT: str = "wt_like"
COND_RD1: str = "rd1_like"
TRACE_CELLS: int = 2


def _job(
    *,
    cell: RefCell,
    cond: str,
    scaling: FittedScaling,
    arm: str,
    bias: BiasSpec | None,
    tag: str,
    save_trace: bool,
) -> CcJob:
    sn, sk = (1.0, 1.0) if cond == COND_WT else (scaling.s_na, scaling.s_k)
    b = (
        "none"
        if bias is None
        else f"{bias.i_bias_pa:.0f}_{bias.sigma_noise_pa:.0f}_{bias.noise_seed}"
    )
    return CcJob(
        job_key=f"spont|{arm}|{tag}|{cell.cell_id}|{cond}|{b}",
        cell_id=cell.cell_id,
        vector_68d=cell.vector_68d,
        s_na=sn,
        s_k=sk,
        arm=arm,
        amp_pa=0.0,
        delay_ms=0.0,
        dur_ms=0.0,
        tail_ms=SPONT_DUR_MS,
        settle_ms=SPONT_SETTLE_MS,
        window_ms=SPONT_DUR_MS,
        bias=bias,
        v_init_mv=V_INIT_MV,
        save_trace=save_trace,
        dt_ms=SPONT_DT_RUN_MS,
    )


def _row(*, job: CcJob, r: dict[str, Any], tag: str) -> dict[str, Any]:
    parts = job.job_key.split("|")
    return {
        "tag": tag,
        "cell_id": job.cell_id,
        "arm": job.arm,
        "condition": parts[4],
        "s_na": job.s_na,
        "s_k": job.s_k,
        "i_bias_pa": None if job.bias is None else job.bias.i_bias_pa,
        "sigma_noise_pa": None if job.bias is None else job.bias.sigma_noise_pa,
        "noise_seed": None if job.bias is None else job.bias.noise_seed,
        "n_spikes": r.get("n_spikes_window"),
        "rate_hz": r.get("rate_hz_window"),
        "isi_cv": r.get("isi_cv"),
        "spike_peak_mv": r.get("spike_peak_mv"),
        "rest_vm_mv": r.get("rest_vm_mv"),
        "v_max_mv": r.get("v_max_mv"),
        "v_min_mv": r.get("v_min_mv"),
        "error": r.get("error"),
    }


def _select_bias(*, tuning: pd.DataFrame) -> dict[str, Any]:
    """Pick the (bias, sigma) whose mean rd1-like rate is closest to 7 Hz with mean ISI CV > 0.5.

    Only rd1-like rows are used. Returns a dict with ``chosen`` (or None), ``criteria_met`` and
    the reason for any fallback.
    """
    rd = tuning[tuning.condition == COND_RD1]
    g = rd.groupby(["i_bias_pa", "sigma_noise_pa"]).agg(
        mean_rate=("rate_hz", "mean"), mean_cv=("isi_cv", "mean"), n=("rate_hz", "size")
    )
    g = g.reset_index()
    g["rate_dist"] = (g["mean_rate"] - BIAS_TARGET_RATE_HZ).abs()
    ok = g[(g["mean_cv"] > BIAS_MIN_ISI_CV) & (g["mean_rate"] > 0.0)]
    if len(ok) > 0:
        best = ok.sort_values("rate_dist").iloc[0]
        return {
            "criteria_met": True,
            "chosen": {
                "i_bias_pa": float(best["i_bias_pa"]),
                "sigma_noise_pa": float(best["sigma_noise_pa"]),
            },
            "mean_rd1_rate_hz": float(best["mean_rate"]),
            "mean_rd1_isi_cv": float(best["mean_cv"]),
            "reason": "closest mean rate to 7 Hz among combinations with mean ISI CV above 0.5",
        }
    best = g.sort_values(["rate_dist", "i_bias_pa"], ascending=[True, False]).iloc[0]
    return {
        "criteria_met": False,
        "chosen": {
            "i_bias_pa": float(best["i_bias_pa"]),
            "sigma_noise_pa": float(best["sigma_noise_pa"]),
        },
        "mean_rd1_rate_hz": float(best["mean_rate"]),
        "mean_rd1_isi_cv": None if pd.isna(best["mean_cv"]) else float(best["mean_cv"]),
        "reason": (
            "no combination gave rd1-like mean rate above 0 with ISI CV above 0.5; fell back to "
            "the combination with the mean rate closest to 7 Hz (ties: larger bias)"
        ),
    }


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
    jsonl = with_arm_suffix(path=DATA_DIR / "spont_rows.jsonl", arm=arm)

    def run(jobs: list[CcJob], desc: str) -> dict[str, dict[str, Any]]:
        return run_jobs(
            jobs=jobs,
            worker_fn=run_current_clamp_job,
            out_path=jsonl,
            key_of=lambda j: j.job_key,
            max_workers=args.workers,
            desc=desc,
        )

    # (a) no-bias at rest, both conditions, all cells.
    jobs_a: list[CcJob] = [
        _job(
            cell=c,
            cond=cond,
            scaling=fits[c.cell_id],
            arm=arm,
            bias=None,
            tag="nobias",
            save_trace=True,
        )
        for c in cells
        for cond in (COND_WT, COND_RD1)
    ]
    rows = run(jobs_a, "spont_nobias")
    recs: list[dict[str, Any]] = [_row(job=j, r=rows[j.job_key], tag="nobias") for j in jobs_a]

    # (b) tuning grid on the first 3 cells (rd1-like decides; WT-like logged for the curves).
    tune_cells = cells[:BIAS_TUNING_N_CELLS]
    seed0 = SPONT_NOISE_SEEDS[0]

    def tuning_jobs(*, biases: list[float], sigmas: list[float], tag: str) -> list[CcJob]:
        return [
            _job(
                cell=c,
                cond=cond,
                scaling=fits[c.cell_id],
                arm=arm,
                bias=BiasSpec(i_bias_pa=ib, sigma_noise_pa=sg, noise_seed=seed0),
                tag=tag,
                save_trace=False,
            )
            for c in tune_cells
            for cond in (COND_RD1, COND_WT)
            for ib in biases
            for sg in sigmas
        ]

    jobs_b = tuning_jobs(biases=BIAS_GRID_PA, sigmas=NOISE_GRID_PA, tag="tune_primary")
    rows = run(jobs_b, "spont_tune_primary")
    tune_recs = [_row(job=j, r=rows[j.job_key], tag="tune_primary") for j in jobs_b]
    sel = _select_bias(tuning=pd.DataFrame(tune_recs))
    stage = "primary"
    if not sel["criteria_met"] and not args.no_extended:
        jobs_x = tuning_jobs(
            biases=BIAS_GRID_EXTENDED_PA, sigmas=NOISE_GRID_EXTENDED_PA, tag="tune_extended"
        )
        rows = run(jobs_x, "spont_tune_extended")
        tune_recs += [_row(job=j, r=rows[j.job_key], tag="tune_extended") for j in jobs_x]
        sel_x = _select_bias(tuning=pd.DataFrame(tune_recs))
        if sel_x["criteria_met"]:
            sel = sel_x
            stage = "extended"
        else:
            sel = sel_x
            stage = "extended_fallback"
    tuning_df = pd.DataFrame(tune_recs)
    tuning_df.to_csv(with_arm_suffix(path=BIAS_TUNING_CSV, arm=arm), index=False)

    # (c) apply the chosen bias to all cells, both conditions, 3 noise seeds.
    ch = sel["chosen"]
    jobs_c: list[CcJob] = []
    for ci, c in enumerate(cells):
        for cond in (COND_WT, COND_RD1):
            for ns in SPONT_NOISE_SEEDS:
                jobs_c.append(
                    _job(
                        cell=c,
                        cond=cond,
                        scaling=fits[c.cell_id],
                        arm=arm,
                        bias=BiasSpec(
                            i_bias_pa=ch["i_bias_pa"],
                            sigma_noise_pa=ch["sigma_noise_pa"],
                            noise_seed=ns,
                        ),
                        tag="chosen",
                        save_trace=ci < TRACE_CELLS and ns == SPONT_NOISE_SEEDS[0],
                    )
                )
    rows = run(jobs_c, "spont_chosen")
    recs += [_row(job=j, r=rows[j.job_key], tag="chosen") for j in jobs_c]
    summary = pd.DataFrame(recs)
    summary.to_csv(with_arm_suffix(path=SPONTANEOUS_SUMMARY_CSV, arm=arm), index=False)

    chosen_df = summary[summary.tag == "chosen"]
    per_cond: dict[str, Any] = {}
    for cond in (COND_WT, COND_RD1):
        sub = chosen_df[chosen_df.condition == cond]
        per_cond[cond] = {
            "mean_rate_hz": float(sub.rate_hz.mean()),
            "median_rate_hz": float(sub.rate_hz.median()),
            "mean_isi_cv": None if sub.isi_cv.isna().all() else float(sub.isi_cv.mean()),
            "n_runs": int(len(sub)),
        }
    nobias = summary[summary.tag == "nobias"]
    per_cond_nobias = {
        cond: {
            "mean_rate_hz": float(nobias[nobias.condition == cond].rate_hz.mean()),
            "median_rate_hz": float(nobias[nobias.condition == cond].rate_hz.median()),
            "mean_rest_vm_mv": float(nobias[nobias.condition == cond].rest_vm_mv.mean()),
        }
        for cond in (COND_WT, COND_RD1)
    }
    rd1_mean = per_cond[COND_RD1]["mean_rate_hz"]
    wt_mean = per_cond[COND_WT]["mean_rate_hz"]
    rd1_cv = per_cond[COND_RD1]["mean_isi_cv"]
    trigger_c_ok = bool(
        TRIGGER_C_RATE_MIN_HZ <= rd1_mean <= TRIGGER_C_RATE_MAX_HZ
        and rd1_cv is not None
        and rd1_cv > BIAS_MIN_ISI_CV
        and wt_mean < TRIGGER_C_WT_MAX_HZ
    )
    out = {
        "arm": arm,
        "tuning_stage_used": stage,
        "selection": sel,
        "noise_seed_tuning": seed0,
        "noise_seeds_applied": SPONT_NOISE_SEEDS,
        "tuning_cells": [c.cell_id for c in tune_cells],
        "tuning_rule": (
            "rd1-like only; closest mean rate to 7 Hz among combinations with mean ISI CV > 0.5; "
            "then the SAME bias and noise are applied to WT-like cells"
        ),
        "bias_form": (
            "DC IClamp at soma(0.5) of i_bias_pa for the whole run plus Gaussian white-noise "
            "IClamp (sigma_noise_pa, Vector.play at dt 0.1 ms, fixed seed per run)"
        ),
        "applied_all_cells": per_cond,
        "no_bias": per_cond_nobias,
        "trigger_c_satisfied": trigger_c_ok,
    }
    with_arm_suffix(path=CHOSEN_BIAS_JSON, arm=arm).write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(json.dumps(out, indent=1))
    _ = np


if __name__ == "__main__":
    main()
