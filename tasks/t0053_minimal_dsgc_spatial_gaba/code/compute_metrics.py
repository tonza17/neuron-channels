"""Compute per-mode tuning-curve metrics and write metrics.json + derived_quantities.json.

Adapted from t0052's ``compute_metrics.py``. Differences:

* The IPSP-conductance hard gate (``gNULL/gPD ~= 3``, ``[2.7, 3.3]``) is removed because the
  spatial centripetal-gating mechanism has no scalar amplitude endpoints — every I synapse either
  fires at full 2 nS or is silent.
* A soft per-direction active-fraction sanity check replaces it: read
  ``active_fraction_per_direction.csv``, compute the cross-direction mean, and WARN (do not raise)
  if the mean is outside ``[ACTIVE_FRACTION_LOWER, ACTIVE_FRACTION_UPPER]``. Always write the per
  direction list and the mean to ``derived_quantities.json``.
* No more ``gaba_mod`` import; per-direction GABA conductance is binary (0 or full amplitude).
"""

from __future__ import annotations

import json
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
from tasks.t0053_minimal_dsgc_spatial_gaba.code.constants import (
    ACTIVE_FRACTION_LOWER,
    ACTIVE_FRACTION_UPPER,
    BASE_OFFSET_MS,
    COL_ACTIVE_FRACTION,
    COL_ANGLE_DEG,
    COL_T_MS,
    COL_TRIAL_SEED,
    COL_VOLTAGE_MV,
    METRIC_KEY_DSI,
    METRIC_KEY_HWHM,
    METRIC_KEY_RELIABILITY,
    METRIC_KEY_RMSE,
    V_INIT_MV,
)
from tasks.t0053_minimal_dsgc_spatial_gaba.code.metrics_extra import (
    compute_preferred_direction_deg,
    compute_vector_sum_dsi,
)
from tasks.t0053_minimal_dsgc_spatial_gaba.code.paths import (
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


def _peak_depolarization_per_angle(
    *,
    voltage_csv: Path,
    baseline_mv: float = V_INIT_MV,
    pre_stim_window_ms: float = BASE_OFFSET_MS - 5.0,
) -> dict[int, float]:
    """Per-angle mean (across trials) peak somatic deflection magnitude in mV."""
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=voltage_csv)
    df_post = df[df[COL_T_MS] >= pre_stim_window_ms]
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


def _build_full_variant(*, full_curve: TuningCurve) -> dict[str, object]:
    metrics: dict[str, float | None] = {}
    metrics[METRIC_KEY_DSI] = compute_dsi(curve=full_curve)
    metrics[METRIC_KEY_HWHM] = compute_hwhm_deg(curve=full_curve)
    reliability: float | None = compute_reliability(curve=full_curve)
    metrics[METRIC_KEY_RELIABILITY] = reliability
    rmse: float | None = _compute_rmse_against_target(
        full_curve=full_curve,
        target_csv=TARGET_TUNING_CURVE_CSV,
    )
    if rmse is not None:
        metrics[METRIC_KEY_RMSE] = rmse
    return {
        "variant_id": "full",
        "label": "Full E+I (spatial centripetal gating)",
        "dimensions": {"mode": "full"},
        "metrics": metrics,
    }


def _build_ampa_variant(*, ampa_curve: TuningCurve) -> dict[str, object]:
    metrics: dict[str, float | None] = {}
    metrics[METRIC_KEY_DSI] = compute_dsi(curve=ampa_curve)
    metrics[METRIC_KEY_RELIABILITY] = compute_reliability(curve=ampa_curve)
    return {
        "variant_id": "ampa_only",
        "label": "AMPA only (zeroed GABA NetCons)",
        "dimensions": {"mode": "ampa_only"},
        "metrics": metrics,
    }


def _build_gaba_variant(*, gaba_curve: TuningCurve) -> dict[str, object]:
    metrics: dict[str, float | None] = {}
    if compute_peak_hz(curve=gaba_curve) > 0.0:
        metrics[METRIC_KEY_DSI] = compute_dsi(curve=gaba_curve)
    return {
        "variant_id": "gaba_only",
        "label": "GABA only (zeroed AMPA NetCons; spatial gating preserved)",
        "dimensions": {"mode": "gaba_only"},
        "metrics": metrics,
    }


def _load_active_fraction_per_direction(*, csv_path: Path) -> dict[int, float]:
    """Read the per-direction active-fraction CSV and return a {angle_deg: fraction} dict."""
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Active-fraction CSV not found at {csv_path}; did the sweep run?",
        )
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=csv_path)
    return {int(row[COL_ANGLE_DEG]): float(row[COL_ACTIVE_FRACTION]) for _, row in df.iterrows()}


