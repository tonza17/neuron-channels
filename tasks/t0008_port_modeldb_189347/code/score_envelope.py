"""Score the 12-angle tuning curve against the t0004 target envelope.

Reads ``data/tuning_curves/curve_modeldb_189347.csv`` (emitted by
``run_tuning_curve.py``), calls the t0012 ``tuning_curve_loss.score``
function against the canonical t0004 target curve, and writes:

  * ``data/score_report.json``  — full ScoreReport dump for debugging
  * ``results/metrics.json``    — the four registered metric keys

The four registered keys are owned by the metrics registered under
``meta/metrics/`` and documented in t0012 scoring.py:

  * ``direction_selectivity_index``
  * ``tuning_curve_hwhm_deg``
  * ``tuning_curve_reliability``
  * ``tuning_curve_rmse``
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict

from tasks.t0008_port_modeldb_189347.code.paths import (
    DATA_DIR,
    METRICS_JSON,
    RESULTS_DIR,
    SCORE_REPORT_JSON,
    TUNING_CURVE_MODELDB_CSV,
)
from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (
    METRIC_KEY_DSI,
    METRIC_KEY_HWHM,
    METRIC_KEY_RELIABILITY,
    METRIC_KEY_RMSE,
    score,
)


def main() -> int:
    if not TUNING_CURVE_MODELDB_CSV.exists():
        print(f"ERROR: tuning curve CSV missing at {TUNING_CURVE_MODELDB_CSV}")
        return 1

    print(f"Scoring {TUNING_CURVE_MODELDB_CSV} vs canonical t0004 target...", flush=True)
    report = score(simulated_curve_csv=TUNING_CURVE_MODELDB_CSV)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Dump full report to data/ for debugging (ScoreReport is a frozen
    # slotted dataclass with nested dataclass fields; asdict recurses).
    full_dump = {
        "loss_scalar": report.loss_scalar,
        "dsi_residual": report.dsi_residual,
        "peak_residual_hz": report.peak_residual_hz,
        "null_residual_hz": report.null_residual_hz,
        "hwhm_residual_deg": report.hwhm_residual_deg,
        "rmse_vs_target": report.rmse_vs_target,
        "reliability": report.reliability,
        "passes_envelope": report.passes_envelope,
        "per_target_pass": dict(report.per_target_pass),
        "residuals": dict(report.residuals),
        "normalized_residuals": dict(report.normalized_residuals),
        "weights_used": dict(report.weights_used),
        "candidate_metrics": asdict(report.candidate_metrics),
        "target_metrics": asdict(report.target_metrics),
        "half_widths_used": dict(report.half_widths_used),
    }
    SCORE_REPORT_JSON.write_text(json.dumps(full_dump, indent=2) + "\n", encoding="utf-8")
    print(f"  wrote {SCORE_REPORT_JSON}", flush=True)

    # Results metrics.json — registered keys only.
    metrics_payload: dict[str, float | None] = {
        METRIC_KEY_DSI: report.candidate_metrics.dsi,
        METRIC_KEY_HWHM: report.candidate_metrics.hwhm_deg,
        METRIC_KEY_RELIABILITY: report.reliability,
        METRIC_KEY_RMSE: report.rmse_vs_target,
    }
    METRICS_JSON.write_text(json.dumps(metrics_payload, indent=2) + "\n", encoding="utf-8")
    print(f"  wrote {METRICS_JSON}", flush=True)

    print(
        "\nSummary:\n"
        f"  candidate DSI           = {report.candidate_metrics.dsi:.3f}\n"
        f"  candidate peak (Hz)     = {report.candidate_metrics.peak_hz:.2f}\n"
        f"  candidate null (Hz)     = {report.candidate_metrics.null_hz:.2f}\n"
        f"  candidate HWHM (deg)    = {report.candidate_metrics.hwhm_deg:.2f}\n"
        f"  reliability             = {report.reliability:.3f}\n"
        f"  RMSE vs target (Hz)     = "
        f"{'n/a' if report.rmse_vs_target is None else f'{report.rmse_vs_target:.3f}'}\n"
        f"  loss_scalar             = {report.loss_scalar:.3f}\n"
        f"  passes_envelope         = {report.passes_envelope}\n",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
