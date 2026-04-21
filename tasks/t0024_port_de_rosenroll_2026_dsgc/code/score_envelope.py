"""Score t0024 DSGC tuning curves against the t0004 envelope.

Wraps the ``tuning_curve_loss`` library (t0012) to compute DSI, peak, null,
HWHM, reliability, and RMSE for the four tuning-curve CSVs produced by
``run_tuning_curve.py``. Results are written to:

* ``data/score_report.json`` — full 13-field ScoreReport for the 12-angle
  correlated sweep (the one comparable to the t0004 target grid).
* ``results/metrics.json`` — the four registered metric keys from the t0012
  library plus the task-local per-condition DSI/peak keys and the
  port-fidelity gate boolean (plan REQ-5).

The port-fidelity gate (plan step 13) is implemented here as well:

* DSI (correlated, 8-dir) in [0.30, 0.50]
* DSI (uncorrelated, 8-dir) in [0.18, 0.35]
* DSI drop from correlated -> uncorrelated >= 20% of the correlated value

If the gate fails, an intervention file is written at
``intervention/port_fidelity_miss.md``.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.loader import (
    TuningCurve,
    load_tuning_curve,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.scoring import (
    METRIC_KEY_DSI,
    METRIC_KEY_HWHM,
    METRIC_KEY_RELIABILITY,
    METRIC_KEY_RMSE,
    ScoreReport,
    score_curves,
)
from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C
from tasks.t0024_port_de_rosenroll_2026_dsgc.code import paths as P

# CSV column names used by run_tuning_curve.py output.
TRIAL_COL: str = "trial"
DIRECTION_COL: str = "direction_deg"
SPIKE_COUNT_COL: str = "spike_count"
PEAK_COL: str = "peak_mv"

# Scoring-library column names.
ANGLE_COL_OUT: str = "angle_deg"
TRIAL_SEED_COL_OUT: str = "trial_seed"
FIRING_RATE_COL_OUT: str = "firing_rate_hz"


@dataclass(frozen=True, slots=True)
class ConditionMetrics:
    """Compact metric bundle for one sweep condition."""

    dsi: float
    peak_hz: float
    null_hz: float
    hwhm_deg: float
    reliability: float


def _tuning_curve_from_raw_csv(*, csv_path: Path) -> TuningCurve:
    """Load a run_tuning_curve.py CSV and convert to the scoring-library schema.

    ``spike_count`` is divided by the simulated duration in seconds
    (``TSTOP_MS / 1000``) to produce a firing rate in Hz.
    """
    df_raw = pd.read_csv(filepath_or_buffer=csv_path)
    duration_s = C.TSTOP_MS / 1000.0
    df_out = pd.DataFrame(
        {
            ANGLE_COL_OUT: df_raw[DIRECTION_COL].astype(float),
            TRIAL_SEED_COL_OUT: df_raw[TRIAL_COL].astype(int),
            FIRING_RATE_COL_OUT: df_raw[SPIKE_COUNT_COL].astype(float) / duration_s,
        }
    )
    tmp_path = csv_path.with_suffix(".canonical.csv")
    df_out.to_csv(path_or_buf=tmp_path, index=False)
    try:
        return load_tuning_curve(csv_path=tmp_path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def _compute_condition_metrics(*, curve: TuningCurve) -> ConditionMetrics:
    """Compute DSI / peak / null / HWHM / reliability without doing a full comparison."""
    # Reuse the library's internals by calling score_curves with target=candidate.
    report: ScoreReport = score_curves(target=curve, candidate=curve)
    return ConditionMetrics(
        dsi=report.candidate_metrics.dsi,
        peak_hz=report.candidate_metrics.peak_hz,
        null_hz=report.candidate_metrics.null_hz,
        hwhm_deg=report.candidate_metrics.hwhm_deg,
        reliability=report.reliability,
    )


def _dsi_from_8dir(*, csv_path: Path) -> ConditionMetrics:
    """DSI/peak/null/HWHM from an 8-direction CSV (not on the 12-angle grid).

    The t0012 loader requires 12 angles with 30 deg spacing, so for 8-dir
    data we compute DSI directly (peak-null / peak+null at the min-max angles)
    rather than routing through the library.
    """
    df = pd.read_csv(filepath_or_buffer=csv_path)
    duration_s = C.TSTOP_MS / 1000.0
    df["firing_rate_hz"] = df[SPIKE_COUNT_COL].astype(float) / duration_s
    per_angle = df.groupby(by=DIRECTION_COL)["firing_rate_hz"].mean()
    rates = per_angle.to_numpy(dtype=np.float64)
    angles = per_angle.index.to_numpy(dtype=np.float64)

    peak_idx = int(np.argmax(rates))
    peak_hz = float(rates[peak_idx])
    peak_angle = float(angles[peak_idx])
    null_angle = (peak_angle + 180.0) % 360.0
    null_rate_candidates = rates[np.isclose(angles, null_angle)]
    if null_rate_candidates.size == 0:
        # Fall back to the minimum rate (shouldn't happen for 8-dir / 12-ang grids).
        null_hz = float(np.min(rates))
    else:
        null_hz = float(null_rate_candidates[0])

    dsi = 0.0 if (peak_hz + null_hz) == 0 else (peak_hz - null_hz) / (peak_hz + null_hz)

    # Reliability: for 8-dir we compute split-half per angle across trials.
    per_trial_list: list[np.ndarray] = []
    for _, grp in df.groupby(by=DIRECTION_COL):
        per_trial_list.append(grp["firing_rate_hz"].to_numpy(dtype=np.float64))
    trial_counts = {arr.size for arr in per_trial_list}
    if len(trial_counts) == 1 and per_trial_list[0].size > 1:
        trials_mat = np.stack(per_trial_list, axis=0)  # (n_angles, n_trials)
        half = trials_mat.shape[1] // 2
        a_mean = trials_mat[:, :half].mean(axis=1)
        b_mean = trials_mat[:, half : 2 * half].mean(axis=1)
        with np.errstate(invalid="ignore"):
            corr = np.corrcoef(a_mean, b_mean)
        reliability = float(corr[0, 1]) if np.isfinite(corr[0, 1]) else 0.0
    else:
        reliability = 1.0

    return ConditionMetrics(
        dsi=float(dsi),
        peak_hz=peak_hz,
        null_hz=null_hz,
        hwhm_deg=float("nan"),  # HWHM not straightforward at 8 angles
        reliability=reliability,
    )


def _evaluate_port_fidelity_gate(
    *,
    dsi_corr_8dir: float,
    dsi_uncorr_8dir: float,
) -> tuple[bool, str]:
    """Check the REQ-5 port-fidelity gate. Returns ``(passes, report_text)``."""
    corr_ok = C.PORT_FIDELITY_DSI_CORR_MIN <= dsi_corr_8dir <= C.PORT_FIDELITY_DSI_CORR_MAX
    uncorr_ok = C.PORT_FIDELITY_DSI_UNCORR_MIN <= dsi_uncorr_8dir <= C.PORT_FIDELITY_DSI_UNCORR_MAX
    if dsi_corr_8dir > 0.0:
        drop_frac = max(0.0, (dsi_corr_8dir - dsi_uncorr_8dir) / dsi_corr_8dir)
    else:
        drop_frac = 0.0
    drop_ok = drop_frac >= C.PORT_FIDELITY_DSI_DROP_MIN_FRAC

    all_pass = bool(corr_ok and uncorr_ok and drop_ok)
    lines: list[str] = []
    lines.append(
        f"- corr DSI    = {dsi_corr_8dir:.3f}"
        f"  required [{C.PORT_FIDELITY_DSI_CORR_MIN}, "
        f"{C.PORT_FIDELITY_DSI_CORR_MAX}]  -> "
        f"{'PASS' if corr_ok else 'FAIL'}"
    )
    lines.append(
        f"- uncorr DSI  = {dsi_uncorr_8dir:.3f}"
        f"  required [{C.PORT_FIDELITY_DSI_UNCORR_MIN}, "
        f"{C.PORT_FIDELITY_DSI_UNCORR_MAX}]  -> "
        f"{'PASS' if uncorr_ok else 'FAIL'}"
    )
    lines.append(
        f"- drop frac   = {drop_frac:.3f}"
        f"  required >= {C.PORT_FIDELITY_DSI_DROP_MIN_FRAC}  -> "
        f"{'PASS' if drop_ok else 'FAIL'}"
    )
    return all_pass, "\n".join(lines)


def _write_intervention(*, report_text: str, dsi_corr: float, dsi_uncorr: float) -> None:
    P.INTERVENTION_DIR.mkdir(parents=True, exist_ok=True)
    body = f"""# Port Fidelity Gate: MISS

