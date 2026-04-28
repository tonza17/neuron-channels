"""Compute per-(gaba, mode) tuning-curve metrics and write metrics.json + derived_quantities.json.

Adapted from ``tasks/t0053_minimal_dsgc_spatial_gaba/code/compute_metrics.py``. Differences:

* Per-mode tuning curves are pivoted by ``gaba_base_ns`` first; one
  :class:`tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.TuningCurve` is
  built per (gaba_base_ns, mode) pair.
* ``metrics.json`` contains 5 GABA values x 3 modes = 15 variants, each with the four registered
  metrics where applicable.
* ``derived_quantities.json`` carries cross-conductance summary arrays
  (``peak_hz_vs_gaba``, ``dsi_primary_vs_gaba``, etc.) and per-variant peak/null/vector-sum/
  preferred-direction.
* The AMPA_ONLY peak Hz regression sentinel (REQ-14) is enforced: every AMPA_ONLY variant must
  have peak_hz within 1e-3 of 0.6667.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
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
from tasks.t0057_tonic_gaba_sweep_t0053.code.constants import (
    ACTIVE_FRACTION_LOWER,
    ACTIVE_FRACTION_UPPER,
    AMPA_ONLY_PEAK_HZ_EXPECTED,
    AMPA_ONLY_PEAK_HZ_TOLERANCE,
    BASE_OFFSET_MS,
    COL_ACTIVE_FRACTION,
    COL_ANGLE_DEG,
    COL_FIRING_RATE_HZ,
    COL_GABA_BASE_NS,
    COL_T_MS,
    COL_TRIAL_SEED,
    COL_VOLTAGE_MV,
    GABA_BASE_NS_VALUES,
    METRIC_KEY_DSI,
    METRIC_KEY_HWHM,
    METRIC_KEY_RELIABILITY,
    METRIC_KEY_RMSE,
    V_INIT_MV,
    TrialMode,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.metrics_extra import (
    compute_preferred_direction_deg,
    compute_vector_sum_dsi,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.paths import (
    ACTIVE_FRACTION_CSV,
    DERIVED_QUANTITIES_JSON,
    METRICS_JSON,
    TARGET_TUNING_CURVE_CSV,
    TUNING_CURVE_AMPA_ONLY_CSV,
    TUNING_CURVE_FULL_CSV,
    TUNING_CURVE_GABA_ONLY_CSV,
    VOLTAGE_TRACES_AMPA_ONLY_CSV,
    VOLTAGE_TRACES_GABA_ONLY_CSV,
)


@dataclass(frozen=True, slots=True)
class CurveKey:
    gaba_base_ns: float
    mode: TrialMode


def _load_tuning_curve_for_gaba(*, csv_path: Path, gaba_base_ns: float) -> TuningCurve:
    """Build a TuningCurve for one GABA value by filtering the per-mode CSV."""
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=csv_path)
    sub: pd.DataFrame = df[np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6)]
    assert len(sub) > 0, (
        f"No rows for gaba_base_ns={gaba_base_ns} in {csv_path}; sweep did not run?"
    )
    # Build trials matrix to populate TuningCurve.trials (used by reliability scoring).
    grouped: pd.DataFrame = (
        sub.groupby(by=COL_ANGLE_DEG, sort=True)[COL_FIRING_RATE_HZ].apply(list).reset_index()
    )
    angles_deg: np.ndarray = grouped[COL_ANGLE_DEG].to_numpy(dtype=np.float64)
    trial_lists: list[list[float]] = grouped[COL_FIRING_RATE_HZ].tolist()
    n_trials_per_angle: set[int] = {len(lst) for lst in trial_lists}
    if len(n_trials_per_angle) != 1:
        # Fall back to mean-only if trials are unequal across angles (should not happen).
        firing_rates_hz: np.ndarray = np.array(
            [float(np.mean(lst)) for lst in trial_lists],
            dtype=np.float64,
        )
        return TuningCurve(
            angles_deg=angles_deg,
            firing_rates_hz=firing_rates_hz,
            trials=None,
        )
    trials_matrix: np.ndarray = np.array(
        [np.asarray(a=row, dtype=np.float64) for row in trial_lists],
        dtype=np.float64,
    )
    firing_rates_hz = trials_matrix.mean(axis=1)
    return TuningCurve(
        angles_deg=angles_deg,
        firing_rates_hz=firing_rates_hz,
        trials=trials_matrix,
    )


def _peak_depolarization_per_angle(
    *,
    voltage_csv: Path,
    gaba_base_ns: float,
    baseline_mv: float = V_INIT_MV,
    pre_stim_window_ms: float = BASE_OFFSET_MS - 5.0,
) -> dict[int, float]:
    """Per-angle mean (across trials) peak somatic deflection magnitude in mV at one GABA value."""
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=voltage_csv)
    sub: pd.DataFrame = df[np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6)]
    df_post = sub[sub[COL_T_MS] >= pre_stim_window_ms]
    grouped = df_post.groupby([COL_ANGLE_DEG, COL_TRIAL_SEED], sort=True)[COL_VOLTAGE_MV]
    per_trial_peak: pd.Series = grouped.apply(
        lambda v: float(np.max(np.abs(v.to_numpy() - baseline_mv))),
    )
    per_trial_peak_df: pd.DataFrame = per_trial_peak.reset_index(name="peak_dep_mv")
    per_angle_mean = per_trial_peak_df.groupby(COL_ANGLE_DEG)["peak_dep_mv"].mean()
    return {int(angle): float(value) for angle, value in per_angle_mean.items()}


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


def _build_variant_metrics(
    *,
    curve: TuningCurve,
    mode: TrialMode,
    target_csv: Path,
) -> dict[str, float | None]:
    """Compute the four registered metrics for one variant.

    For modes other than FULL, RMSE is omitted (the target curve is for the full system).
    DSI / HWHM / Reliability are only meaningful when peak_hz > 0.
    """
    metrics: dict[str, float | None] = {}
    peak_hz: float = float(compute_peak_hz(curve=curve))
    if peak_hz > 0.0:
        metrics[METRIC_KEY_DSI] = float(compute_dsi(curve=curve))
        metrics[METRIC_KEY_HWHM] = float(compute_hwhm_deg(curve=curve))
    reliability: float | None = compute_reliability(curve=curve)
    metrics[METRIC_KEY_RELIABILITY] = float(reliability) if reliability is not None else None
    if mode == TrialMode.FULL:
        rmse: float | None = _compute_rmse_against_target(
            full_curve=curve,
            target_csv=target_csv,
        )
        if rmse is not None:
            metrics[METRIC_KEY_RMSE] = rmse
    return metrics


def _variant_label(*, gaba_base_ns: float, mode: TrialMode) -> str:
    return f"GABA={gaba_base_ns:.2f} nS / {mode.value.upper()}"


def _variant_id(*, gaba_base_ns: float, mode: TrialMode) -> str:
    # Variant ids use lowercase letters/digits/dots/underscores per the metrics spec.
    return f"gaba_{gaba_base_ns:.2f}_{mode.value}"


def _all_curve_keys() -> Iterable[CurveKey]:
    for gaba_base_ns in GABA_BASE_NS_VALUES:
        for mode in (TrialMode.FULL, TrialMode.AMPA_ONLY, TrialMode.GABA_ONLY):
            yield CurveKey(gaba_base_ns=gaba_base_ns, mode=mode)


def _curve_csv_for_mode(*, mode: TrialMode) -> Path:
    if mode == TrialMode.FULL:
        return TUNING_CURVE_FULL_CSV
    if mode == TrialMode.AMPA_ONLY:
        return TUNING_CURVE_AMPA_ONLY_CSV
    if mode == TrialMode.GABA_ONLY:
        return TUNING_CURVE_GABA_ONLY_CSV
    raise AssertionError(f"Unhandled mode: {mode}")


def _load_active_fraction_per_direction(*, csv_path: Path) -> dict[int, float]:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Active-fraction CSV not found at {csv_path}; did the sweep run?",
        )
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=csv_path)
    return {int(row[COL_ANGLE_DEG]): float(row[COL_ACTIVE_FRACTION]) for _, row in df.iterrows()}


def _check_ampa_only_regression(
    *,
    curves_by_key: dict[CurveKey, TuningCurve],
) -> None:
    """REQ-14: every AMPA_ONLY variant must have peak_hz of approximately 0.6667 Hz."""
    for key, curve in curves_by_key.items():
        if key.mode != TrialMode.AMPA_ONLY:
            continue
        peak_hz: float = float(compute_peak_hz(curve=curve))
        delta: float = abs(peak_hz - AMPA_ONLY_PEAK_HZ_EXPECTED)
        if delta > AMPA_ONLY_PEAK_HZ_TOLERANCE:
            print(
                f"WARNING: REQ-14 sentinel: AMPA_ONLY peak_hz at "
                f"gaba_base_ns={key.gaba_base_ns:.2f} = {peak_hz:.6f} Hz, expected "
                f"{AMPA_ONLY_PEAK_HZ_EXPECTED:.6f} +/- {AMPA_ONLY_PEAK_HZ_TOLERANCE:.6f} Hz "
                f"(|delta|={delta:.6f}). The AMPA path is supposed to be unchanged from t0053.",
                file=sys.stderr,
                flush=True,
            )
        else:
            print(
                f"[regression] AMPA_ONLY peak_hz at gaba_base_ns={key.gaba_base_ns:.2f} = "
                f"{peak_hz:.6f} Hz (within {AMPA_ONLY_PEAK_HZ_TOLERANCE:.6f} of "
                f"{AMPA_ONLY_PEAK_HZ_EXPECTED:.6f}); REQ-14 PASS.",
                flush=True,
            )


def main() -> int:
    print("[metrics] Loading per-(gaba, mode) tuning curves...", flush=True)
    curves_by_key: dict[CurveKey, TuningCurve] = {}
    for key in _all_curve_keys():
        curves_by_key[key] = _load_tuning_curve_for_gaba(
            csv_path=_curve_csv_for_mode(mode=key.mode),
            gaba_base_ns=key.gaba_base_ns,
        )

    # ----------------------------------------------------------------
    # REQ-14 regression sentinel.
    # ----------------------------------------------------------------
    _check_ampa_only_regression(curves_by_key=curves_by_key)

    # ----------------------------------------------------------------
    # Per-(gaba) peak EPSP / IPSP envelopes (per-direction summary).
    # ----------------------------------------------------------------
    print("[metrics] Computing per-(gaba, angle) peak EPSP / IPSP magnitudes...", flush=True)
    epsp_per_gaba: dict[float, dict[int, float]] = {}
    ipsp_per_gaba: dict[float, dict[int, float]] = {}
    for gaba_base_ns in GABA_BASE_NS_VALUES:
        epsp_per_gaba[gaba_base_ns] = _peak_depolarization_per_angle(
            voltage_csv=VOLTAGE_TRACES_AMPA_ONLY_CSV,
            gaba_base_ns=gaba_base_ns,
        )
        ipsp_per_gaba[gaba_base_ns] = _peak_depolarization_per_angle(
            voltage_csv=VOLTAGE_TRACES_GABA_ONLY_CSV,
            gaba_base_ns=gaba_base_ns,
        )

    # ----------------------------------------------------------------
    # Active-fraction sanity check (carried over from t0053; conductance-independent).
    # ----------------------------------------------------------------
    active_fraction_per_direction: dict[int, float] = _load_active_fraction_per_direction(
        csv_path=ACTIVE_FRACTION_CSV,
    )
    fractions_array: np.ndarray = np.asarray(
        a=list(active_fraction_per_direction.values()),
        dtype=np.float64,
    )
    mean_active_fraction: float = float(np.mean(fractions_array))
    print(
        f"[metrics] mean_active_fraction = {mean_active_fraction:.4f} "
        f"(soft band [{ACTIVE_FRACTION_LOWER}, {ACTIVE_FRACTION_UPPER}])",
        flush=True,
    )
    if not (ACTIVE_FRACTION_LOWER <= mean_active_fraction <= ACTIVE_FRACTION_UPPER):
        print(
            f"WARNING: mean_active_fraction = {mean_active_fraction:.4f} is outside "
            f"[{ACTIVE_FRACTION_LOWER}, {ACTIVE_FRACTION_UPPER}]; informational only.",
            file=sys.stderr,
            flush=True,
        )

    # ----------------------------------------------------------------
    # Build the 15-variant metrics.json payload.
    # ----------------------------------------------------------------
    variants: list[dict[str, object]] = []
    for key in _all_curve_keys():
        curve: TuningCurve = curves_by_key[key]
        variant_metrics: dict[str, float | None] = _build_variant_metrics(
            curve=curve,
            mode=key.mode,
            target_csv=TARGET_TUNING_CURVE_CSV,
        )
        variants.append(
            {
                "variant_id": _variant_id(gaba_base_ns=key.gaba_base_ns, mode=key.mode),
                "label": _variant_label(gaba_base_ns=key.gaba_base_ns, mode=key.mode),
                "dimensions": {
                    "mode": key.mode.value,
                    "gaba_base_ns": float(key.gaba_base_ns),
                },
                "metrics": variant_metrics,
            },
        )
    metrics_payload: dict[str, object] = {"variants": variants}
    METRICS_JSON.parent.mkdir(parents=True, exist_ok=True)
    METRICS_JSON.write_text(json.dumps(metrics_payload, indent=2), encoding="utf-8")
    print(f"[metrics] Wrote {METRICS_JSON} with {len(variants)} variants", flush=True)

    # ----------------------------------------------------------------
    # Cross-conductance derived quantities.
    # ----------------------------------------------------------------
    per_variant_quantities: dict[str, dict[str, float | None]] = {}
    for key in _all_curve_keys():
        variant_id: str = _variant_id(gaba_base_ns=key.gaba_base_ns, mode=key.mode)
        curve = curves_by_key[key]
        peak_hz: float = float(compute_peak_hz(curve=curve))
        per_variant_quantities[variant_id] = {
            "peak_hz": peak_hz,
            "null_hz": float(compute_null_hz(curve=curve)),
            "vector_sum_dsi": float(compute_vector_sum_dsi(curve=curve)),
            "preferred_direction_deg": float(compute_preferred_direction_deg(curve=curve)),
        }

    # FULL-mode arrays vs gaba_base_ns (the sweep's headline panels).
    gaba_axis: list[float] = list(GABA_BASE_NS_VALUES)
    peak_hz_vs_gaba: list[float | None] = []
    null_hz_vs_gaba: list[float | None] = []
    dsi_primary_vs_gaba: list[float | None] = []
    dsi_vector_sum_vs_gaba: list[float | None] = []
    hwhm_vs_gaba: list[float | None] = []
    rmse_vs_gaba: list[float | None] = []
    for gaba_base_ns in GABA_BASE_NS_VALUES:
        full_key = CurveKey(gaba_base_ns=gaba_base_ns, mode=TrialMode.FULL)
        full_curve = curves_by_key[full_key]
        peak_hz_full: float = float(compute_peak_hz(curve=full_curve))
        peak_hz_vs_gaba.append(peak_hz_full)
        null_hz_vs_gaba.append(float(compute_null_hz(curve=full_curve)))
        dsi_primary_vs_gaba.append(
            float(compute_dsi(curve=full_curve)) if peak_hz_full > 0.0 else None,
        )
        dsi_vector_sum_vs_gaba.append(float(compute_vector_sum_dsi(curve=full_curve)))
        hwhm_vs_gaba.append(
            float(compute_hwhm_deg(curve=full_curve)) if peak_hz_full > 0.0 else None,
        )
        rmse: float | None = _compute_rmse_against_target(
            full_curve=full_curve,
            target_csv=TARGET_TUNING_CURVE_CSV,
        )
        rmse_vs_gaba.append(rmse)

    aggregate_epsp: dict[str, dict[str, float]] = {
        f"gaba_{g:.2f}": {f"angle_{a:03d}": float(v) for a, v in sorted(epsp_per_gaba[g].items())}
        for g in GABA_BASE_NS_VALUES
    }
    aggregate_ipsp: dict[str, dict[str, float]] = {
        f"gaba_{g:.2f}": {f"angle_{a:03d}": float(v) for a, v in sorted(ipsp_per_gaba[g].items())}
        for g in GABA_BASE_NS_VALUES
    }
    active_fraction_block: dict[str, float] = {
        f"angle_{angle:03d}": float(value)
        for angle, value in sorted(active_fraction_per_direction.items())
    }

    derived: dict[str, object] = {
        "gaba_base_ns_values": gaba_axis,
        "peak_hz_vs_gaba": peak_hz_vs_gaba,
        "null_hz_vs_gaba": null_hz_vs_gaba,
        "dsi_primary_vs_gaba": dsi_primary_vs_gaba,
        "dsi_vector_sum_vs_gaba": dsi_vector_sum_vs_gaba,
        "hwhm_vs_gaba": hwhm_vs_gaba,
        "rmse_vs_gaba": rmse_vs_gaba,
        "active_fraction_per_direction": active_fraction_block,
        "mean_active_fraction": mean_active_fraction,
        "active_fraction_soft_lower": ACTIVE_FRACTION_LOWER,
        "active_fraction_soft_upper": ACTIVE_FRACTION_UPPER,
        "active_fraction_soft_pass": (
            ACTIVE_FRACTION_LOWER <= mean_active_fraction <= ACTIVE_FRACTION_UPPER
        ),
        "aggregate_epsp_peak_per_direction_mv": aggregate_epsp,
        "aggregate_ipsp_peak_per_direction_mv": aggregate_ipsp,
        "per_variant_quantities": per_variant_quantities,
        "rmse_target_note": (
            "tuning_curve_rmse omitted: t0004 target_tuning_curve.csv not present"
            if not TARGET_TUNING_CURVE_CSV.exists()
            else "tuning_curve_rmse computed against t0004 target curve for FULL mode only"
        ),
    }
    DERIVED_QUANTITIES_JSON.write_text(
        json.dumps(_to_jsonable(derived), indent=2),
        encoding="utf-8",
    )
    print(f"[metrics] Wrote {DERIVED_QUANTITIES_JSON}", flush=True)
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
