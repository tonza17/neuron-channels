"""Step 11: signed antipodal DSI (8 directions, 1400 ms), four conditions, and the heatmap."""

import argparse
import json
import time
from dataclasses import asdict
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.bias import BiasSpec
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_factory import (
    build_scaled,
    dispose_all_cells,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_io import RefCell, load_reference_cells
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    DSI_GATE_MIN_DSI,
    DSI_GATE_PD_TOLERANCE,
    DSI_N_BOOTSTRAP,
    HEATMAP_DIRECTIONS_DEG,
    HEATMAP_N_SEEDS,
    MAX_WORKERS,
    N_DIRECTIONS_FULL,
    N_HEATMAP_CELLS,
    RNG_SEED,
    S_K_GRID,
    S_NA_GRID,
    TSTOP_MS,
    WILCOXON_ALPHA,
    Condition,
    ScalingArm,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.dsi_rules import (
    ConditionSummary,
    TrialCount,
    summarise_counts,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.evaluator import (
    MODE_BAR,
    TrialJob,
    eval_seeds,
    run_trial_job,
    trial_seed,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.fitted_io import (
    load_fitted_scalings,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.parallel import run_jobs
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    CELL_PARAMS_JSONL,
    CHOSEN_BIAS_JSON,
    DATA_DIR,
    DSI_HEATMAP_CSV,
    DSI_RESULTS_CSV,
    DSI_STATS_JSON,
    DSI_TRIALS_JSONL,
    with_arm_suffix,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.scaling import (
    ChannelScales,
    snapshot_gbars,
)

CONDITIONS: list[Condition] = [
    Condition.WT_LIKE,
    Condition.RD1_LIKE,
    Condition.WT_LIKE_BIAS,
    Condition.RD1_LIKE_BIAS,
]


def trial_worker(job: TrialJob) -> dict[str, Any]:
    out = asdict(run_trial_job(job))
    out["cell_id"] = job.cell_id
    out["direction_deg"] = job.direction_deg
    out["seed_index"] = job.seed_index
    out["s_na"] = job.s_na
    out["s_k"] = job.s_k
    out["arm"] = job.arm
    return out


def load_chosen_bias(*, arm: str) -> BiasSpec | None:
    path = with_arm_suffix(path=CHOSEN_BIAS_JSON, arm=arm)
    if not path.exists():
        return None
    d = json.loads(path.read_text(encoding="utf-8"))
    ch = d["selection"]["chosen"]
    return BiasSpec(
        i_bias_pa=float(ch["i_bias_pa"]),
        sigma_noise_pa=float(ch["sigma_noise_pa"]),
        noise_seed=0,
    )


def _job(
    *,
    tag: str,
    cell: RefCell,
    cond_name: str,
    s_na: float,
    s_k: float,
    arm: str,
    bias: BiasSpec | None,
    direction_deg: float,
    seed_index: int,
    base_seed: int,
) -> TrialJob:
    seed = trial_seed(base_seed=base_seed, direction_deg=direction_deg)
    b: BiasSpec | None = None
    if bias is not None:
        b = BiasSpec(i_bias_pa=bias.i_bias_pa, sigma_noise_pa=bias.sigma_noise_pa, noise_seed=seed)
    return TrialJob(
        job_key=f"{tag}|{arm}|{cell.cell_id}|{cond_name}|{direction_deg:.0f}|{seed_index}",
        cell_id=cell.cell_id,
        vector_68d=cell.vector_68d,
        s_na=s_na,
        s_k=s_k,
        arm=arm,
        bias=b,
        mode=MODE_BAR,
        direction_deg=direction_deg,
        seed_index=seed_index,
        seed=seed,
        exc_scale=1.0,
        tstop_ms=TSTOP_MS,
    )


def _counts_for(*, rows: dict[str, dict[str, Any]], keys: list[str]) -> list[TrialCount]:
    out: list[TrialCount] = []
    for k in keys:
        r = rows[k]
        out.append(
            TrialCount(
                direction_deg=float(r["direction_deg"]),
                seed_index=int(r["seed_index"]),
                spike_count=int(r["spike_count"]),
                peak_mv=r["peak_mv"],
                error=r["error"],
            )
        )
    return out


def _paired_stats(*, a: list[float | None], b: list[float | None], label: str) -> dict[str, Any]:
    """Paired difference b - a with undefined pairs dropped; Wilcoxon and bootstrap CI."""
    pairs = [(x, y) for x, y in zip(a, b, strict=True) if x is not None and y is not None]
    n_dropped = len(a) - len(pairs)
    out: dict[str, Any] = {"label": label, "n_pairs": len(pairs), "n_dropped_undefined": n_dropped}
    if len(pairs) < 2:
        out.update({"median_diff": None, "wilcoxon_p": None, "ci95": None})
        return out
    diffs = np.array([y - x for x, y in pairs], dtype=np.float64)
    out["median_diff"] = float(np.median(diffs))
    out["mean_diff"] = float(np.mean(diffs))
    try:
        res = wilcoxon(diffs, alternative="two-sided")
        out["wilcoxon_p"] = float(res.pvalue)
        out["significant_alpha_0.05"] = bool(res.pvalue < WILCOXON_ALPHA)
    except ValueError:
        out["wilcoxon_p"] = None
    rng = np.random.default_rng(RNG_SEED)
    boots = np.array(
        [
            np.median(rng.choice(diffs, size=len(diffs), replace=True))
            for _ in range(DSI_N_BOOTSTRAP)
        ]
    )
    out["ci95"] = [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]
    return out


def run_main(*, args: argparse.Namespace) -> None:
    arm: str = args.arm
    cells = load_reference_cells(limit=args.limit)
    fits = load_fitted_scalings(arm=arm)
    bias = load_chosen_bias(arm=arm)
    seeds = eval_seeds()[: args.seeds]
    angles = [float(d) * (360.0 / N_DIRECTIONS_FULL) for d in range(N_DIRECTIONS_FULL)]
    conds: list[Condition] = CONDITIONS if bias is not None else CONDITIONS[:2]
    if args.gate:
        conds = [Condition.WT_LIKE]
    jobs: list[TrialJob] = []
    meta: dict[str, dict[str, Any]] = {}
    for c in cells:
        for cond in conds:
            is_rd1 = cond in (Condition.RD1_LIKE, Condition.RD1_LIKE_BIAS)
            with_bias = cond in (Condition.WT_LIKE_BIAS, Condition.RD1_LIKE_BIAS)
            sn = fits[c.cell_id].s_na if is_rd1 else 1.0
            sk = fits[c.cell_id].s_k if is_rd1 else 1.0
            meta[f"{c.cell_id}|{cond.value}"] = {
                "s_na": sn,
                "s_k": sk,
                "bias": bias if with_bias else None,
            }
            for si, base in enumerate(seeds):
                for d in angles:
                    jobs.append(
                        _job(
                            tag="dsi",
                            cell=c,
                            cond_name=cond.value,
                            s_na=sn,
                            s_k=sk,
                            arm=arm,
                            bias=bias if with_bias else None,
                            direction_deg=d,
                            seed_index=si,
                            base_seed=base,
                        )
                    )
    t0 = time.time()
    out_jsonl = with_arm_suffix(path=DSI_TRIALS_JSONL, arm=arm)
    if args.gate:
        out_jsonl = DATA_DIR / "dsi_gate_trials.jsonl"
    rows = run_jobs(
        jobs=jobs,
        worker_fn=trial_worker,
        out_path=out_jsonl,
        key_of=lambda j: j.job_key,
        max_workers=args.workers,
        desc=f"dsi_{arm}",
    )
    print(f"DSI wall time {time.time() - t0:.1f} s for {len(jobs)} trials", flush=True)
    results: list[dict[str, Any]] = []
    for c in cells:
        for cond in conds:
            keys = [
                j.job_key for j in jobs if j.cell_id == c.cell_id and f"|{cond.value}|" in j.job_key
            ]
            summ: ConditionSummary = summarise_counts(trials=_counts_for(rows=rows, keys=keys))
            m = meta[f"{c.cell_id}|{cond.value}"]
            b: BiasSpec | None = m["bias"]
            row: dict[str, Any] = {
                "cell_id": c.cell_id,
                "seed_label": c.seed_label,
                "arm": arm,
                "condition": cond.value,
                "s_na": m["s_na"],
                "s_k": m["s_k"],
                "i_bias_pa": None if b is None else b.i_bias_pa,
                "sigma_noise_pa": None if b is None else b.sigma_noise_pa,
                "n_seeds": len(seeds),
                "pd_spikes": summ.pd_spikes,
                "nd_spikes": summ.nd_spikes,
                "pd_rate_hz": summ.pd_rate_hz,
                "nd_rate_hz": summ.nd_rate_hz,
                "dsi_signed": summ.dsi_signed,
                "dsi_unguarded": summ.dsi_unguarded,
                "low_count": summ.low_count,
                "n_undefined": 1 if summ.dsi_signed is None else 0,
                "n_trials": summ.n_trials,
                "n_errors": summ.n_errors,
                "recorded_pd_rate_hz": c.pd_rate_hz,
            }
            for dname, v in summ.mean_counts_per_direction.items():
                row[f"mean_spikes_dir_{dname}"] = v
            results.append(row)
    df = pd.DataFrame(results)
    if args.gate:
        pd.set_option("display.width", 220)
        print(df.T)
        r0 = results[0]
        pd_ok = abs(r0["pd_rate_hz"] - r0["recorded_pd_rate_hz"]) <= (
            DSI_GATE_PD_TOLERANCE * r0["recorded_pd_rate_hz"]
        )
        dsi_ok = r0["dsi_unguarded"] is not None and r0["dsi_unguarded"] > DSI_GATE_MIN_DSI
        print("GATE pd_ok", pd_ok, "dsi_ok", dsi_ok)
        return
    df.to_csv(with_arm_suffix(path=DSI_RESULTS_CSV, arm=arm), index=False)

    # Per-cell parameter dump (t0129-compatible keys plus condition, scales, raw counts).
    with with_arm_suffix(path=CELL_PARAMS_JSONL, arm=arm).open("w", encoding="utf-8") as f:
        for r in results:
            cell = next(x for x in cells if x.cell_id == r["cell_id"])
            dispose_all_cells()
            built = build_scaled(
                vector_68d=cell.vector_68d,
                scales=ChannelScales(s_na=r["s_na"], s_k=r["s_k"], arm=ScalingArm(arm)),
                with_synapses=False,
            )
            dump = {
                "gen": -1,
                "cell_idx": 0,
                "cell_id": r["cell_id"],
                "condition": r["condition"],
                "arm": arm,
                "s_na": r["s_na"],
                "s_k": r["s_k"],
                "param_vector": cell.vector_68d,
                "dsi_signed": r["dsi_signed"],
                "pd_rate_hz": r["pd_rate_hz"],
                "nd_rate_hz": r["nd_rate_hz"],
                "pd_spikes": r["pd_spikes"],
                "nd_spikes": r["nd_spikes"],
                "low_count": r["low_count"],
                "silence_failed": r["low_count"],
                "n_errors": r["n_errors"],
                "scaled_gbar_totals": snapshot_gbars(cell=built.cell),
            }
            f.write(json.dumps(dump) + "\n")

    # Statistics: paired rd1 - wt, without and with bias.
    stats: dict[str, Any] = {"arm": arm, "n_cells": len(cells)}
    piv = {
        cond.value: df[df.condition == cond.value]
        .set_index("cell_id")
        .loc[[c.cell_id for c in cells]]
        for cond in conds
    }

    def col(name: str, cond: Condition, field: str) -> list[float | None]:
        _ = name
        return [None if pd.isna(v) else float(v) for v in piv[cond.value][field]]

    for field in ("dsi_signed", "pd_rate_hz", "nd_rate_hz"):
        stats[f"rd1_minus_wt_{field}"] = _paired_stats(
            a=col("a", Condition.WT_LIKE, field),
            b=col("b", Condition.RD1_LIKE, field),
            label=f"rd1_like - wt_like ({field})",
        )
        if bias is not None:
            stats[f"rd1_bias_minus_wt_bias_{field}"] = _paired_stats(
                a=col("a", Condition.WT_LIKE_BIAS, field),
                b=col("b", Condition.RD1_LIKE_BIAS, field),
                label=f"rd1_like_with_bias - wt_like_with_bias ({field})",
            )
    per_cond: dict[str, Any] = {}
    for cond in conds:
        sub = df[df.condition == cond.value]
        defined = sub.dsi_signed.dropna()
        per_cond[cond.value] = {
            "median_dsi_signed": None if len(defined) == 0 else float(defined.median()),
            "mean_dsi_signed": None if len(defined) == 0 else float(defined.mean()),
            "n_defined": int(len(defined)),
            "n_undefined": int(len(sub) - len(defined)),
            "median_pd_rate_hz": float(sub.pd_rate_hz.median()),
            "median_nd_rate_hz": float(sub.nd_rate_hz.median()),
            "total_pd_spikes": int(sub.pd_spikes.sum()),
            "total_nd_spikes": int(sub.nd_spikes.sum()),
        }
    stats["per_condition"] = per_cond
    with_arm_suffix(path=DSI_STATS_JSON, arm=arm).write_text(
        json.dumps(stats, indent=2), encoding="utf-8"
    )
    pd.set_option("display.width", 250)
    print(
        df[
            [
                "cell_id",
                "condition",
                "pd_spikes",
                "nd_spikes",
                "pd_rate_hz",
                "nd_rate_hz",
                "dsi_signed",
                "low_count",
            ]
        ]
    )
    print(json.dumps(per_cond, indent=1))


def run_heatmap(*, args: argparse.Namespace) -> None:
    arm: str = args.arm
    cells = load_reference_cells(limit=N_HEATMAP_CELLS if args.limit is None else args.limit)
    seeds = eval_seeds()[:HEATMAP_N_SEEDS]
    jobs: list[TrialJob] = []
    for c in cells:
        for sn in S_NA_GRID:
            for sk in S_K_GRID:
                for si, base in enumerate(seeds):
                    for d in HEATMAP_DIRECTIONS_DEG:
                        jobs.append(
                            _job(
                                tag="heat",
                                cell=c,
                                cond_name=f"{sn:.2f}_{sk:.2f}",
                                s_na=sn,
                                s_k=sk,
                                arm=arm,
                                bias=None,
                                direction_deg=d,
                                seed_index=si,
                                base_seed=base,
                            )
                        )
    rows = run_jobs(
        jobs=jobs,
        worker_fn=trial_worker,
        out_path=with_arm_suffix(path=DATA_DIR / "dsi_heatmap_trials.jsonl", arm=arm),
        key_of=lambda j: j.job_key,
        max_workers=args.workers,
        desc=f"heatmap_{arm}",
    )
    recs: list[dict[str, Any]] = []
    for c in cells:
        for sn in S_NA_GRID:
            for sk in S_K_GRID:
                keys = [
                    j.job_key
                    for j in jobs
                    if j.cell_id == c.cell_id and f"|{sn:.2f}_{sk:.2f}|" in j.job_key
                ]
                summ = summarise_counts(trials=_counts_for(rows=rows, keys=keys))
                recs.append(
                    {
                        "cell_id": c.cell_id,
                        "arm": arm,
                        "s_na": sn,
                        "s_k": sk,
                        "pd_spikes": summ.pd_spikes,
                        "nd_spikes": summ.nd_spikes,
                        "pd_rate_hz": summ.pd_rate_hz,
                        "nd_rate_hz": summ.nd_rate_hz,
                        "dsi_signed": summ.dsi_signed,
                        "dsi_unguarded": summ.dsi_unguarded,
                        "low_count": summ.low_count,
                        "n_errors": summ.n_errors,
                    }
                )
    pd.DataFrame(recs).to_csv(with_arm_suffix(path=DSI_HEATMAP_CSV, arm=arm), index=False)
    print("heatmap rows", len(recs))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["main", "heatmap"], default="main")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--workers", type=int, default=MAX_WORKERS)
    ap.add_argument("--arm", type=str, default=str(ScalingArm.SOMA_AIS))
    args = ap.parse_args()
    if args.mode == "main":
        run_main(args=args)
    else:
        run_heatmap(args=args)


if __name__ == "__main__":
    main()
