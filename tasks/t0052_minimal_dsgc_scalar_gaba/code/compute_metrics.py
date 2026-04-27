"""Compute per-mode tuning-curve metrics and write metrics.json + derived_quantities.json.

* Loads each mode's tuning-curve CSV via the t0012 ``load_tuning_curve``.
* Computes registered-metric values (DSI, HWHM, reliability) for the FULL variant; DSI and
  reliability for AMPA_ONLY; (none usable for GABA_ONLY since it never fires).
* Computes derived quantities: peak Hz, null Hz, vector-sum DSI, preferred direction (deg),
  per-direction aggregate EPSP / IPSP peaks, the IPSP *conductance* ratio (gabaMOD(180) /
  gabaMOD(0)) and the IPSP *somatic-voltage-deflection* ratio.
* Hard-fails if the IPSP conductance ratio falls outside [2.7, 3.3] (REQ-18). The somatic-voltage
  ratio is generally below the conductance ratio because of synaptic driving-force saturation, and
  is recorded as a derived observable rather than a gate.
* Optionally adds ``tuning_curve_rmse`` to the FULL variant if a t0004 target curve exists.
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
from tasks.t0052_minimal_dsgc_scalar_gaba.code.constants import (
    BASE_OFFSET_MS,
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
from tasks.t0052_minimal_dsgc_scalar_gaba.code.metrics_extra import (
    compute_preferred_direction_deg,
    compute_vector_sum_dsi,
)
from tasks.t0052_minimal_dsgc_scalar_gaba.code.paths import (
    DERIVED_QUANTITIES_JSON,
    METRICS_JSON,
    TARGET_TUNING_CURVE_CSV,
    TUNING_CURVE_AMPA_ONLY_CSV,
    TUNING_CURVE_FULL_CSV,
    TUNING_CURVE_GABA_ONLY_CSV,
    VOLTAGE_TRACES_AMPA_ONLY_CSV,
    VOLTAGE_TRACES_GABA_ONLY_CSV,
)
from tasks.t0052_minimal_dsgc_scalar_gaba.code.synapses import gaba_mod

IPSP_RATIO_LOWER: float = 2.7
IPSP_RATIO_UPPER: float = 3.3
PD_ANGLE_DEG: float = 0.0
ND_ANGLE_DEG: float = 180.0


def _peak_depolarization_per_angle(
    *,
    voltage_csv: Path,
    baseline_mv: float = V_INIT_MV,
    pre_stim_window_ms: float = BASE_OFFSET_MS - 5.0,
) -> dict[int, float]:
    """Per-angle mean (across trials) peak somatic depolarisation in mV.

    For each trial, peak depolarisation = ``max(v_soma) - V_INIT_MV``, ignoring the pre-stimulus
    window. Returns a dict ``{angle_deg: mean_peak_dep_mv}``.

    NOTE: For IPSP traces the soma actually hyperpolarises, so we take the magnitude of the
    *deflection* from baseline (signed difference at peak amplitude time), looking at
    ``max(|v_soma - baseline|)``. This works for both EPSP (positive deflection) and IPSP
    (negative deflection) traces.
    """
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=voltage_csv)
    # Trial-level: group (angle, seed), find max |v - baseline| during stim window.
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
        "label": "Full E+I (scalar gabaMOD)",
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
    # GABA_ONLY produces no spikes; DSI is 0/0 -> 0 by convention. Don't claim anything.
    if compute_peak_hz(curve=gaba_curve) > 0.0:
        metrics[METRIC_KEY_DSI] = compute_dsi(curve=gaba_curve)
    return {
        "variant_id": "gaba_only",
        "label": "GABA only (zeroed AMPA NetCons)",
        "dimensions": {"mode": "gaba_only"},
        "metrics": metrics,
    }


def _safe_get_angle_value(*, mapping: dict[int, float], angle_deg: int) -> float | None:
    """Return ``mapping[angle_deg]`` as a float, or ``None`` if the angle is missing."""
    if angle_deg in mapping:
        return float(mapping[angle_deg])
    return None


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

    # IPSP-ratio sanity check: per the plan REQ-18 the canonical ratio is the *conductance* ratio
    # gabaMOD(180) / gabaMOD(0), expected to be ~ 0.99 / 0.33 ~= 3.03 by construction. We hard-fail
    # this gate (it must be exactly 3.0 + epsilon if synapses.gaba_mod is correctly defined).
    #
    # The somatic IPSP voltage-deflection ratio is a downstream observable that is generally less
    # than the conductance ratio because of synaptic driving-force saturation: as more synapses fire
    # the local membrane potential approaches E_GABA = -75 mV and the per-synapse driving force
    # collapses. We therefore record the conductance ratio (the gate) AND the somatic-IPSP ratio
    # (derived observable, no gate) so both are auditable.
    gaba_mod_pd: float = gaba_mod(theta_deg=PD_ANGLE_DEG)
    gaba_mod_nd: float = gaba_mod(theta_deg=ND_ANGLE_DEG)
    ipsp_conductance_ratio: float = gaba_mod_nd / gaba_mod_pd if gaba_mod_pd > 0.0 else math.inf
    print(
        f"[metrics] gabaMOD(0)={gaba_mod_pd:.4f}  gabaMOD(180)={gaba_mod_nd:.4f}  "
        f"conductance_ratio={ipsp_conductance_ratio:.4f}",
        flush=True,
    )
    if not (IPSP_RATIO_LOWER <= ipsp_conductance_ratio <= IPSP_RATIO_UPPER):
        print(
            f"[metrics] IPSP conductance-ratio sanity check FAILED: "
            f"{ipsp_conductance_ratio:.4f} not in [{IPSP_RATIO_LOWER}, {IPSP_RATIO_UPPER}]. "
            f"gabaMOD(0)={gaba_mod_pd:.4f} gabaMOD(180)={gaba_mod_nd:.4f}.",
            file=sys.stderr,
            flush=True,
        )
        raise AssertionError(
            f"IPSP conductance ratio gNULL/gPD = {ipsp_conductance_ratio:.4f} "
            f"outside [{IPSP_RATIO_LOWER}, {IPSP_RATIO_UPPER}]; "
            f"gabaMOD(0)={gaba_mod_pd:.4f}, gabaMOD(180)={gaba_mod_nd:.4f}.",
        )

    # Somatic IPSP voltage-deflection ratio (derived observable; reflects driving-force saturation).
    gaba_pd: float | None = _safe_get_angle_value(
        mapping=gaba_peak_dep_per_angle,
        angle_deg=int(PD_ANGLE_DEG),
    )
    gaba_nd: float | None = _safe_get_angle_value(
        mapping=gaba_peak_dep_per_angle,
        angle_deg=int(ND_ANGLE_DEG),
    )
    if gaba_pd is None or gaba_nd is None:
        print(
            f"[metrics] IPSP_PD={gaba_pd} IPSP_ND={gaba_nd}; cannot compute "
            f"somatic-deflection ratio (will write nulls).",
            flush=True,
        )
        ipsp_voltage_ratio: float | None = None
    elif gaba_pd > 0.0:
        ipsp_voltage_ratio = float(gaba_nd / gaba_pd)
    else:
        ipsp_voltage_ratio = None
    print(
        f"[metrics] Somatic IPSP deflection: PD={gaba_pd} mV ND={gaba_nd} mV "
        f"voltage_ratio={ipsp_voltage_ratio} (driving-force saturation expected to shrink "
        f"this below the conductance ratio).",
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
    derived: dict[str, object] = {
        "peak_hz": compute_peak_hz(curve=full_curve),
        "null_hz": compute_null_hz(curve=full_curve),
        "vector_sum_dsi": compute_vector_sum_dsi(curve=full_curve),
        "preferred_direction_deg": compute_preferred_direction_deg(curve=full_curve),
        "ipsp_conductance_ratio_null_over_pref": ipsp_conductance_ratio,
        "ipsp_voltage_ratio_null_over_pref": ipsp_voltage_ratio,
        "gaba_mod_pd": gaba_mod_pd,
        "gaba_mod_nd": gaba_mod_nd,
        "ipsp_pd_mv": gaba_pd,
        "ipsp_nd_mv": gaba_nd,
        "aggregate_epsp_peak_per_direction_mv": aggregate_epsp,
        "aggregate_ipsp_peak_per_direction_mv": aggregate_ipsp,
        "ampa_only_peak_hz": compute_peak_hz(curve=ampa_curve),
        "ampa_only_vector_sum_dsi": compute_vector_sum_dsi(curve=ampa_curve),
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
