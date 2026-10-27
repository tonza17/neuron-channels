"""Step 14: test the panel D predictions in the NEURON model (strength sweep, three pulses)."""

import argparse
import json
import time
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.bias import BiasSpec
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_io import RefCell, load_reference_cells
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    BASELINE_PRED_RD1,
    MAX_WORKERS,
    N_PANEL_D_CELLS,
    PD_DIRECTION_DEG,
    PD_N_SEEDS,
    PD_STRENGTHS,
    PSTH_BIN_MS,
    PSTH_SMOOTH_SIGMA_MS,
    PULSE_N_REPS,
    PULSE_TSTOP_MS,
    SAT_PRED_RD1_MIN,
    SAT_PRED_WT_MAX,
    SEED_BASE,
    STRATUM_DRAW_ORDER,
    TSTOP_MS,
    ScalingArm,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.evaluator import (
    MODE_BAR,
    MODE_PULSE,
    TrialJob,
    eval_seeds,
    trial_seed,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.fitted_io import (
    FittedScaling,
    load_fitted_scalings,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.panel_d_metrics import (
    PulseMetrics,
    gaussian_smooth,
    pulse_metrics,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.parallel import load_done_rows, run_jobs
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    CHOSEN_BIAS_JSON,
    DSI_TRIALS_JSONL,
    PANEL_D_PSTH_NPZ,
    PANEL_D_PULSE_TRIALS_JSONL,
    PANEL_D_PULSES_CSV,
    PANEL_D_SWEEP_CSV,
    PANEL_D_SWEEP_TRIALS_JSONL,
    PANEL_D_VERDICTS_JSON,
    TOY_PARAMS_JSON,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.run_dsi import trial_worker

CONDS: list[str] = ["wt_like", "rd1_like", "wt_like_with_bias", "rd1_like_with_bias"]
GATE_TOLERANCE: float = 0.10
PULSE_BASE_SEED: int = SEED_BASE + 9000
PULSE_SEED_STRIDE: int = 17


@dataclass(frozen=True, slots=True)
class CondSpec:
    s_na: float
    s_k: float
    bias: BiasSpec | None


def pick_cells(*, limit: int | None) -> list[RefCell]:
    all_cells = load_reference_cells()
    chosen: list[RefCell] = []
    for stratum in STRATUM_DRAW_ORDER[:N_PANEL_D_CELLS]:
        for c in all_cells:
            if c.seed_label == stratum:
                chosen.append(c)
                break
    return chosen if limit is None else chosen[:limit]


def load_bias() -> BiasSpec | None:
    if not CHOSEN_BIAS_JSON.exists():
        return None
    d = json.loads(CHOSEN_BIAS_JSON.read_text(encoding="utf-8"))
    ch = d["selection"]["chosen"]
    return BiasSpec(
        i_bias_pa=float(ch["i_bias_pa"]), sigma_noise_pa=float(ch["sigma_noise_pa"]), noise_seed=0
    )


def cond_spec(*, cond: str, fit: FittedScaling, bias: BiasSpec | None) -> CondSpec:
    is_rd1 = cond.startswith("rd1")
    with_bias = cond.endswith("bias")
    return CondSpec(
        s_na=fit.s_na if is_rd1 else 1.0,
        s_k=fit.s_k if is_rd1 else 1.0,
        bias=bias if with_bias else None,
    )


def _make_job(
    *,
    key: str,
    cell: RefCell,
    spec: CondSpec,
    mode: str,
    direction_deg: float,
    exc_scale: float,
    seed_index: int,
    seed: int,
    tstop_ms: float,
) -> TrialJob:
    b: BiasSpec | None = None
    if spec.bias is not None:
        b = BiasSpec(
            i_bias_pa=spec.bias.i_bias_pa, sigma_noise_pa=spec.bias.sigma_noise_pa, noise_seed=seed
        )
    return TrialJob(
        job_key=key,
        cell_id=cell.cell_id,
        vector_68d=cell.vector_68d,
        s_na=spec.s_na,
        s_k=spec.s_k,
        arm=str(ScalingArm.SOMA_AIS),
        bias=b,
        mode=mode,
        direction_deg=direction_deg,
        seed_index=seed_index,
        seed=seed,
        exc_scale=exc_scale,
        tstop_ms=tstop_ms,
    )


def median_or_none(*, values: list[float | None]) -> float | None:
    vals = [v for v in values if v is not None]
    return float(np.median(vals)) if len(vals) > 0 else None


def _le(*, value: float | None, limit: float) -> bool:
    return value is not None and value <= limit


def _gt(*, value: float | None, limit: float) -> bool:
    return value is not None and value > limit


def _baseline_elevated(*, m_rd: PulseMetrics, m_wt: PulseMetrics) -> bool:
    if m_rd.baseline_rel is None or m_wt.baseline_rel is None:
        return False
    return m_rd.baseline_rel > m_wt.baseline_rel + 0.5 * BASELINE_PRED_RD1


def verdict_from_flags(*, direction_ok: bool, magnitude_ok: bool, some_cells_ok: bool) -> str:
    if direction_ok and magnitude_ok:
        return "reproduced"
    if direction_ok or some_cells_ok:
        return "partly reproduced"
    return "disproved"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--workers", type=int, default=MAX_WORKERS)
    args = ap.parse_args()
    cells = pick_cells(limit=args.limit)
    fits = load_fitted_scalings(arm=str(ScalingArm.SOMA_AIS))
    bias = load_bias()
    conds = CONDS if bias is not None else CONDS[:2]
    seeds = eval_seeds()[:PD_N_SEEDS]
    t0 = time.time()

    # ---- (a) strength sweep (PD direction only; excitatory weights scaled by u / 100) ----
    strengths: list[float] = [0.0, 100.0] if args.gate else PD_STRENGTHS
    sweep_jobs: list[TrialJob] = []
    for c in cells:
        for cond in conds:
            spec = cond_spec(cond=cond, fit=fits[c.cell_id], bias=bias)
            for u in strengths:
                for si, base in enumerate(seeds[: (1 if args.gate else PD_N_SEEDS)]):
                    seed = trial_seed(base_seed=base, direction_deg=PD_DIRECTION_DEG)
                    sweep_jobs.append(
                        _make_job(
                            key=f"sweep|{c.cell_id}|{cond}|{u:.0f}|{si}",
                            cell=c,
                            spec=spec,
                            mode=MODE_BAR,
                            direction_deg=PD_DIRECTION_DEG,
                            exc_scale=u / 100.0,
                            seed_index=si,
                            seed=seed,
                            tstop_ms=TSTOP_MS,
                        )
                    )
    sweep_path = (
        PANEL_D_SWEEP_TRIALS_JSONL.with_name("panel_d_gate_trials.jsonl")
        if args.gate
        else PANEL_D_SWEEP_TRIALS_JSONL
    )
    rows = run_jobs(
        jobs=sweep_jobs,
        worker_fn=trial_worker,
        out_path=sweep_path,
        key_of=lambda j: j.job_key,
        max_workers=args.workers,
        desc="panel_d_sweep",
    )
    dsi_rows = load_done_rows(path=DSI_TRIALS_JSONL)
    gate: dict[str, Any] = {}
    for c in cells:
        for si in range(1 if args.gate else PD_N_SEEDS):
            key100 = f"sweep|{c.cell_id}|wt_like|100|{si}"
            dsi_key = f"dsi|{ScalingArm.SOMA_AIS}|{c.cell_id}|wt_like|0|{si}"
            if key100 in rows and dsi_key in dsi_rows:
                a = int(rows[key100]["spike_count"])
                b = int(dsi_rows[dsi_key]["spike_count"])
                gate[f"{c.cell_id}|{si}"] = {
                    "u100_spikes": a,
                    "dsi_run_spikes": b,
                    "within_10pct": abs(a - b) <= GATE_TOLERANCE * max(b, 1),
                }
    print("gate u=100 vs DSI-run WT-like PD:", json.dumps(gate))
    if args.gate:
        for k, v in rows.items():
            print(k, v["spike_count"])
        return
    sweep_recs: list[dict[str, Any]] = []
    for c in cells:
        for cond in conds:
            for u in strengths:
                counts = [
                    int(rows[f"sweep|{c.cell_id}|{cond}|{u:.0f}|{si}"]["spike_count"])
                    for si in range(PD_N_SEEDS)
                ]
                sweep_recs.append(
                    {
                        "cell_id": c.cell_id,
                        "condition": cond,
                        "u": u,
                        "mean_spikes": float(np.mean(counts)),
                        "rate_hz": float(np.mean(counts)) / (TSTOP_MS / 1000.0),
                        "counts": counts,
                    }
                )
    sweep_df = pd.DataFrame(sweep_recs)
    sweep_df.to_csv(PANEL_D_SWEEP_CSV, index=False)

    # ---- (b) three-pulse drive ----
    pulse_jobs: list[TrialJob] = []
    for c in cells:
        for cond in conds:
            spec = cond_spec(cond=cond, fit=fits[c.cell_id], bias=bias)
            for rep in range(PULSE_N_REPS):
                seed = PULSE_BASE_SEED + PULSE_SEED_STRIDE * rep
                pulse_jobs.append(
                    _make_job(
                        key=f"pulse|{c.cell_id}|{cond}|{rep}",
                        cell=c,
                        spec=spec,
                        mode=MODE_PULSE,
                        direction_deg=0.0,
                        exc_scale=1.0,
                        seed_index=rep,
                        seed=seed,
                        tstop_ms=PULSE_TSTOP_MS,
                    )
                )
    prow = run_jobs(
        jobs=pulse_jobs,
        worker_fn=trial_worker,
        out_path=PANEL_D_PULSE_TRIALS_JSONL,
        key_of=lambda j: j.job_key,
        max_workers=args.workers,
        desc="panel_d_pulses",
    )
    print(f"panel D wall time {time.time() - t0:.1f} s", flush=True)
    n_bins = int(PULSE_TSTOP_MS / PSTH_BIN_MS)
    t_centres = (np.arange(n_bins, dtype=np.float64) + 0.5) * PSTH_BIN_MS
    psth_store: dict[str, Any] = {"t_ms": t_centres}
    pulse_recs: list[dict[str, Any]] = []
    metrics_by: dict[str, dict[str, PulseMetrics]] = {}
    for c in cells:
        for cond in conds:
            bin_counts = np.zeros(n_bins, dtype=np.float64)
            n_sp = 0
            for rep in range(PULSE_N_REPS):
                r = prow[f"pulse|{c.cell_id}|{cond}|{rep}"]
                times = np.asarray(r["spike_times_ms"], dtype=np.float64)
                n_sp += len(times)
                if len(times) > 0:
                    hist, _edges = np.histogram(times, bins=n_bins, range=(0.0, PULSE_TSTOP_MS))
                    bin_counts += hist
            psth_hz = bin_counts / (PULSE_N_REPS * (PSTH_BIN_MS / 1000.0))
            smooth = gaussian_smooth(y=psth_hz, sigma_bins=PSTH_SMOOTH_SIGMA_MS / PSTH_BIN_MS)
            m = pulse_metrics(t_ms=t_centres, y=smooth)
            metrics_by.setdefault(c.cell_id, {})[cond] = m
            psth_store[f"{c.cell_id}|{cond}"] = smooth
            pulse_recs.append(
                {
                    "cell_id": c.cell_id,
                    "condition": cond,
                    "n_spikes_total": n_sp,
                    "mean_rate_hz": n_sp / (PULSE_N_REPS * PULSE_TSTOP_MS / 1000.0),
                    "mean_peak_hz": m.mean_peak,
                    "baseline_hz": m.baseline_abs,
                    "baseline_rel_to_peak": m.baseline_rel,
                    "min_between_hz": m.mean_min_between,
                    "distinctness": m.distinctness,
                    "fwhm_ms": m.mean_fwhm_ms,
                    "locking_r": m.locking_r,
                }
            )
    pulse_df = pd.DataFrame(pulse_recs)
    pulse_df.to_csv(PANEL_D_PULSES_CSV, index=False)
    np.savez_compressed(PANEL_D_PSTH_NPZ, **psth_store)

    # ---- verdicts ----
    toy = json.loads(TOY_PARAMS_JSON.read_text(encoding="utf-8"))
    toy_wt = toy["pulse_metrics"]["wt"]
    toy_rd1 = toy["pulse_metrics"]["rd1"]
    verdicts: dict[str, Any] = {"cells": [c.cell_id for c in cells]}
    for suffix in ("", "_with_bias"):
        wt_c, rd_c = f"wt_like{suffix}", f"rd1_like{suffix}"
        if wt_c not in conds:
            continue
        sat: dict[str, dict[str, float | None]] = {wt_c: {}, rd_c: {}}
        growth: dict[str, float | None] = {}
        for c in cells:
            for cond in (wt_c, rd_c):
                sub = sweep_df[(sweep_df.cell_id == c.cell_id) & (sweep_df.condition == cond)]
                r100 = float(sub[sub.u == 100.0].rate_hz.iloc[0])
                r20 = float(sub[sub.u == 20.0].rate_hz.iloc[0])
                r0 = float(sub[sub.u == 0.0].rate_hz.iloc[0])
                sat[cond][c.cell_id] = (r20 / r100) if r100 > 0.0 else None
                if cond == wt_c:
                    growth[c.cell_id] = r100 - r0
        med_sat_wt = median_or_none(values=list(sat[wt_c].values()))
        med_sat_rd = median_or_none(values=list(sat[rd_c].values()))
        n_rd_sat_cells = sum(
            1 for v in sat[rd_c].values() if v is not None and v >= SAT_PRED_RD1_MIN
        )
        # Prediction 1: rd1 output flat and saturated at all but the lowest strengths.
        rd_rates = {
            c.cell_id: float(
                sweep_df[
                    (sweep_df.cell_id == c.cell_id)
                    & (sweep_df.condition == rd_c)
                    & (sweep_df.u == 100.0)
                ].rate_hz.iloc[0]
            )
            for c in cells
        }
        rd_active = [v for v in rd_rates.values() if v > 0.0]
        p1_dir = med_sat_rd is not None and (med_sat_wt is None or med_sat_rd > med_sat_wt)
        p1_mag = med_sat_rd is not None and med_sat_rd >= SAT_PRED_RD1_MIN
        if len(rd_active) == 0:
            p1 = "disproved"
            p1_note = "rd1-like output is zero at u=100 in every cell (flat at zero, not saturated)"
        else:
            p1 = verdict_from_flags(
                direction_ok=bool(p1_dir),
                magnitude_ok=bool(p1_mag),
                some_cells_ok=n_rd_sat_cells > 0,
            )
            p1_note = (
                f"median saturation index rd1={med_sat_rd}, wt={med_sat_wt}; "
                f"rd1 cells >= {SAT_PRED_RD1_MIN}: {n_rd_sat_cells}/{len(cells)}"
            )
        # Prediction 2: WT output grows gradually (saturation index <= 0.6 and positive growth).
        n_wt_grad = sum(
            1
            for c in cells
            if _le(value=sat[wt_c][c.cell_id], limit=SAT_PRED_WT_MAX)
            and _gt(value=growth[c.cell_id], limit=0.0)
        )
        wt_dir = med_sat_wt is not None and med_sat_wt <= SAT_PRED_WT_MAX
        p2 = verdict_from_flags(
            direction_ok=bool(wt_dir), magnitude_ok=bool(wt_dir), some_cells_ok=n_wt_grad > 0
        )
        # Prediction 3: elevated baseline in rd1 (relative to own peak), ~0.35.
        bl_wt = median_or_none(values=[metrics_by[c.cell_id][wt_c].baseline_rel for c in cells])
        bl_rd = median_or_none(values=[metrics_by[c.cell_id][rd_c].baseline_rel for c in cells])
        base_rd_hz = median_or_none(
            values=[metrics_by[c.cell_id][rd_c].baseline_abs for c in cells]
        )
        base_wt_hz = median_or_none(
            values=[metrics_by[c.cell_id][wt_c].baseline_abs for c in cells]
        )
        n_bl = sum(
            1
            for c in cells
            if _baseline_elevated(
                m_rd=metrics_by[c.cell_id][rd_c], m_wt=metrics_by[c.cell_id][wt_c]
            )
        )
        p3_dir = bl_rd is not None and bl_wt is not None and bl_rd > bl_wt
        p3_mag = (
            bl_rd is not None and bl_wt is not None and (bl_rd - bl_wt) >= 0.5 * BASELINE_PRED_RD1
        )
        if bl_rd is None:
            p3 = "disproved"
            p3_note = "rd1-like pulse response undefined (no spikes), so no elevated baseline"
        else:
            p3 = verdict_from_flags(
                direction_ok=bool(p3_dir), magnitude_ok=bool(p3_mag), some_cells_ok=n_bl > 0
            )
            p3_note = (
                f"median baseline/peak rd1={bl_rd}, wt={bl_wt}; cells meeting half magnitude {n_bl}"
            )
        # Prediction 4: temporal smearing (lower distinctness, broader peaks in rd1).
        d_wt = median_or_none(values=[metrics_by[c.cell_id][wt_c].distinctness for c in cells])
        d_rd = median_or_none(values=[metrics_by[c.cell_id][rd_c].distinctness for c in cells])
        f_wt = median_or_none(values=[metrics_by[c.cell_id][wt_c].mean_fwhm_ms for c in cells])
        f_rd = median_or_none(values=[metrics_by[c.cell_id][rd_c].mean_fwhm_ms for c in cells])
        toy_d = (toy_wt["distinctness"] or 0.0) - (toy_rd1["distinctness"] or 0.0)
        toy_f = (toy_rd1["mean_fwhm_ms"] or 0.0) - (toy_wt["mean_fwhm_ms"] or 0.0)
        if d_rd is None or d_wt is None:
            p4 = "disproved"
            p4_note = "rd1-like or WT-like pulse response undefined (no spikes)"
        else:
            dir_d = d_rd < d_wt
            mag_d = (d_wt - d_rd) >= 0.5 * toy_d
            dir_f = f_wt is not None and f_rd is not None and f_rd > f_wt
            mag_f = dir_f and (f_rd - f_wt) >= 0.5 * toy_f  # type: ignore[operator]
            p4 = verdict_from_flags(
                direction_ok=bool(dir_d and dir_f),
                magnitude_ok=bool(mag_d and mag_f),
                some_cells_ok=bool(dir_d or dir_f),
            )
            p4_note = (
                f"median distinctness rd1={d_rd}, wt={d_wt}; FWHM rd1={f_rd}, wt={f_wt}; "
                f"toy differences d={toy_d}, fwhm={toy_f}"
            )
        verdicts[f"series{suffix or '_no_bias'}"] = {
            "conditions": [wt_c, rd_c],
            "saturation_index_per_cell": sat,
            "median_saturation_index": {wt_c: med_sat_wt, rd_c: med_sat_rd},
            "median_baseline_hz": {wt_c: base_wt_hz, rd_c: base_rd_hz},
            "predictions": {
                "rd1_flat_saturated": {"verdict": p1, "evidence": p1_note},
                "wt_gradual_growth": {
                    "verdict": p2,
                    "evidence": (
                        f"median WT saturation index {med_sat_wt}; cells with index <= "
                        f"{SAT_PRED_WT_MAX} and positive growth: {n_wt_grad}/{len(cells)}"
                    ),
                },
                "rd1_elevated_baseline": {"verdict": p3, "evidence": p3_note},
                "rd1_temporal_smearing": {"verdict": p4, "evidence": p4_note},
            },
        }
    verdicts["rules"] = (
        "reproduced: direction and at least half the predicted magnitude hold in the median over "
        "cells; partly reproduced: direction only, or holds in some cells; disproved: opposite, "
        "absent or undefined because the rd1-like response is silent"
    )
    PANEL_D_VERDICTS_JSON.write_text(json.dumps(verdicts, indent=2), encoding="utf-8")
    print(
        json.dumps({k: v for k, v in verdicts.items() if k.startswith("series")}, indent=1)[:4000]
    )


if __name__ == "__main__":
    main()
