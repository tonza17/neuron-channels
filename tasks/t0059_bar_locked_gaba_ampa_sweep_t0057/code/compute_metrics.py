"""Compute per-(gampa, gaba, mode) tuning-curve metrics and write metrics.json.

Adapted from ``tasks/t0057_tonic_gaba_sweep_t0053/code/compute_metrics.py``. Differences:

* Per-mode tuning curves are pivoted by (gampa_ns, gaba_base_ns, mode) — 75 variants.
* The legacy AMPA_ONLY peak-Hz regression sentinel is removed (peak Hz is direction-dependent
  under bar-locked windows).
* The IPSP-sustained-window check is removed (replaced by the bar-locked IPSP envelope test).
* EPSP_PASSIVE peak-Vm soft gate (REQ-15) is enforced inline.
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
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants import (
    ACTIVE_FRACTION_LOWER,
    ACTIVE_FRACTION_UPPER,
    AMPA_PEAK_NS_VALUES,
    BASE_OFFSET_MS,
    COL_ACTIVE_FRACTION,
    COL_ANGLE_DEG,
    COL_FIRING_RATE_HZ,
    COL_GABA_BASE_NS,
    COL_GAMPA_NS,
    COL_T_MS,
    COL_TRIAL_SEED,
    COL_VOLTAGE_MV,
    EPSP_PASSIVE_PEAK_VM_GATE_MV,
    GABA_BASE_NS_VALUES,
    METRIC_KEY_DSI,
    METRIC_KEY_HWHM,
    METRIC_KEY_RELIABILITY,
    METRIC_KEY_RMSE,
    V_INIT_MV,
    TrialMode,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.metrics_extra import (
    compute_preferred_direction_deg,
    compute_vector_sum_dsi,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.paths import (
    ACTIVE_FRACTION_CSV,
    DERIVED_QUANTITIES_JSON,
    METRICS_JSON,
    TARGET_TUNING_CURVE_CSV,
    TUNING_CURVE_EPSP_PASSIVE_CSV,
    TUNING_CURVE_FULL_CSV,
    TUNING_CURVE_IPSP_PASSIVE_CSV,
    VOLTAGE_TRACES_EPSP_PASSIVE_CSV,
    VOLTAGE_TRACES_IPSP_PASSIVE_CSV,
)


@dataclass(frozen=True, slots=True)
class CurveKey:
    gampa_ns: float
    gaba_base_ns: float
    mode: TrialMode


def _load_tuning_curve_for_cell(
    *,
    csv_path: Path,
    gampa_ns: float,
    gaba_base_ns: float,
) -> TuningCurve:
    """Build a TuningCurve for one (gampa, gaba) cell by filtering the per-mode CSV."""
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=csv_path)
    sub: pd.DataFrame = df[
        np.isclose(df[COL_GAMPA_NS], gampa_ns, atol=1e-6)
        & np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6)
    ]
    assert len(sub) > 0, (
        f"No rows for gampa_ns={gampa_ns}, gaba_base_ns={gaba_base_ns} in {csv_path}; "
        f"sweep did not run?"
    )
    grouped: pd.DataFrame = (
        sub.groupby(by=COL_ANGLE_DEG, sort=True)[COL_FIRING_RATE_HZ].apply(list).reset_index()
    )
    angles_deg: np.ndarray = grouped[COL_ANGLE_DEG].to_numpy(dtype=np.float64)
    trial_lists: list[list[float]] = grouped[COL_FIRING_RATE_HZ].tolist()
    n_trials_per_angle: set[int] = {len(lst) for lst in trial_lists}
    if len(n_trials_per_angle) != 1:
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
    gampa_ns: float,
    gaba_base_ns: float,
    baseline_mv: float = V_INIT_MV,
    pre_stim_window_ms: float = BASE_OFFSET_MS - 5.0,
) -> dict[int, float]:
    """Per-angle mean (across trials) peak somatic deflection magnitude in mV at one cell."""
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=voltage_csv)
    sub: pd.DataFrame = df[
        np.isclose(df[COL_GAMPA_NS], gampa_ns, atol=1e-6)
        & np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6)
    ]
    df_post = sub[sub[COL_T_MS] >= pre_stim_window_ms]
    grouped = df_post.groupby([COL_ANGLE_DEG, COL_TRIAL_SEED], sort=True)[COL_VOLTAGE_MV]
    per_trial_peak: pd.Series = grouped.apply(
        lambda v: float(np.max(np.abs(v.to_numpy() - baseline_mv))),
    )
    per_trial_peak_df: pd.DataFrame = per_trial_peak.reset_index(name="peak_dep_mv")
    per_angle_mean = per_trial_peak_df.groupby(COL_ANGLE_DEG)["peak_dep_mv"].mean()
    return {int(angle): float(value) for angle, value in per_angle_mean.items()}


def _peak_vm_overall(
    *,
    voltage_csv: Path,
    gampa_ns: float,
    gaba_base_ns: float,
) -> float:
    """Maximum somatic Vm across all trials and times at one (gampa, gaba) cell."""
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=voltage_csv)
    sub: pd.DataFrame = df[
        np.isclose(df[COL_GAMPA_NS], gampa_ns, atol=1e-6)
        & np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6)
    ]
    if len(sub) == 0:
        return float("-inf")
    return float(sub[COL_VOLTAGE_MV].max())


def _epsp_decay_per_angle(
    *,
    voltage_csv: Path,
    gampa_ns: float,
    gaba_base_ns: float,
    baseline_mv: float = V_INIT_MV,
    decay_t_late_ms: float = 1300.0,
    decay_t_early_ms: float = 200.0,
) -> dict[int, float | None]:
    """Per-angle EPSP decay metric (RQ5).

    Defined as the ratio |v(decay_t_late) - V_INIT| / |v(decay_t_early) - V_INIT|, mean across
    trials. Returns None per angle if the early window has zero deflection (decay undefined).
    """
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=voltage_csv)
    sub: pd.DataFrame = df[
        np.isclose(df[COL_GAMPA_NS], gampa_ns, atol=1e-6)
        & np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6)
    ]
    out: dict[int, float | None] = {}
    for angle_deg, sub_a in sub.groupby(COL_ANGLE_DEG):
        ratios: list[float] = []
        for _, sub_t in sub_a.groupby(COL_TRIAL_SEED):
            t_arr: np.ndarray = sub_t[COL_T_MS].to_numpy(dtype=np.float64)
            v_arr: np.ndarray = sub_t[COL_VOLTAGE_MV].to_numpy(dtype=np.float64)
            if len(t_arr) == 0:
                continue
            early_idx: int = int(np.argmin(np.abs(t_arr - decay_t_early_ms)))
            late_idx: int = int(np.argmin(np.abs(t_arr - decay_t_late_ms)))
            d_early: float = abs(float(v_arr[early_idx]) - baseline_mv)
            d_late: float = abs(float(v_arr[late_idx]) - baseline_mv)
            if d_early > 1e-6:
                ratios.append(d_late / d_early)
        out[int(angle_deg)] = float(np.mean(ratios)) if len(ratios) > 0 else None
    return out


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
    DSI / HWHM are only meaningful when peak_hz > 0; otherwise they are None.
    """
    metrics: dict[str, float | None] = {}
    peak_hz: float = float(compute_peak_hz(curve=curve))
    if peak_hz > 0.0:
        metrics[METRIC_KEY_DSI] = float(compute_dsi(curve=curve))
        metrics[METRIC_KEY_HWHM] = float(compute_hwhm_deg(curve=curve))
    else:
        metrics[METRIC_KEY_DSI] = None
        metrics[METRIC_KEY_HWHM] = None
    reliability: float | None = compute_reliability(curve=curve)
    metrics[METRIC_KEY_RELIABILITY] = float(reliability) if reliability is not None else None
    if mode == TrialMode.FULL:
        rmse: float | None = _compute_rmse_against_target(
            full_curve=curve,
            target_csv=target_csv,
        )
        metrics[METRIC_KEY_RMSE] = rmse
    else:
        metrics[METRIC_KEY_RMSE] = None
    return metrics