def main() -> int:
    print("[metrics] Loading per-mode tuning curves...", flush=True)
    full_curve: TuningCurve = load_tuning_curve(csv_path=TUNING_CURVE_FULL_CSV)
    ampa_curve: TuningCurve = load_tuning_curve(csv_path=TUNING_CURVE_AMPA_ONLY_CSV)
    gaba_curve: TuningCurve = load_tuning_curve(csv_path=TUNING_CURVE_GABA_ONLY_CSV)

    print("[metrics] Computing peak somatic deflection per direction...", flush=True)
    ampa_peak_dep_per_angle: dict[int, float] = _peak_depolarization_per_angle(
        voltage_csv=VOLTAGE_TRACES_AMPA_ONLY_CSV,
    )
    gaba_peak_dep_per_angle: dict[int, float] = _peak_depolarization_per_angle(
        voltage_csv=VOLTAGE_TRACES_GABA_ONLY_CSV,
    )

    # ----------------------------------------------------------------
    # Soft active-fraction sanity check (replaces the t0052 hard IPSP-conductance gate).
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
        f"[metrics] active fraction per direction: "
        f"{ {int(k): round(v, 4) for k, v in active_fraction_per_direction.items()} }",
        flush=True,
    )
    print(
        f"[metrics] mean_active_fraction = {mean_active_fraction:.4f} "
        f"(soft band [{ACTIVE_FRACTION_LOWER}, {ACTIVE_FRACTION_UPPER}])",
        flush=True,
    )
    if not (ACTIVE_FRACTION_LOWER <= mean_active_fraction <= ACTIVE_FRACTION_UPPER):
        print(
            f"WARNING: mean_active_fraction = {mean_active_fraction:.4f} is outside "
            f"[{ACTIVE_FRACTION_LOWER}, {ACTIVE_FRACTION_UPPER}]; this is informational and "
            f"reflects dendritic-field asymmetry from the off-centre soma. Continuing.",
            file=sys.stderr,
            flush=True,
        )

    # ----------------------------------------------------------------
    # Metrics JSON (explicit multi-variant format).
    # ----------------------------------------------------------------
    variants: list[dict[str, object]] = [
        _build_full_variant(full_curve=full_curve),
        _build_ampa_variant(ampa_curve=ampa_curve),
        _build_gaba_variant(gaba_curve=gaba_curve),
    ]
    metrics_payload: dict[str, object] = {"variants": variants}
    METRICS_JSON.parent.mkdir(parents=True, exist_ok=True)
    METRICS_JSON.write_text(json.dumps(metrics_payload, indent=2), encoding="utf-8")
    print(f"[metrics] Wrote {METRICS_JSON}", flush=True)

    # ----------------------------------------------------------------
    # Derived quantities JSON (non-registered scalars).
    # ----------------------------------------------------------------
    aggregate_epsp: dict[str, float] = {
        f"angle_{angle:03d}": float(value)
        for angle, value in sorted(ampa_peak_dep_per_angle.items())
    }
    aggregate_ipsp: dict[str, float] = {
        f"angle_{angle:03d}": float(value)
        for angle, value in sorted(gaba_peak_dep_per_angle.items())
    }
    active_fraction_block: dict[str, float] = {
        f"angle_{angle:03d}": float(value)
        for angle, value in sorted(active_fraction_per_direction.items())
    }

    # Per-variant peak/null/vector-sum/preferred_direction.
    per_variant_quantities: dict[str, dict[str, float | None]] = {
        "full": {
            "peak_hz": float(compute_peak_hz(curve=full_curve)),
            "null_hz": float(compute_null_hz(curve=full_curve)),
            "vector_sum_dsi": float(compute_vector_sum_dsi(curve=full_curve)),
            "preferred_direction_deg": float(compute_preferred_direction_deg(curve=full_curve)),
        },
        "ampa_only": {
            "peak_hz": float(compute_peak_hz(curve=ampa_curve)),
            "null_hz": float(compute_null_hz(curve=ampa_curve)),
            "vector_sum_dsi": float(compute_vector_sum_dsi(curve=ampa_curve)),
            "preferred_direction_deg": float(compute_preferred_direction_deg(curve=ampa_curve)),
        },
        "gaba_only": {
            "peak_hz": float(compute_peak_hz(curve=gaba_curve)),
            "null_hz": float(compute_null_hz(curve=gaba_curve)),
            "vector_sum_dsi": float(compute_vector_sum_dsi(curve=gaba_curve)),
            "preferred_direction_deg": float(compute_preferred_direction_deg(curve=gaba_curve)),
        },
    }

    derived: dict[str, object] = {
        # Top-level FULL-mode quantities (kept for parity with t0052 derived schema and for the
        # plan's verification gate).
        "peak_hz": per_variant_quantities["full"]["peak_hz"],
        "null_hz": per_variant_quantities["full"]["null_hz"],
        "vector_sum_dsi": per_variant_quantities["full"]["vector_sum_dsi"],
        "preferred_direction_deg": per_variant_quantities["full"]["preferred_direction_deg"],
        # Active-fraction soft sanity block.
        "active_fraction_per_direction": active_fraction_block,
        "mean_active_fraction": mean_active_fraction,
        "active_fraction_soft_lower": ACTIVE_FRACTION_LOWER,
        "active_fraction_soft_upper": ACTIVE_FRACTION_UPPER,
        "active_fraction_soft_pass": (
            ACTIVE_FRACTION_LOWER <= mean_active_fraction <= ACTIVE_FRACTION_UPPER
        ),
        # Aggregate EPSP / IPSP per direction.
        "aggregate_epsp_peak_per_direction_mv": aggregate_epsp,
        "aggregate_ipsp_peak_per_direction_mv": aggregate_ipsp,
        # Per-variant tuning quantities.
        "per_variant_quantities": per_variant_quantities,
        "rmse_target_note": (
            "tuning_curve_rmse omitted: t0004 target_tuning_curve.csv not present (this task is a "
            "mechanism-comparison sibling of t0052, not an optimisation target)"
            if not TARGET_TUNING_CURVE_CSV.exists()
            else "tuning_curve_rmse computed against t0004 target curve"
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