The de Rosenroll 2026 DSGC port did not meet the REQ-5 port-fidelity gate.
This is a first-class finding per plan step 13, not a blocking error.

## Gate checks

{report_text}

## Measured values

- DSI (correlated, 8-dir)   = {dsi_corr:.4f}
- DSI (uncorrelated, 8-dir) = {dsi_uncorr:.4f}

## Interpretation

The simplified port (ACh/GABA Exp2Syn pairs per terminal with AR(2)-modulated
Poisson release and a null-biased GABA release probability, no full SAC
varicosity network) captures the asymmetric-inhibition mechanism but does
not perfectly reproduce the paper's absolute DSI magnitudes. Follow-up
tasks can port the full ``SacNetwork`` (``bp_locs``, ``probs``, ``deltas``)
to close the gap.
"""
    P.PORT_FIDELITY_MISS_MD.write_text(body, encoding="utf-8")
    print(f"wrote intervention file -> {P.PORT_FIDELITY_MISS_MD}")


def main() -> int:
    # --- 12-angle correlated: full scoring against t0004 target ---
    if not P.TUNING_CURVE_12ANG_CORR_CSV.exists():
        raise FileNotFoundError(
            f"Missing 12-angle correlated sweep: {P.TUNING_CURVE_12ANG_CORR_CSV}"
        )
    candidate_12ang = _tuning_curve_from_raw_csv(
        csv_path=P.TUNING_CURVE_12ANG_CORR_CSV,
    )
    from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.paths import (
        TARGET_MEAN_CSV,
    )

    target = load_tuning_curve(csv_path=TARGET_MEAN_CSV)
    report: ScoreReport = score_curves(target=target, candidate=candidate_12ang)

    # --- Per-condition metrics (all four sweeps) ---
    corr_8dir_metrics = _dsi_from_8dir(csv_path=P.TUNING_CURVE_8DIR_CORR_CSV)
    uncorr_8dir_metrics = _dsi_from_8dir(csv_path=P.TUNING_CURVE_8DIR_UNCORR_CSV)
    uncorr_12ang_curve = _tuning_curve_from_raw_csv(
        csv_path=P.TUNING_CURVE_12ANG_UNCORR_CSV,
    )
    uncorr_12ang_metrics = _compute_condition_metrics(curve=uncorr_12ang_curve)

    # --- Port-fidelity gate ---
    gate_pass, gate_text = _evaluate_port_fidelity_gate(
        dsi_corr_8dir=corr_8dir_metrics.dsi,
        dsi_uncorr_8dir=uncorr_8dir_metrics.dsi,
    )
    print("=== Port-fidelity gate ===")
    print(gate_text)
    print(f"=> {'PASS' if gate_pass else 'FAIL'}")
    if not gate_pass:
        _write_intervention(
            report_text=gate_text,
            dsi_corr=corr_8dir_metrics.dsi,
            dsi_uncorr=uncorr_8dir_metrics.dsi,
        )

    # --- Write data/score_report.json ---
    P.DATA_DIR.mkdir(parents=True, exist_ok=True)
    score_dump = {
        "loss_scalar": report.loss_scalar,
        "dsi_residual": report.dsi_residual,
        "peak_residual_hz": report.peak_residual_hz,
        "null_residual_hz": report.null_residual_hz,
        "hwhm_residual_deg": report.hwhm_residual_deg,
        "rmse_vs_target": report.rmse_vs_target,
        "reliability": report.reliability,
        "passes_envelope": report.passes_envelope,
        "per_target_pass": report.per_target_pass,
        "residuals": report.residuals,
        "normalized_residuals": report.normalized_residuals,
        "weights_used": report.weights_used,
        "candidate_metrics": {
            "dsi": report.candidate_metrics.dsi,
            "peak_hz": report.candidate_metrics.peak_hz,
            "null_hz": report.candidate_metrics.null_hz,
            "hwhm_deg": report.candidate_metrics.hwhm_deg,
            "reliability": report.candidate_metrics.reliability,
        },
        "target_metrics": {
            "dsi": report.target_metrics.dsi,
            "peak_hz": report.target_metrics.peak_hz,
            "null_hz": report.target_metrics.null_hz,
            "hwhm_deg": report.target_metrics.hwhm_deg,
            "reliability": report.target_metrics.reliability,
        },
    }
    P.SCORE_REPORT_JSON.write_text(
        json.dumps(score_dump, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote score report -> {P.SCORE_REPORT_JSON}")

    # --- Write results/metrics.json ---
    P.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    metrics: dict[str, float | bool | None] = {
        METRIC_KEY_DSI: report.candidate_metrics.dsi,
        METRIC_KEY_HWHM: report.candidate_metrics.hwhm_deg,
        METRIC_KEY_RELIABILITY: report.reliability,
        METRIC_KEY_RMSE: report.rmse_vs_target,
        C.METRIC_KEY_DSI_CORR_8DIR: corr_8dir_metrics.dsi,
        C.METRIC_KEY_DSI_UNCORR_8DIR: uncorr_8dir_metrics.dsi,
        C.METRIC_KEY_DSI_CORR_12ANG: report.candidate_metrics.dsi,
        C.METRIC_KEY_DSI_UNCORR_12ANG: uncorr_12ang_metrics.dsi,
        C.METRIC_KEY_PEAK_CORR_8DIR: corr_8dir_metrics.peak_hz,
        C.METRIC_KEY_PEAK_UNCORR_8DIR: uncorr_8dir_metrics.peak_hz,
        C.METRIC_KEY_PORT_FIDELITY_PASS: gate_pass,
    }
    P.METRICS_JSON.write_text(
        json.dumps(metrics, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote metrics -> {P.METRICS_JSON}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