def _variant_label(*, gampa_ns: float, gaba_base_ns: float, mode: TrialMode) -> str:
    return f"gAMPA={gampa_ns:.2f}/GABA={gaba_base_ns:.2f}/{mode.value.upper()}"


def _variant_id(*, gampa_ns: float, gaba_base_ns: float, mode: TrialMode) -> str:
    # Variant ids use lowercase letters/digits/dots/underscores per the metrics spec.
    return f"gampa_{gampa_ns:.2f}_gaba_{gaba_base_ns:.2f}_{mode.value}"


def _all_curve_keys() -> Iterable[CurveKey]:
    for gampa_ns in AMPA_PEAK_NS_VALUES:
        for gaba_base_ns in GABA_BASE_NS_VALUES:
            for mode in (TrialMode.FULL, TrialMode.EPSP_PASSIVE, TrialMode.IPSP_PASSIVE):
                yield CurveKey(gampa_ns=gampa_ns, gaba_base_ns=gaba_base_ns, mode=mode)


def _curve_csv_for_mode(*, mode: TrialMode) -> Path:
    if mode == TrialMode.FULL:
        return TUNING_CURVE_FULL_CSV
    if mode == TrialMode.EPSP_PASSIVE:
        return TUNING_CURVE_EPSP_PASSIVE_CSV
    if mode == TrialMode.IPSP_PASSIVE:
        return TUNING_CURVE_IPSP_PASSIVE_CSV
    raise AssertionError(f"Unhandled mode: {mode}")


