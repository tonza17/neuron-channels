"""Stage 5: compute width metrics for all 25 conditions.

Reads ``results/data/per_trial_full.csv``. For each condition:
  * Aggregates per-trial firing rates into the canonical t0012 schema and writes
    one CSV per condition under ``results/data/tuning_curves/<condition_id>.csv``.
  * Concatenates all 25 into ``results/data/tuning_curves.csv``.
  * Computes peak / null / DSI_PD-ND / HWHM (gated on peak >= 1 Hz) / vector-sum
    DSI / RMSE vs t0004 / split-half reliability.
  * Computes deltas vs baseline and the ``is_inert`` flag.
  * Writes ``results/metrics_summary.csv`` (25 rows) and ``results/metrics.json``
    in the explicit-variants format with one variant per condition.
"""

from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.loader import (
    TuningCurve,
    load_tuning_curve,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics import (
    compute_dsi,
    compute_hwhm_deg,
    compute_null_hz,
    compute_peak_hz,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.scoring import (
    score,
)
from tasks.t0074_channel_tuning_width_bed_a.code.constants import (
    BASELINE_CONDITION_ID,
    CHANNEL_DEFS,
    COL_ANGLE_DEG,
    COL_BASELINE_VM_MV,
    COL_CHANNEL_KIND,
    COL_CONDITION_ID,
    COL_DELTA_HWHM_DEG,
    COL_DELTA_VECTOR_SUM_DSI,
    COL_DENSITY_LABEL,
    COL_DENSITY_MS_CM2,
    COL_DSI_PD_ND,
    COL_FIRING_RATE_HZ,
    COL_HWHM_DEG,
    COL_IS_INERT,
    COL_IS_UNSTABLE,
    COL_N_SPIKES,
    COL_NULL_HZ,
    COL_PD_ANGLE_DEG,
    COL_PEAK_HZ,
    COL_PEAK_VM_MV,
    COL_RATE_AT_ND_HZ,
    COL_RATE_AT_PD_HZ,
    COL_RMSE_VS_T0004,
    COL_TC_ANGLE_DEG,
    COL_TC_FIRING_RATE_HZ,
    COL_TC_TRIAL_SEED,
    COL_TRIAL_MODE,
    COL_TRIAL_SEED,
    COL_TUNING_CURVE_RELIABILITY,
    COL_VECTOR_SUM_DSI,
    DELTA_HWHM_THRESHOLD_DEG,
    DELTA_VECTOR_SUM_DSI_THRESHOLD,
    LOW_RATE_HZ_THRESHOLD,
    METRIC_KEY_DSI,
    METRIC_KEY_HWHM,
    METRIC_KEY_RELIABILITY,
    METRIC_KEY_RMSE,
    N_ANGLES,
    ChannelDef,
    ChannelKind,
    DensityLabel,
    TrialMode,
)
from tasks.t0074_channel_tuning_width_bed_a.code.paths import (
    DATA_DIR,
    METRICS_JSON,
    METRICS_SUMMARY_CSV,
    PER_TRIAL_FULL_CSV,
    RESULTS_DIR,
    T0004_TARGET_CSV,
    TUNING_CURVES_CSV,
    TUNING_CURVES_DIR,
)


@dataclass(frozen=True, slots=True)
class ConditionMetrics:
    condition_id: str
    channel_kind: str
    density_label: str
    density_mS_cm2: float
    peak_hz: float
    null_hz: float
    dsi_pd_nd: float
    hwhm_deg: float | None
    vector_sum_dsi: float
    pd_angle_deg: float
    rate_at_pd_hz: float
    rate_at_nd_hz: float
    rmse_vs_t0004: float | None
    tuning_curve_reliability: float | None
    delta_hwhm_deg: float | None
    delta_vector_sum_dsi: float


@dataclass(frozen=True, slots=True)
class ChannelInertness:
    channel_kind: ChannelKind
    is_inert: bool


PER_TRIAL_DTYPES: dict[str, Any] = {
    COL_CONDITION_ID: pd.StringDtype(),
    COL_CHANNEL_KIND: pd.StringDtype(),
    COL_DENSITY_LABEL: pd.StringDtype(),
    COL_DENSITY_MS_CM2: np.dtype("float64"),
    COL_ANGLE_DEG: np.dtype("float64"),
    COL_TRIAL_SEED: pd.Int64Dtype(),
    COL_TRIAL_MODE: pd.StringDtype(),
    COL_N_SPIKES: pd.Int64Dtype(),
    COL_FIRING_RATE_HZ: np.dtype("float64"),
    COL_PEAK_VM_MV: np.dtype("float64"),
    COL_BASELINE_VM_MV: np.dtype("float64"),
    COL_IS_UNSTABLE: pd.BooleanDtype(),
}


def _load_per_trial_full() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(
        filepath_or_buffer=PER_TRIAL_FULL_CSV,
        dtype=PER_TRIAL_DTYPES,
    )
    full_only: pd.DataFrame = df[df[COL_TRIAL_MODE] == TrialMode.FULL.value].copy()
    return full_only


def _channel_def_for_kind(kind: ChannelKind) -> ChannelDef:
    for ch in CHANNEL_DEFS:
        if ch.kind == kind:
            return ch
    raise ValueError(f"Unknown channel kind: {kind}")


def _expected_condition_ids() -> list[str]:
    out: list[str] = [BASELINE_CONDITION_ID]
    for ch in CHANNEL_DEFS:
        short_kind: str = ch.kind.value.replace(".", "").lower()
        for label in (DensityLabel.LOW, DensityLabel.MED, DensityLabel.HIGH):
            out.append(f"{short_kind}_{label.value}")
    return out


def _write_condition_csv(*, df_condition: pd.DataFrame, csv_path: Path) -> None:
    """Write a per-condition CSV in canonical t0012 schema (sorted by angle, seed)."""
    df_out: pd.DataFrame = df_condition[[COL_ANGLE_DEG, COL_TRIAL_SEED, COL_FIRING_RATE_HZ]].copy()
    df_out = df_out.rename(
        columns={
            COL_ANGLE_DEG: COL_TC_ANGLE_DEG,
            COL_TRIAL_SEED: COL_TC_TRIAL_SEED,
            COL_FIRING_RATE_HZ: COL_TC_FIRING_RATE_HZ,
        },
    )
    df_out = df_out.sort_values(by=[COL_TC_ANGLE_DEG, COL_TC_TRIAL_SEED]).reset_index(drop=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(path_or_buf=csv_path, index=False)


def _load_curve(*, csv_path: Path) -> TuningCurve:
    return load_tuning_curve(csv_path=csv_path)


def _vector_sum_dsi_and_pd_angle(
    *,
    angles_deg: NDArray[np.float64],
    rates_hz: NDArray[np.float64],
) -> tuple[float, float]:
    """Return (vector_sum_dsi, pd_angle_deg). Vector-sum DSI = |sum r exp(i*theta)| / sum r."""
    if rates_hz.sum() <= 0.0:
        return 0.0, 0.0
    angles_rad: NDArray[np.float64] = np.deg2rad(angles_deg)
    complex_sum: complex = complex(np.sum(rates_hz * np.exp(1j * angles_rad)))
    magnitude: float = float(abs(complex_sum))
    pd_angle_rad: float = float(np.angle(complex_sum))
    pd_angle_deg: float = float(np.rad2deg(pd_angle_rad)) % 360.0
    vector_sum_dsi: float = magnitude / float(rates_hz.sum())
    return vector_sum_dsi, pd_angle_deg


def _rate_at_angle(
    *,
    angles_deg: NDArray[np.float64],
    rates_hz: NDArray[np.float64],
    target_angle_deg: float,
) -> float:
    """Return firing rate at the angle bin closest to ``target_angle_deg``."""
    target_mod: float = target_angle_deg % 360.0
    diffs: NDArray[np.float64] = np.minimum(
        np.abs(angles_deg - target_mod),
        360.0 - np.abs(angles_deg - target_mod),
    )
    idx: int = int(np.argmin(diffs))
    return float(rates_hz[idx])


def _compute_seed_pearson_reliability(*, df_condition: pd.DataFrame) -> float | None:
    """Pearson r averaged over all seed pairs, on per-seed firing-rate vectors."""
    pivot: pd.DataFrame = df_condition.pivot_table(
        index=COL_ANGLE_DEG,
        columns=COL_TRIAL_SEED,
        values=COL_FIRING_RATE_HZ,
        aggfunc="mean",
    )
    seeds: list[int] = sorted(int(s) for s in pivot.columns.tolist())
    if len(seeds) < 2:
        return None
    pivot = pivot[seeds].astype("float64")
    rs: list[float] = []
    for i in range(len(seeds)):
        for j in range(i + 1, len(seeds)):
            x: NDArray[np.float64] = pivot[seeds[i]].to_numpy(dtype=np.float64)
            y: NDArray[np.float64] = pivot[seeds[j]].to_numpy(dtype=np.float64)
            if x.std() == 0.0 or y.std() == 0.0:
                continue
            with np.errstate(invalid="ignore"):
                r: float = float(np.corrcoef(x, y)[0, 1])
            if np.isnan(r):
                continue
            rs.append(r)
    if len(rs) == 0:
        return None
    mean_r: float = float(np.mean(rs))
    return max(0.0, min(1.0, mean_r))


def _compute_condition_metrics(
    *,
    condition_id: str,
    df_condition: pd.DataFrame,
    csv_path: Path,
) -> ConditionMetrics:
    first_row: pd.Series = df_condition.iloc[0]
    channel_kind: str = str(first_row[COL_CHANNEL_KIND])
    density_label: str = str(first_row[COL_DENSITY_LABEL])
    density_mS_cm2: float = float(first_row[COL_DENSITY_MS_CM2])

    # Load via t0012 loader to get per-angle mean + per-seed trials matrix.
    curve: TuningCurve = _load_curve(csv_path=csv_path)
    angles_deg: NDArray[np.float64] = curve.angles_deg
    rates_hz: NDArray[np.float64] = curve.firing_rates_hz
    assert angles_deg.shape[0] == N_ANGLES, "expected 12-angle grid"

    peak_hz: float = compute_peak_hz(curve=curve)
    null_hz: float = compute_null_hz(curve=curve)
    dsi_pd_nd: float = compute_dsi(curve=curve)

    if peak_hz < LOW_RATE_HZ_THRESHOLD:
        hwhm_deg: float | None = None
    else:
        hwhm_deg = float(compute_hwhm_deg(curve=curve))

    vector_sum_dsi, pd_angle_deg = _vector_sum_dsi_and_pd_angle(
        angles_deg=angles_deg,
        rates_hz=rates_hz,
    )
    rate_at_pd_hz: float = _rate_at_angle(
        angles_deg=angles_deg,
        rates_hz=rates_hz,
        target_angle_deg=pd_angle_deg,
    )
    rate_at_nd_hz: float = _rate_at_angle(
        angles_deg=angles_deg,
        rates_hz=rates_hz,
        target_angle_deg=pd_angle_deg + 180.0,
    )

    rmse_vs_t0004: float | None
    try:
        score_report = score(
            simulated_curve_csv=csv_path,
            target_curve_csv=T0004_TARGET_CSV,
        )
        rmse_vs_t0004 = score_report.rmse_vs_target
    except (ValueError, FileNotFoundError) as exc:
        print(f"  WARNING: RMSE failed for {condition_id}: {exc}", flush=True)
        rmse_vs_t0004 = None

    reliability: float | None = _compute_seed_pearson_reliability(df_condition=df_condition)

    return ConditionMetrics(
        condition_id=condition_id,
        channel_kind=channel_kind,
        density_label=density_label,
        density_mS_cm2=density_mS_cm2,
        peak_hz=peak_hz,
        null_hz=null_hz,
        dsi_pd_nd=dsi_pd_nd,
        hwhm_deg=hwhm_deg,
        vector_sum_dsi=vector_sum_dsi,
        pd_angle_deg=pd_angle_deg,
        rate_at_pd_hz=rate_at_pd_hz,
        rate_at_nd_hz=rate_at_nd_hz,
        rmse_vs_t0004=rmse_vs_t0004,
        tuning_curve_reliability=reliability,
        delta_hwhm_deg=None,  # filled in after baseline known
        delta_vector_sum_dsi=0.0,
    )


def _write_metrics_summary_csv(*, metrics: list[ConditionMetrics]) -> None:
    METRICS_SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = [
        COL_CONDITION_ID,
        COL_CHANNEL_KIND,
        COL_DENSITY_LABEL,
        COL_DENSITY_MS_CM2,
        COL_PEAK_HZ,
        COL_NULL_HZ,
        COL_DSI_PD_ND,
        COL_HWHM_DEG,
        COL_VECTOR_SUM_DSI,
        COL_PD_ANGLE_DEG,
        COL_RATE_AT_PD_HZ,
        COL_RATE_AT_ND_HZ,
        COL_RMSE_VS_T0004,
        COL_TUNING_CURVE_RELIABILITY,
        COL_DELTA_HWHM_DEG,
        COL_DELTA_VECTOR_SUM_DSI,
        COL_IS_INERT,
    ]
    inert_flags: dict[str, bool] = _compute_is_inert_per_condition(metrics=metrics)
    with open(file=METRICS_SUMMARY_CSV, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for m in metrics:
            row: dict[str, Any] = {
                COL_CONDITION_ID: m.condition_id,
                COL_CHANNEL_KIND: m.channel_kind,
                COL_DENSITY_LABEL: m.density_label,
                COL_DENSITY_MS_CM2: m.density_mS_cm2,
                COL_PEAK_HZ: m.peak_hz,
                COL_NULL_HZ: m.null_hz,
                COL_DSI_PD_ND: m.dsi_pd_nd,
                COL_HWHM_DEG: "" if m.hwhm_deg is None else m.hwhm_deg,
                COL_VECTOR_SUM_DSI: m.vector_sum_dsi,
                COL_PD_ANGLE_DEG: m.pd_angle_deg,
                COL_RATE_AT_PD_HZ: m.rate_at_pd_hz,
                COL_RATE_AT_ND_HZ: m.rate_at_nd_hz,
                COL_RMSE_VS_T0004: "" if m.rmse_vs_t0004 is None else m.rmse_vs_t0004,
                COL_TUNING_CURVE_RELIABILITY: (
                    "" if m.tuning_curve_reliability is None else m.tuning_curve_reliability
                ),
                COL_DELTA_HWHM_DEG: "" if m.delta_hwhm_deg is None else m.delta_hwhm_deg,
                COL_DELTA_VECTOR_SUM_DSI: m.delta_vector_sum_dsi,
                COL_IS_INERT: inert_flags.get(m.condition_id, False),
            }
            writer.writerow(row)


def _compute_is_inert_per_condition(*, metrics: list[ConditionMetrics]) -> dict[str, bool]:
    """A condition row is ``is_inert`` if every density of its channel is non-meaningful.

    Condition is non-meaningful when ``|delta_hwhm_deg| <= threshold AND
    |delta_vector_sum_dsi| <= threshold``. The decision is per-channel: if any
    density of a given channel reaches the threshold, none of that channel's
    density rows are inert.
    """
    by_channel: dict[str, list[ConditionMetrics]] = {}
    for m in metrics:
        if m.condition_id == BASELINE_CONDITION_ID:
            continue
        by_channel.setdefault(m.channel_kind, []).append(m)

    is_inert: dict[str, bool] = {BASELINE_CONDITION_ID: False}
    for ms in by_channel.values():
        any_meaningful: bool = False
        for m in ms:
            dh: float = abs(m.delta_hwhm_deg) if m.delta_hwhm_deg is not None else 0.0
            dv: float = abs(m.delta_vector_sum_dsi)
            if dh > DELTA_HWHM_THRESHOLD_DEG or dv > DELTA_VECTOR_SUM_DSI_THRESHOLD:
                any_meaningful = True
                break
        for m in ms:
            is_inert[m.condition_id] = not any_meaningful
    return is_inert


def _write_metrics_json(*, metrics: list[ConditionMetrics]) -> None:
    METRICS_JSON.parent.mkdir(parents=True, exist_ok=True)
    variants: list[dict[str, Any]] = []
    for m in metrics:
        variants.append(
            {
                "variant_id": m.condition_id,
                "label": m.condition_id,
                "dimensions": {
                    "channel_kind": m.channel_kind,
                    "density_label": m.density_label,
                    "density_ms_cm2": m.density_mS_cm2,
                },
                "metrics": {
                    METRIC_KEY_DSI: m.dsi_pd_nd,
                    METRIC_KEY_HWHM: m.hwhm_deg,
                    METRIC_KEY_RELIABILITY: m.tuning_curve_reliability,
                    METRIC_KEY_RMSE: m.rmse_vs_t0004,
                },
            },
        )
    with open(file=METRICS_JSON, mode="w", encoding="utf-8") as f:
        json.dump({"variants": variants}, f, indent=2)


def _write_combined_tuning_curves(*, df_full: pd.DataFrame) -> None:
    df_out: pd.DataFrame = df_full[
        [COL_CONDITION_ID, COL_ANGLE_DEG, COL_TRIAL_SEED, COL_FIRING_RATE_HZ]
    ].copy()
    df_out = df_out.rename(
        columns={
            COL_ANGLE_DEG: COL_TC_ANGLE_DEG,
            COL_TRIAL_SEED: COL_TC_TRIAL_SEED,
            COL_FIRING_RATE_HZ: COL_TC_FIRING_RATE_HZ,
        },
    )
    df_out = df_out.sort_values(
        by=[COL_CONDITION_ID, COL_TC_ANGLE_DEG, COL_TC_TRIAL_SEED],
    ).reset_index(drop=True)
    TUNING_CURVES_CSV.parent.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(path_or_buf=TUNING_CURVES_CSV, index=False)


def _aggregate_to_per_angle_means(*, df_full: pd.DataFrame) -> pd.DataFrame:
    """Per-condition x angle x seed firing rate (mean across the trials at that
    condition/angle/seed; here each (condition, angle, seed) has 1 trial only)."""
    grouped: pd.DataFrame = df_full.groupby(
        by=[COL_CONDITION_ID, COL_ANGLE_DEG, COL_TRIAL_SEED],
        as_index=False,
    )[COL_FIRING_RATE_HZ].mean()
    return grouped


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TUNING_CURVES_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading {PER_TRIAL_FULL_CSV}...", flush=True)
    df_full: pd.DataFrame = _load_per_trial_full()
    df_full = _aggregate_to_per_angle_means(df_full=df_full)
    print(f"  {len(df_full)} (condition, angle, seed) rows", flush=True)

    expected_ids: list[str] = _expected_condition_ids()
    found_ids: list[str] = sorted(df_full[COL_CONDITION_ID].unique().tolist())
    missing: list[str] = [c for c in expected_ids if c not in found_ids]
    if len(missing) > 0:
        print(f"WARNING: missing condition IDs in per_trial_full.csv: {missing}", flush=True)

    metrics_list: list[ConditionMetrics] = []
    for condition_id in expected_ids:
        if condition_id not in found_ids:
            continue
        condition_csv: Path = TUNING_CURVES_DIR / f"{condition_id}.csv"
        df_cond_for_csv: pd.DataFrame = df_full[df_full[COL_CONDITION_ID] == condition_id].copy()
        # Reattach the channel kind / density columns so the per-trial join works.
        df_cond_full_meta: pd.DataFrame = df_full[df_full[COL_CONDITION_ID] == condition_id].merge(
            right=_load_per_trial_full()[
                [COL_CONDITION_ID, COL_CHANNEL_KIND, COL_DENSITY_LABEL, COL_DENSITY_MS_CM2]
            ].drop_duplicates(),
            on=COL_CONDITION_ID,
            how="left",
            validate="many_to_one",
        )
        _write_condition_csv(df_condition=df_cond_for_csv, csv_path=condition_csv)
        m: ConditionMetrics = _compute_condition_metrics(
            condition_id=condition_id,
            df_condition=df_cond_full_meta,
            csv_path=condition_csv,
        )
        metrics_list.append(m)
        print(
            f"  {condition_id:14s} peak={m.peak_hz:6.2f} Hz vec_DSI={m.vector_sum_dsi:5.3f} "
            f"hwhm={'NA' if m.hwhm_deg is None else f'{m.hwhm_deg:6.2f}'} deg",
            flush=True,
        )

    # Compute deltas vs baseline.
    baseline: ConditionMetrics | None = next(
        (m for m in metrics_list if m.condition_id == BASELINE_CONDITION_ID),
        None,
    )
    if baseline is None:
        raise RuntimeError("Baseline condition not found in metrics list")

    metrics_with_deltas: list[ConditionMetrics] = []
    for m in metrics_list:
        delta_hwhm: float | None
        if m.condition_id == BASELINE_CONDITION_ID:
            delta_hwhm = None if baseline.hwhm_deg is None else 0.0
        elif m.hwhm_deg is None or baseline.hwhm_deg is None:
            delta_hwhm = None
        else:
            delta_hwhm = m.hwhm_deg - baseline.hwhm_deg
        delta_vec: float = m.vector_sum_dsi - baseline.vector_sum_dsi
        metrics_with_deltas.append(
            ConditionMetrics(
                condition_id=m.condition_id,
                channel_kind=m.channel_kind,
                density_label=m.density_label,
                density_mS_cm2=m.density_mS_cm2,
                peak_hz=m.peak_hz,
                null_hz=m.null_hz,
                dsi_pd_nd=m.dsi_pd_nd,
                hwhm_deg=m.hwhm_deg,
                vector_sum_dsi=m.vector_sum_dsi,
                pd_angle_deg=m.pd_angle_deg,
                rate_at_pd_hz=m.rate_at_pd_hz,
                rate_at_nd_hz=m.rate_at_nd_hz,
                rmse_vs_t0004=m.rmse_vs_t0004,
                tuning_curve_reliability=m.tuning_curve_reliability,
                delta_hwhm_deg=delta_hwhm,
                delta_vector_sum_dsi=delta_vec,
            ),
        )

    print(f"\nWriting {METRICS_SUMMARY_CSV}...", flush=True)
    _write_metrics_summary_csv(metrics=metrics_with_deltas)

    print(f"Writing {METRICS_JSON}...", flush=True)
    _write_metrics_json(metrics=metrics_with_deltas)

    print(f"Writing {TUNING_CURVES_CSV}...", flush=True)
    _write_combined_tuning_curves(df_full=df_full)

    print(f"\nDone. {len(metrics_with_deltas)} conditions processed.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
