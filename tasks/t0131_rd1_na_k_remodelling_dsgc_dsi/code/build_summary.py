"""Collect every number the results step will quote into results/data_summary.json."""

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import ScalingArm
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    ARM_DECISION_JSON,
    BIAS_TUNING_CSV,
    CC_COLLAPSE_VERDICT_JSON,
    CC_STEP_SUMMARY_CSV,
    CHOSEN_BIAS_JSON,
    CLAMP_BASELINE_CSV,
    CLAMP_SENSITIVITY_CSV,
    DATA_DIR,
    DATA_SUMMARY_JSON,
    DSI_HEATMAP_CSV,
    DSI_RESULTS_CSV,
    DSI_STATS_JSON,
    FITTED_SCALINGS_JSON,
    PANEL_D_PULSES_CSV,
    PANEL_D_SWEEP_CSV,
    PANEL_D_VERDICTS_JSON,
    REFERENCE_CELLS_JSONL,
    SPONTANEOUS_SUMMARY_CSV,
    TOY_ANCHOR_CHECK_JSON,
    TOY_PARAMS_JSON,
    with_arm_suffix,
)


def _read_json(*, path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def _clean(*, obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): _clean(obj=v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean(obj=v) for v in obj]
    if isinstance(obj, float) and not np.isfinite(obj):
        return None
    if isinstance(obj, np.floating):
        return None if not np.isfinite(float(obj)) else float(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def _cc_block(*, arm: str) -> dict[str, Any] | None:
    path = with_arm_suffix(path=CC_STEP_SUMMARY_CSV, arm=arm)
    if not path.exists():
        return None
    df = pd.read_csv(path)
    out: dict[str, Any] = {}
    for cond in ("wt_like", "rd1_like"):
        sub = df[df.condition == cond]
        by_amp: dict[str, Any] = {}
        for amp, g in sub.groupby("amp_pa"):
            by_amp[f"{amp:.0f}"] = {
                "mean_spikes": float(g.n_spikes.mean()),
                "median_spikes": float(g.n_spikes.median()),
                "mean_rate_hz": float(g.rate_hz.mean()),
                "n_cells_firing": int((g.n_spikes > 0).sum()),
                "mean_spike_peak_mv": None
                if g.spike_peak_mv.isna().all()
                else float(g.spike_peak_mv.mean()),
                "mean_spike_fwhm_ms": None
                if g.spike_fwhm_ms.isna().all()
                else float(g.spike_fwhm_ms.mean()),
                "mean_adaptation_index": None
                if g.adaptation_index.isna().all()
                else float(g.adaptation_index.mean()),
                "mean_rest_vm_mv": None
                if g.rest_vm_mv.isna().all()
                else float(g.rest_vm_mv.mean()),
                "mean_v_max_mv": None if g.v_max_mv.isna().all() else float(g.v_max_mv.mean()),
                "per_cell_spikes": {r.cell_id: int(r.n_spikes) for r in g.itertuples()},
            }
        out[cond] = by_amp
    return out


def main() -> None:
    summary: dict[str, Any] = {}
    cells = [json.loads(line) for line in REFERENCE_CELLS_JSONL.read_text("utf-8").splitlines()]
    summary["reference_cells"] = [
        {
            "cell_id": c["cell_id"],
            "stratum": c["seed_label"],
            "recorded_dsi_vector_sum": c["dsi_vector_sum"],
            "recorded_pd_rate_hz": c["pd_rate_hz"],
        }
        for c in cells
    ]
    screen_path = DATA_DIR / "reference_cell_screen.csv"
    if screen_path.exists():
        sc = pd.read_csv(screen_path)
        summary["reference_cell_screen"] = {
            "n_screened": int(len(sc)),
            "n_passed": int(sc.passed_screen.sum()),
            "n_rejected": int((~sc.passed_screen).sum()),
            "rejected": [
                {
                    "cell_id": r.cell_id,
                    "pd_spikes": int(r.pd_spikes),
                    "nd_spikes": int(r.nd_spikes),
                    "recorded_pd_rate_hz": float(r.recorded_pd_rate_hz),
                    "pd_rate_ok": bool(r.pd_rate_ok),
                    "dsi_ok": bool(r.dsi_ok),
                }
                for r in sc[~sc.passed_screen].itertuples()
            ],
        }
    if CLAMP_BASELINE_CSV.exists():
        cb = pd.read_csv(CLAMP_BASELINE_CSV)
        summary["clamp_baseline_wt_like"] = {
            "n_cells": int(len(cb)),
            "sustained_na_median": float(cb.sustained_na.median()),
            "sustained_na_min": float(cb.sustained_na.min()),
            "sustained_na_max": float(cb.sustained_na.max()),
            "na_transient_na_median": float(cb.na_transient_na.median()),
            "na_transient_na_min": float(cb.na_transient_na.min()),
            "na_transient_na_max": float(cb.na_transient_na.max()),
            "total_early_min_na_median": float(cb.total_early_min_na.median()),
            "hold_current_na_median": float(cb.baseline_na.median()),
            "all_na_transient_inward_and_above_0.2nA": bool(cb.na_transient_ok.all()),
            "all_sustained_positive": bool(cb.sustained_positive.all()),
            "researcher_panel_c_wt_sustained_na": 2.0,
        }
    if CLAMP_SENSITIVITY_CSV.exists():
        cs = pd.read_csv(CLAMP_SENSITIVITY_CSV)
        summary["clamp_sensitivity_abs_step_40mv"] = [
            {
                "cell_id": r.cell_id,
                "sustained_na": float(r.sustained_na),
                "na_transient_na": float(r.na_transient_na),
            }
            for r in cs.itertuples()
        ]
    for arm in (str(ScalingArm.SOMA_AIS), str(ScalingArm.SOMA_AIS_DENDRITE)):
        key = "base_arm" if arm == str(ScalingArm.SOMA_AIS) else "dendritic_arm"
        block: dict[str, Any] = {}
        block["fitted_scalings"] = _read_json(
            path=with_arm_suffix(path=FITTED_SCALINGS_JSON, arm=arm)
        )
        block["current_clamp"] = _cc_block(arm=arm)
        block["collapse_verdicts"] = _read_json(
            path=with_arm_suffix(path=CC_COLLAPSE_VERDICT_JSON, arm=arm)
        )
        block["chosen_bias"] = _read_json(path=with_arm_suffix(path=CHOSEN_BIAS_JSON, arm=arm))
        sp = with_arm_suffix(path=SPONTANEOUS_SUMMARY_CSV, arm=arm)
        if sp.exists():
            sdf = pd.read_csv(sp)
            per_cell_rates: dict[str, dict[str, list[float]]] = {}
            for (tag, cond), g in sdf[sdf.tag.isin(["nobias", "chosen"])].groupby(
                ["tag", "condition"]
            ):
                per_cell_rates[f"{tag}|{cond}"] = {
                    str(cid): [float(x) for x in gg.rate_hz] for cid, gg in g.groupby("cell_id")
                }
            block["spontaneous_rates_per_cell"] = per_cell_rates
            rows = sdf[sdf.tag.isin(["nobias", "chosen"])]
            block["spontaneous_by_tag_condition"] = {
                f"{tag}|{cond}": {
                    "mean_rate_hz": float(g.rate_hz.mean()),
                    "median_rate_hz": float(g.rate_hz.median()),
                    "min_rate_hz": float(g.rate_hz.min()),
                    "max_rate_hz": float(g.rate_hz.max()),
                    "mean_isi_cv": None if g.isi_cv.isna().all() else float(g.isi_cv.mean()),
                    "mean_rest_vm_mv": None
                    if g.rest_vm_mv.isna().all()
                    else float(g.rest_vm_mv.mean()),
                    "mean_spike_peak_mv": None
                    if g.spike_peak_mv.isna().all()
                    else float(g.spike_peak_mv.mean()),
                    "mean_v_max_mv": float(g.v_max_mv.mean()),
                    "n_runs": int(len(g)),
                }
                for (tag, cond), g in rows.groupby(["tag", "condition"])
            }
        bt = with_arm_suffix(path=BIAS_TUNING_CSV, arm=arm)
        if bt.exists():
            tdf = pd.read_csv(bt)
            block["bias_tuning_overview"] = {
                "n_rows": int(len(tdf)),
                "rd1_max_mean_rate_hz_over_grid": float(
                    tdf[tdf.condition == "rd1_like"]
                    .groupby(["i_bias_pa", "sigma_noise_pa"])
                    .rate_hz.mean()
                    .max()
                ),
                "wt_min_mean_rate_hz_over_grid": float(
                    tdf[tdf.condition == "wt_like"]
                    .groupby(["i_bias_pa", "sigma_noise_pa"])
                    .rate_hz.mean()
                    .min()
                ),
                "tags": sorted(set(tdf.tag)),
            }
        dr = with_arm_suffix(path=DSI_RESULTS_CSV, arm=arm)
        if dr.exists():
            ddf = pd.read_csv(dr)
            block["dsi_per_cell"] = _clean(
                obj=ddf[
                    [
                        "cell_id",
                        "condition",
                        "pd_spikes",
                        "nd_spikes",
                        "pd_rate_hz",
                        "nd_rate_hz",
                        "dsi_signed",
                        "dsi_unguarded",
                        "low_count",
                    ]
                ].to_dict(orient="records")
            )
        block["dsi_stats"] = _read_json(path=with_arm_suffix(path=DSI_STATS_JSON, arm=arm))
        hm = with_arm_suffix(path=DSI_HEATMAP_CSV, arm=arm)
        if hm.exists():
            hdf = pd.read_csv(hm)
            md = hdf.groupby(["s_na", "s_k"]).dsi_signed.median()
            mp = hdf.groupby(["s_na", "s_k"]).pd_rate_hz.median()
            nd = hdf.groupby(["s_na", "s_k"]).dsi_signed.count()
            block["dsi_heatmap"] = {
                "n_grid_points": int(len(md)),
                "n_cells": int(hdf.cell_id.nunique()),
                "median_dsi_at_1_1": float(md.loc[(1.0, 1.0)]) if (1.0, 1.0) in md.index else None,
                "median_dsi_min": None if md.isna().all() else float(md.min()),
                "median_dsi_max": None if md.isna().all() else float(md.max()),
                "median_pd_rate_min_hz": float(mp.min()),
                "median_pd_rate_max_hz": float(mp.max()),
                "n_defined_dsi_by_grid_point_min": int(nd.min()),
                "n_defined_dsi_by_grid_point_max": int(nd.max()),
                "grid_points_with_zero_defined_dsi": int((nd == 0).sum()),
            }
        summary[key] = block
    summary["arm_decision"] = _read_json(path=ARM_DECISION_JSON)
    summary["toy_params"] = _read_json(path=TOY_PARAMS_JSON)
    summary["toy_anchor_check"] = _read_json(path=TOY_ANCHOR_CHECK_JSON)
    summary["panel_d_verdicts"] = _read_json(path=PANEL_D_VERDICTS_JSON)
    if PANEL_D_SWEEP_CSV.exists():
        sw = pd.read_csv(PANEL_D_SWEEP_CSV)
        summary["panel_d_sweep_mean_rate_hz"] = {
            cond: {f"{u:.0f}": float(g.rate_hz.mean()) for u, g in sub.groupby("u")}
            for cond, sub in sw.groupby("condition")
        }
    if PANEL_D_PULSES_CSV.exists():
        pu = pd.read_csv(PANEL_D_PULSES_CSV)
        summary["panel_d_pulses_per_cell"] = _clean(obj=pu.to_dict(orient="records"))
    DATA_SUMMARY_JSON.write_text(json.dumps(_clean(obj=summary), indent=2), encoding="utf-8")
    print("wrote", DATA_SUMMARY_JSON)


if __name__ == "__main__":
    main()