def _load_active_fraction_per_direction(*, csv_path: Path) -> dict[int, float]:
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Active-fraction CSV not found at {csv_path}; did the sweep run?",
        )
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=csv_path)
    return {int(row[COL_ANGLE_DEG]): float(row[COL_ACTIVE_FRACTION]) for _, row in df.iterrows()}


def _check_epsp_passive_peak_vm_gate() -> None:
    """REQ-15: max EPSP_PASSIVE Vm must be < EPSP_PASSIVE_PEAK_VM_GATE_MV (above E_AMPA = 0 mV)."""
    print("[metrics] Running EPSP_PASSIVE peak-Vm gate (REQ-15)...", flush=True)
    if not VOLTAGE_TRACES_EPSP_PASSIVE_CSV.exists():
        print(
            f"[metrics] Skipping EPSP_PASSIVE peak-Vm gate: "
            f"{VOLTAGE_TRACES_EPSP_PASSIVE_CSV} does not exist.",
            flush=True,
        )
        return
    for gampa_ns in AMPA_PEAK_NS_VALUES:
        for gaba_base_ns in GABA_BASE_NS_VALUES:
            peak_vm: float = _peak_vm_overall(
                voltage_csv=VOLTAGE_TRACES_EPSP_PASSIVE_CSV,
                gampa_ns=gampa_ns,
                gaba_base_ns=gaba_base_ns,
            )
            if peak_vm > EPSP_PASSIVE_PEAK_VM_GATE_MV:
                raise RuntimeError(
                    f"REQ-15 gate failed: gampa_ns={gampa_ns:.2f}, "
                    f"gaba_base_ns={gaba_base_ns:.2f}, EPSP_PASSIVE peak Vm = {peak_vm:.2f} mV "
                    f"exceeds EPSP_PASSIVE_PEAK_VM_GATE_MV = "
                    f"{EPSP_PASSIVE_PEAK_VM_GATE_MV:.2f} mV. The HH save-and-zero is wired "
                    f"incorrectly.",
                )
    print(
        "[metrics] REQ-15 gate PASSED: all EPSP_PASSIVE peak Vm < EPSP_PASSIVE_PEAK_VM_GATE_MV.",
        flush=True,
    )


