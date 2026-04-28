"""Compute per-(gnmda, mode) tuning-curve metrics and write metrics.json.

Adapted from ``tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/compute_metrics.py``. Groups
each per-mode CSV by ``gnmda_ns`` to produce 12 metrics variants — one per (gNMDA, mode)
combination — with ``variant_id = f"gnmda_{gnmda:.2f}_{mode}"``.

Hard-fails if:

* The IPSP conductance ratio gabaMOD(180)/gabaMOD(0) is outside [2.7, 3.3].
* The gNMDA = 0 FULL-mode firing rates differ from t0054's ``tuning_curve_full.csv`` (filtered to
  ``gnmda_ns == 0.0``) by more than 1e-6 Hz on any (angle, trial) row (the gNMDA = 0 cross-task
  regression gate). Reference rebound from t0052 (used by t0054) to t0054 (used by t0055).

Writes:

* ``metrics.json`` — explicit multi-variant format with 12 variants.
* ``derived_quantities.json`` — per-variant peak Hz / null Hz / vector-sum DSI / preferred
  direction / active fraction; per-gNMDA EPSP decay-to-1/e (from E_ONLY at preferred
  direction); plus the IPSP-ratio fields and aggregate EPSP/IPSP per direction; plus the
  three pass-criterion booleans for the S-0054-01 headline gate
  (``pass_criterion_dsi_at_gnmda_025``, ``pass_criterion_peak_hz_at_gnmda_025``,
  ``pass_criterion_overall``).
"""