def main() -> int:
    print("[metrics] Loading per-(gampa, gaba, mode) tuning curves...", flush=True)
    curves_by_key: dict[CurveKey, TuningCurve] = {}
    for key in _all_curve_keys():
        curves_by_key[key] = _load_tuning_curve_for_cell(
            csv_path=_curve_csv_for_mode(mode=key.mode),
            gampa_ns=key.gampa_ns,
            gaba_base_ns=key.gaba_base_ns,
        )

    # ----------------------------------------------------------------
    # REQ-15: EPSP_PASSIVE peak-Vm gate.
    # ----------------------------------------------------------------
    _check_epsp_passive_peak_vm_gate()

    # ----------------------------------------------------------------
    # Active-fraction sanity check (carried over from t0057; conductance-independent).
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
    # Build the 75-variant metrics.json payload.
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
                "variant_id": _variant_id(
                    gampa_ns=key.gampa_ns,
                    gaba_base_ns=key.gaba_base_ns,
                    mode=key.mode,
                ),
                "label": _variant_label(
                    gampa_ns=key.gampa_ns,
                    gaba_base_ns=key.gaba_base_ns,
                    mode=key.mode,
                ),
                "dimensions": {
                    "mode": key.mode.value,
                    "gampa_ns": float(key.gampa_ns),
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
    # Cross-grid derived quantities.
    # ----------------------------------------------------------------
    per_variant_quantities: dict[str, dict[str, float | None]] = {}
    for key in _all_curve_keys():
        variant_id: str = _variant_id(
            gampa_ns=key.gampa_ns,
            gaba_base_ns=key.gaba_base_ns,
            mode=key.mode,
        )
        curve = curves_by_key[key]
        peak_hz: float = float(compute_peak_hz(curve=curve))
        per_variant_quantities[variant_id] = {
            "peak_hz": peak_hz,
            "null_hz": float(compute_null_hz(curve=curve)),
            "vector_sum_dsi": float(compute_vector_sum_dsi(curve=curve)),
            "preferred_direction_deg": float(compute_preferred_direction_deg(curve=curve)),
        }

    # FULL-mode 5x5 grids (the cross-grid heatmap data).
    gampa_axis: list[float] = list(AMPA_PEAK_NS_VALUES)
    gaba_axis: list[float] = list(GABA_BASE_NS_VALUES)
    n_g: int = len(gampa_axis)
    n_b: int = len(gaba_axis)

    peak_hz_grid: list[list[float]] = [[0.0 for _ in range(n_b)] for _ in range(n_g)]
    null_hz_grid: list[list[float]] = [[0.0 for _ in range(n_b)] for _ in range(n_g)]
    dsi_primary_grid: list[list[float | None]] = [[None for _ in range(n_b)] for _ in range(n_g)]
    dsi_vector_sum_grid: list[list[float]] = [[0.0 for _ in range(n_b)] for _ in range(n_g)]
    hwhm_grid: list[list[float | None]] = [[None for _ in range(n_b)] for _ in range(n_g)]
    rmse_grid: list[list[float | None]] = [[None for _ in range(n_b)] for _ in range(n_g)]
    for i, gampa_ns in enumerate(gampa_axis):
        for j, gaba_base_ns in enumerate(gaba_axis):
            full_key = CurveKey(
                gampa_ns=gampa_ns,
                gaba_base_ns=gaba_base_ns,
                mode=TrialMode.FULL,
            )
            full_curve = curves_by_key[full_key]
            peak_hz_full: float = float(compute_peak_hz(curve=full_curve))
            peak_hz_grid[i][j] = peak_hz_full
            null_hz_grid[i][j] = float(compute_null_hz(curve=full_curve))
            dsi_vector_sum_grid[i][j] = float(compute_vector_sum_dsi(curve=full_curve))
            if peak_hz_full > 0.0:
                dsi_primary_grid[i][j] = float(compute_dsi(curve=full_curve))
                hwhm_grid[i][j] = float(compute_hwhm_deg(curve=full_curve))
            rmse_grid[i][j] = _compute_rmse_against_target(
                full_curve=full_curve,
                target_csv=TARGET_TUNING_CURVE_CSV,
            )

    # EPSP-decay grid per (gampa, gaba, angle).
    epsp_decay_grid: dict[str, dict[str, dict[int, float | None]]] = {}
    if VOLTAGE_TRACES_EPSP_PASSIVE_CSV.exists():
        for gampa_ns in AMPA_PEAK_NS_VALUES:
            sub_g: dict[str, dict[int, float | None]] = {}
            for gaba_base_ns in GABA_BASE_NS_VALUES:
                sub_g[f"gaba_{gaba_base_ns:.2f}"] = _epsp_decay_per_angle(
                    voltage_csv=VOLTAGE_TRACES_EPSP_PASSIVE_CSV,
                    gampa_ns=gampa_ns,
                    gaba_base_ns=gaba_base_ns,
                )
            epsp_decay_grid[f"gampa_{gampa_ns:.2f}"] = sub_g

    # Aggregate EPSP / IPSP envelopes per (gampa, gaba, direction).
    aggregate_epsp: dict[str, dict[str, dict[str, float]]] = {}
    aggregate_ipsp: dict[str, dict[str, dict[str, float]]] = {}
    if VOLTAGE_TRACES_EPSP_PASSIVE_CSV.exists():
        for gampa_ns in AMPA_PEAK_NS_VALUES:
            sub_g_eps: dict[str, dict[str, float]] = {}
            for gaba_base_ns in GABA_BASE_NS_VALUES:
                eps_per_angle: dict[int, float] = _peak_depolarization_per_angle(
                    voltage_csv=VOLTAGE_TRACES_EPSP_PASSIVE_CSV,
                    gampa_ns=gampa_ns,
                    gaba_base_ns=gaba_base_ns,
                )
                sub_g_eps[f"gaba_{gaba_base_ns:.2f}"] = {
                    f"angle_{a:03d}": float(v) for a, v in sorted(eps_per_angle.items())
                }
            aggregate_epsp[f"gampa_{gampa_ns:.2f}"] = sub_g_eps
    if VOLTAGE_TRACES_IPSP_PASSIVE_CSV.exists():
        for gampa_ns in AMPA_PEAK_NS_VALUES:
            sub_g_ips: dict[str, dict[str, float]] = {}
            for gaba_base_ns in GABA_BASE_NS_VALUES:
                ips_per_angle: dict[int, float] = _peak_depolarization_per_angle(
                    voltage_csv=VOLTAGE_TRACES_IPSP_PASSIVE_CSV,
                    gampa_ns=gampa_ns,
                    gaba_base_ns=gaba_base_ns,
                )
                sub_g_ips[f"gaba_{gaba_base_ns:.2f}"] = {
                    f"angle_{a:03d}": float(v) for a, v in sorted(ips_per_angle.items())
                }
            aggregate_ipsp[f"gampa_{gampa_ns:.2f}"] = sub_g_ips

    active_fraction_block: dict[str, float] = {
        f"angle_{angle:03d}": float(value)
        for angle, value in sorted(active_fraction_per_direction.items())
    }

    derived: dict[str, object] = {
        "ampa_peak_ns_values": gampa_axis,
        "gaba_base_ns_values": gaba_axis,
        "peak_hz_grid": peak_hz_grid,
        "null_hz_grid": null_hz_grid,
        "dsi_primary_grid": dsi_primary_grid,
        "dsi_vector_sum_grid": dsi_vector_sum_grid,
        "hwhm_grid": hwhm_grid,
        "rmse_grid": rmse_grid,
        "active_fraction_per_direction": active_fraction_block,
        "mean_active_fraction": mean_active_fraction,
        "active_fraction_soft_lower": ACTIVE_FRACTION_LOWER,
        "active_fraction_soft_upper": ACTIVE_FRACTION_UPPER,
        "active_fraction_soft_pass": (
            ACTIVE_FRACTION_LOWER <= mean_active_fraction <= ACTIVE_FRACTION_UPPER
        ),
        "epsp_decay_grid": epsp_decay_grid,
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