from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (
    TuningCurve,
    compute_dsi,
    compute_hwhm_deg,
    compute_null_hz,
    compute_peak_hz,
    compute_reliability,
    load_tuning_curve,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.constants import (
    BASE_OFFSET_MS,
    COL_ANGLE_DEG,
    COL_FIRING_RATE_HZ,
    COL_GNMDA_NS,
    COL_T_MS,
    COL_TRIAL_SEED,
    COL_VOLTAGE_MV,
    METRIC_KEY_DSI,
    METRIC_KEY_HWHM,
    METRIC_KEY_RELIABILITY,
    METRIC_KEY_RMSE,
    NMDA_PEAK_NS_VALUES,
    V_INIT_MV,
    TrialMode,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.metrics_extra import (
    compute_preferred_direction_deg,
    compute_vector_sum_dsi,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.paths import (
    DERIVED_QUANTITIES_JSON,
    METRICS_JSON,
    T0054_TUNING_CURVE_FULL_CSV,
    TARGET_TUNING_CURVE_CSV,
    TUNING_CURVE_E_ONLY_CSV,
    TUNING_CURVE_FULL_CSV,
    TUNING_CURVE_GABA_ONLY_CSV,
    VOLTAGE_TRACES_E_ONLY_CSV,
    VOLTAGE_TRACES_GABA_ONLY_CSV,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.synapses import gaba_mod

IPSP_RATIO_LOWER: float = 2.7
IPSP_RATIO_UPPER: float = 3.3
PD_ANGLE_DEG: float = 0.0
ND_ANGLE_DEG: float = 180.0
GNMDA0_REGRESSION_TOL_HZ: float = 1e-6
PASS_CRITERION_GNMDA_NS: float = 0.25
PASS_CRITERION_DSI_THRESHOLD: float = 0.50
PASS_CRITERION_PEAK_HZ_THRESHOLD: float = 5.0


def _slice_curve_by_gnmda(
    *,
    curve_csv: Path,
    gnmda_ns: float,
    tmp_dir: Path,
) -> TuningCurve:
    """Return a TuningCurve by writing a per-gNMDA slice to a temp CSV and re-reading via t0012."""
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=curve_csv)
    sub: pd.DataFrame = df[np.isclose(df[COL_GNMDA_NS], gnmda_ns)].drop(columns=[COL_GNMDA_NS])
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path: Path = tmp_dir / f"{curve_csv.stem}_gnmda_{gnmda_ns:.2f}.csv"
    sub.to_csv(path_or_buf=tmp_path, index=False)
    return load_tuning_curve(csv_path=tmp_path)


def _peak_depolarization_per_angle(
    *,
    voltage_csv: Path,
    gnmda_ns: float,
    baseline_mv: float = V_INIT_MV,
    pre_stim_window_ms: float = BASE_OFFSET_MS - 5.0,
) -> dict[int, float]:
    """Per-angle mean (across trials) peak somatic deflection in mV at a given gNMDA."""
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=voltage_csv)
    df = df[np.isclose(df[COL_GNMDA_NS], gnmda_ns)]
    df_post = df[df[COL_T_MS] >= pre_stim_window_ms]
    grouped = df_post.groupby([COL_ANGLE_DEG, COL_TRIAL_SEED], sort=True)[COL_VOLTAGE_MV]
    per_trial_peak: pd.Series = grouped.apply(
        lambda v: float(np.max(np.abs(v.to_numpy() - baseline_mv))),
    )
    per_trial_peak_df: pd.DataFrame = per_trial_peak.reset_index(name="peak_dep_mv")
    per_angle_mean = per_trial_peak_df.groupby(COL_ANGLE_DEG)["peak_dep_mv"].mean()
    return {int(angle): float(value) for angle, value in per_angle_mean.items()}


def _compute_epsp_decay_to_1e_ms(
    *,
    e_only_voltage_csv: Path,
    gnmda_ns: float,
    preferred_direction_deg: float,
    baseline_mv: float = V_INIT_MV,
) -> float | None:
    """Average the 10 E_ONLY trials at the preferred direction at this gNMDA; return decay time."""
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=e_only_voltage_csv)
    df = df[np.isclose(df[COL_GNMDA_NS], gnmda_ns)]
    target_angle: int = int(round(preferred_direction_deg))
    sub: pd.DataFrame = df[df[COL_ANGLE_DEG] == target_angle]
    if len(sub) == 0:
        return None
    pivot: pd.DataFrame = sub.pivot_table(
        index=COL_T_MS,
        columns=COL_TRIAL_SEED,
        values=COL_VOLTAGE_MV,
    )
    pivot = pivot.dropna(axis=0, how="any")
    if len(pivot) == 0:
        return None
    t_ms: np.ndarray = pivot.index.to_numpy(dtype=np.float64)
    v_mean: np.ndarray = pivot.to_numpy(dtype=np.float64).mean(axis=1)
    deflection: np.ndarray = v_mean - baseline_mv
    peak_idx: int = int(np.argmax(deflection))
    peak_dep: float = float(deflection[peak_idx])
    if peak_dep <= 0.0:
        return None
    threshold: float = peak_dep / math.e
    post_peak: np.ndarray = deflection[peak_idx:]
    crossing_indices: np.ndarray = np.where(post_peak <= threshold)[0]
    if len(crossing_indices) == 0:
        return None
    t_decay: float = float(t_ms[peak_idx + int(crossing_indices[0])])
    t_peak: float = float(t_ms[peak_idx])
    return t_decay - t_peak


def _compute_rmse_against_target(*, full_curve: TuningCurve, target_csv: Path) -> float | None:
    """Return RMSE between the full curve and the t0004 target curve, or None if unavailable."""
    if not target_csv.exists():
        return None
    target_curve: TuningCurve = load_tuning_curve(csv_path=target_csv)
    if target_curve.firing_rates_hz.shape != full_curve.firing_rates_hz.shape:
        return None
    if not np.allclose(target_curve.angles_deg, full_curve.angles_deg, atol=1e-3):
        return None
    diff: np.ndarray = full_curve.firing_rates_hz - target_curve.firing_rates_hz
    return float(np.sqrt(float(np.mean(diff * diff))))


def _build_full_variant(
    *,
    full_curve: TuningCurve,
    gnmda_ns: float,
) -> dict[str, object]:
    metrics: dict[str, float | None] = {}
    metrics[METRIC_KEY_DSI] = compute_dsi(curve=full_curve)
    metrics[METRIC_KEY_HWHM] = compute_hwhm_deg(curve=full_curve)
    metrics[METRIC_KEY_RELIABILITY] = compute_reliability(curve=full_curve)
    rmse: float | None = _compute_rmse_against_target(
        full_curve=full_curve,
        target_csv=TARGET_TUNING_CURVE_CSV,
    )
    if rmse is not None:
        metrics[METRIC_KEY_RMSE] = rmse
    return {
        "variant_id": f"gnmda_{gnmda_ns:.2f}_{TrialMode.FULL.value}",
        "label": f"gNMDA = {gnmda_ns:.2f} nS, FULL",
        "dimensions": {"gnmda_ns": gnmda_ns, "mode": TrialMode.FULL.value},
        "metrics": metrics,
    }


def _build_e_only_variant(
    *,
    e_only_curve: TuningCurve,
    gnmda_ns: float,
) -> dict[str, object]:
    metrics: dict[str, float | None] = {}
    if compute_peak_hz(curve=e_only_curve) > 0.0:
        metrics[METRIC_KEY_DSI] = compute_dsi(curve=e_only_curve)
    metrics[METRIC_KEY_RELIABILITY] = compute_reliability(curve=e_only_curve)
    return {
        "variant_id": f"gnmda_{gnmda_ns:.2f}_{TrialMode.E_ONLY.value}",
        "label": f"gNMDA = {gnmda_ns:.2f} nS, E_ONLY",
        "dimensions": {"gnmda_ns": gnmda_ns, "mode": TrialMode.E_ONLY.value},
        "metrics": metrics,
    }


def _build_gaba_variant(
    *,
    gaba_curve: TuningCurve,
    gnmda_ns: float,
) -> dict[str, object]:
    metrics: dict[str, float | None] = {}
    if compute_peak_hz(curve=gaba_curve) > 0.0:
        metrics[METRIC_KEY_DSI] = compute_dsi(curve=gaba_curve)
    return {
        "variant_id": f"gnmda_{gnmda_ns:.2f}_{TrialMode.GABA_ONLY.value}",
        "label": f"gNMDA = {gnmda_ns:.2f} nS, GABA_ONLY",
        "dimensions": {"gnmda_ns": gnmda_ns, "mode": TrialMode.GABA_ONLY.value},
        "metrics": metrics,
    }


def _check_gnmda0_regression(*, full_csv: Path) -> None:
    """Hard-fail if t0055 gnmda_ns=0 FULL rates differ from t0054's full curve at gnmda=0.

    Reads both CSVs, sorts by (angle_deg, trial_seed), and asserts row-by-row equality within
    1e-6 Hz. Failure means either (a) NMDA is leaking at zero conductance, (b) NetCon weight
    state is leaking between trials, or (c) the placement RNG drifted.
    """
    if not T0054_TUNING_CURVE_FULL_CSV.exists():
        print(
            f"[gnmda0-gate] t0054 tuning_curve_full.csv not found at "
            f"{T0054_TUNING_CURVE_FULL_CSV}; cannot run regression gate. STOP.",
            file=sys.stderr,
            flush=True,
        )
        raise FileNotFoundError(T0054_TUNING_CURVE_FULL_CSV)

    df_t0055: pd.DataFrame = pd.read_csv(filepath_or_buffer=full_csv)
    df_t0055_g0: pd.DataFrame = (
        df_t0055[np.isclose(df_t0055[COL_GNMDA_NS], 0.0)]
        .drop(columns=[COL_GNMDA_NS])
        .sort_values([COL_ANGLE_DEG, COL_TRIAL_SEED])
        .reset_index(drop=True)
    )
    df_t0054_full: pd.DataFrame = pd.read_csv(filepath_or_buffer=T0054_TUNING_CURVE_FULL_CSV)
    df_t0054_g0: pd.DataFrame = (
        df_t0054_full[np.isclose(df_t0054_full[COL_GNMDA_NS], 0.0)]
        .drop(columns=[COL_GNMDA_NS])
        .sort_values([COL_ANGLE_DEG, COL_TRIAL_SEED])
        .reset_index(drop=True)
    )
    assert len(df_t0055_g0) == len(df_t0054_g0), (
        f"Row count mismatch: t0055 (gnmda=0) has {len(df_t0055_g0)} rows, "
        f"t0054 (gnmda=0) has {len(df_t0054_g0)} rows."
    )
    rates_t0055: np.ndarray = df_t0055_g0[COL_FIRING_RATE_HZ].to_numpy(dtype=np.float64)
    rates_t0054: np.ndarray = df_t0054_g0[COL_FIRING_RATE_HZ].to_numpy(dtype=np.float64)
    diffs: np.ndarray = np.abs(rates_t0055 - rates_t0054)
    max_diff: float = float(np.max(diffs)) if diffs.size > 0 else 0.0
    print(
        f"[gnmda0-gate] max |rate diff| = {max_diff:.3e} Hz (n={len(rates_t0055)} rows)",
        flush=True,
    )
    if not np.allclose(rates_t0055, rates_t0054, atol=GNMDA0_REGRESSION_TOL_HZ, rtol=0.0):
        bad_idx: np.ndarray = np.where(diffs > GNMDA0_REGRESSION_TOL_HZ)[0]
        for idx in bad_idx[:10]:
            print(
                f"  mismatch[{idx}]: angle={int(df_t0054_g0.iloc[idx][COL_ANGLE_DEG])} "
                f"seed={int(df_t0054_g0.iloc[idx][COL_TRIAL_SEED])} "
                f"t0055={rates_t0055[idx]:.6f} Hz t0054={rates_t0054[idx]:.6f} Hz "
                f"diff={diffs[idx]:.3e} Hz",
                file=sys.stderr,
                flush=True,
            )
        raise AssertionError(
            f"gNMDA = 0 cross-task regression gate FAILED: {len(bad_idx)} rows differ from "
            f"t0054 by more than {GNMDA0_REGRESSION_TOL_HZ} Hz; max diff = {max_diff:.3e} Hz.",
        )
    print(
        "[gnmda0-gate] OK: t0055 gnmda=0 FULL rates match t0054 within tolerance.",
        flush=True,
    )


def main() -> int:
    print("[metrics] Running gNMDA = 0 cross-task regression gate first...", flush=True)
    _check_gnmda0_regression(full_csv=TUNING_CURVE_FULL_CSV)

    # IPSP conductance ratio sanity check (mode-independent and gnmda-independent).
    gaba_mod_pd: float = gaba_mod(theta_deg=PD_ANGLE_DEG)
    gaba_mod_nd: float = gaba_mod(theta_deg=ND_ANGLE_DEG)
    ipsp_conductance_ratio: float = gaba_mod_nd / gaba_mod_pd if gaba_mod_pd > 0.0 else math.inf
    print(
        f"[metrics] gabaMOD(0)={gaba_mod_pd:.4f}  gabaMOD(180)={gaba_mod_nd:.4f}  "
        f"conductance_ratio={ipsp_conductance_ratio:.4f}",
        flush=True,
    )
    if not (IPSP_RATIO_LOWER <= ipsp_conductance_ratio <= IPSP_RATIO_UPPER):
        raise AssertionError(
            f"IPSP conductance ratio gNULL/gPD = {ipsp_conductance_ratio:.4f} "
            f"outside [{IPSP_RATIO_LOWER}, {IPSP_RATIO_UPPER}]; "
            f"gabaMOD(0)={gaba_mod_pd:.4f}, gabaMOD(180)={gaba_mod_nd:.4f}.",
        )

    tmp_dir: Path = METRICS_JSON.parent / "_metrics_tmp"
    variants: list[dict[str, object]] = []
    derived_per_variant: dict[str, dict[str, object]] = {}
    derived_per_gnmda: dict[str, dict[str, object]] = {}

    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        gnmda_label: str = f"{gnmda_ns:.2f}"
        print(f"[metrics] === gNMDA = {gnmda_label} nS ===", flush=True)

        full_curve: TuningCurve = _slice_curve_by_gnmda(
            curve_csv=TUNING_CURVE_FULL_CSV,
            gnmda_ns=gnmda_ns,
            tmp_dir=tmp_dir,
        )
        e_only_curve: TuningCurve = _slice_curve_by_gnmda(
            curve_csv=TUNING_CURVE_E_ONLY_CSV,
            gnmda_ns=gnmda_ns,
            tmp_dir=tmp_dir,
        )
        gaba_curve: TuningCurve = _slice_curve_by_gnmda(
            curve_csv=TUNING_CURVE_GABA_ONLY_CSV,
            gnmda_ns=gnmda_ns,
            tmp_dir=tmp_dir,
        )

        variants.append(_build_full_variant(full_curve=full_curve, gnmda_ns=gnmda_ns))
        variants.append(_build_e_only_variant(e_only_curve=e_only_curve, gnmda_ns=gnmda_ns))
        variants.append(_build_gaba_variant(gaba_curve=gaba_curve, gnmda_ns=gnmda_ns))

        for label, curve in (
            (TrialMode.FULL.value, full_curve),
            (TrialMode.E_ONLY.value, e_only_curve),
            (TrialMode.GABA_ONLY.value, gaba_curve),
        ):
            derived_per_variant[f"gnmda_{gnmda_label}_{label}"] = {
                "peak_hz": compute_peak_hz(curve=curve),
                "null_hz": compute_null_hz(curve=curve),
                "vector_sum_dsi": compute_vector_sum_dsi(curve=curve),
                "preferred_direction_deg": compute_preferred_direction_deg(curve=curve),
                "active_fraction": 1.0,
            }

        preferred_dir: float = compute_preferred_direction_deg(curve=full_curve)
        epsp_decay_ms: float | None = _compute_epsp_decay_to_1e_ms(
            e_only_voltage_csv=VOLTAGE_TRACES_E_ONLY_CSV,
            gnmda_ns=gnmda_ns,
            preferred_direction_deg=preferred_dir,
        )
        e_only_peak_dep: dict[int, float] = _peak_depolarization_per_angle(
            voltage_csv=VOLTAGE_TRACES_E_ONLY_CSV,
            gnmda_ns=gnmda_ns,
        )
        gaba_peak_dep: dict[int, float] = _peak_depolarization_per_angle(
            voltage_csv=VOLTAGE_TRACES_GABA_ONLY_CSV,
            gnmda_ns=gnmda_ns,
        )
        gaba_pd: float | None = (
            float(gaba_peak_dep[int(PD_ANGLE_DEG)]) if int(PD_ANGLE_DEG) in gaba_peak_dep else None
        )
        gaba_nd: float | None = (
            float(gaba_peak_dep[int(ND_ANGLE_DEG)]) if int(ND_ANGLE_DEG) in gaba_peak_dep else None
        )
        ipsp_voltage_ratio: float | None = (
            float(gaba_nd / gaba_pd)
            if (gaba_pd is not None and gaba_nd is not None and gaba_pd > 0.0)
            else None
        )
        derived_per_gnmda[gnmda_label] = {
            "epsp_decay_to_1e_ms": epsp_decay_ms,
            "preferred_direction_deg": preferred_dir,
            "aggregate_epsp_peak_per_direction_mv": {
                f"angle_{angle:03d}": float(value)
                for angle, value in sorted(e_only_peak_dep.items())
            },
            "aggregate_ipsp_peak_per_direction_mv": {
                f"angle_{angle:03d}": float(value) for angle, value in sorted(gaba_peak_dep.items())
            },
            "ipsp_pd_mv": gaba_pd,
            "ipsp_nd_mv": gaba_nd,
            "ipsp_voltage_ratio_null_over_pref": ipsp_voltage_ratio,
        }

    # Write metrics.json.
    metrics_payload: dict[str, object] = {"variants": variants}
    METRICS_JSON.parent.mkdir(parents=True, exist_ok=True)
    METRICS_JSON.write_text(json.dumps(metrics_payload, indent=2), encoding="utf-8")
    print(f"[metrics] Wrote {METRICS_JSON} ({len(variants)} variants)", flush=True)

    # ---- Headline pass-criterion evaluation (S-0054-01) ----
    pass_key: str = f"gnmda_{PASS_CRITERION_GNMDA_NS:.2f}_full"
    pass_variant: dict[str, object] = derived_per_variant.get(pass_key, {})
    dsi_at_025: float | None = (
        float(pass_variant["vector_sum_dsi"])  # type: ignore[arg-type]
        if "vector_sum_dsi" in pass_variant and pass_variant["vector_sum_dsi"] is not None
        else None
    )
    peak_hz_at_025: float | None = (
        float(pass_variant["peak_hz"])  # type: ignore[arg-type]
        if "peak_hz" in pass_variant and pass_variant["peak_hz"] is not None
        else None
    )
    pass_dsi: bool = dsi_at_025 is not None and dsi_at_025 > PASS_CRITERION_DSI_THRESHOLD
    pass_hz: bool = (
        peak_hz_at_025 is not None and peak_hz_at_025 >= PASS_CRITERION_PEAK_HZ_THRESHOLD
    )
    pass_overall: bool = bool(pass_dsi and pass_hz)

    derived: dict[str, object] = {
        "ipsp_conductance_ratio_null_over_pref": ipsp_conductance_ratio,
        "gaba_mod_pd": gaba_mod_pd,
        "gaba_mod_nd": gaba_mod_nd,
        "per_variant": derived_per_variant,
        "per_gnmda": derived_per_gnmda,
        "pass_criterion_dsi_at_gnmda_025": pass_dsi,
        "pass_criterion_peak_hz_at_gnmda_025": pass_hz,
        "pass_criterion_overall": pass_overall,
        "pass_criterion_meta": {
            "gnmda_ns": PASS_CRITERION_GNMDA_NS,
            "mode": "full",
            "dsi_threshold_gt": PASS_CRITERION_DSI_THRESHOLD,
            "peak_hz_threshold_gte": PASS_CRITERION_PEAK_HZ_THRESHOLD,
            "dsi_observed": dsi_at_025,
            "peak_hz_observed": peak_hz_at_025,
        },
        "rmse_target_note": (
            "tuning_curve_rmse omitted: t0004 target_tuning_curve.csv not present"
            if not TARGET_TUNING_CURVE_CSV.exists()
            else "tuning_curve_rmse computed against t0004 target curve"
        ),
    }
    DERIVED_QUANTITIES_JSON.write_text(
        json.dumps(_to_jsonable(derived), indent=2),
        encoding="utf-8",
    )
    print(f"[metrics] Wrote {DERIVED_QUANTITIES_JSON}", flush=True)
    dsi_str: str = f"{dsi_at_025:.4f}" if dsi_at_025 is not None else "None"
    hz_str: str = f"{peak_hz_at_025:.4f}" if peak_hz_at_025 is not None else "None"
    print(
        f"[metrics] S-0054-01 PASS={pass_overall} (DSI={dsi_str} > 0.50? {pass_dsi}; "
        f"peakHz={hz_str} >= 5.0? {pass_hz})",
        flush=True,
    )
    return 0


def _to_jsonable(value: object) -> object:
    """Recursively convert numpy / pandas scalars to native JSON types."""
    if isinstance(value, dict):
        result_dict: dict[str, object] = {}
        for inner_k, inner_v in value.items():
            result_dict[str(inner_k)] = _to_jsonable(inner_v)
        return result_dict
    if isinstance(value, list | tuple):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, defaultdict):
        return _to_jsonable(dict(value))
    return value


if __name__ == "__main__":
    sys.exit(main())
