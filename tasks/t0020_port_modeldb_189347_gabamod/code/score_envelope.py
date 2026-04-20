"""Score the two-condition PD/ND gabaMOD sweep against the literature envelope.

Reads ``data/tuning_curves.csv`` (emitted by ``run_gabamod_sweep.py``),
computes ``DSI = (mean_PD - mean_ND) / (mean_PD + mean_ND)`` and
``peak = mean_PD`` inline, gates them against the unwidened literature
envelope from Poleg-Polsky & Diamond 2016 (DSI 0.70-0.85, peak 40-80 Hz),
and writes:

  * ``results/score_report.json`` — full ScoreReport (protocol metadata,
    means, DSI, peak, envelope thresholds, gate.passed).
  * ``results/metrics.json``      — the registered metric keys
    (``dsi``, ``peak_hz``, ``mean_pd_hz``, ``mean_nd_hz``, ``gate_passed``).

The t0012 high-level ``score()`` entry point cannot be used here — its
loader validates a 12-angle 30-degree grid, which the two-point PD/ND
schema does not satisfy. The formula is identical to t0012's internal
``compute_dsi``; the envelope is the raw literature range rather than
t0012's widened test-conformant envelope.
"""

from __future__ import annotations

import json
import sys

import pandas as pd
from pandas import DataFrame
from pydantic import BaseModel, ConfigDict

from tasks.t0020_port_modeldb_189347_gabamod.code.constants import (
    CONDITION_COLUMN,
    DSI_ENVELOPE,
    FIRING_RATE_COLUMN,
    METRIC_KEY_DSI,
    METRIC_KEY_GATE_PASSED,
    METRIC_KEY_MEAN_ND_HZ,
    METRIC_KEY_MEAN_PD_HZ,
    METRIC_KEY_PEAK_HZ,
    N_TRIALS_PER_CONDITION,
    PEAK_ENVELOPE_HZ,
    PROTOCOL_NAME,
    TRIAL_SEED_COLUMN,
    Condition,
)
from tasks.t0020_port_modeldb_189347_gabamod.code.paths import (
    METRICS_JSON,
    RESULTS_DIR,
    SCORE_REPORT_JSON,
    TUNING_CURVES_CSV,
)

TUNING_CURVES_DTYPE: dict[str, object] = {
    CONDITION_COLUMN: pd.StringDtype(),
    TRIAL_SEED_COLUMN: pd.UInt32Dtype(),
    FIRING_RATE_COLUMN: "float64",
}


class GateResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    dsi_min: float
    dsi_max: float
    peak_min_hz: float
    peak_max_hz: float
    dsi_in_range: bool
    peak_in_range: bool
    passed: bool


class ScoreReport(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    protocol: str
    n_trials_per_condition: int
    n_pd_trials: int
    n_nd_trials: int
    mean_pd_hz: float
    mean_nd_hz: float
    std_pd_hz: float
    std_nd_hz: float
    dsi: float
    peak_hz: float
    gate: GateResult


def _load_tuning_curves() -> DataFrame:
    df = pd.read_csv(
        filepath_or_buffer=TUNING_CURVES_CSV,
        dtype=TUNING_CURVES_DTYPE,
    )
    assert CONDITION_COLUMN in df.columns, (
        f"missing column '{CONDITION_COLUMN}' in {TUNING_CURVES_CSV}; got {list(df.columns)}"
    )
    assert FIRING_RATE_COLUMN in df.columns, (
        f"missing column '{FIRING_RATE_COLUMN}' in {TUNING_CURVES_CSV}; got {list(df.columns)}"
    )
    return df


def _build_score_report(*, df: DataFrame) -> ScoreReport:
    pd_mask = df[CONDITION_COLUMN] == Condition.PD.value
    nd_mask = df[CONDITION_COLUMN] == Condition.ND.value
    pd_rates = df.loc[pd_mask, FIRING_RATE_COLUMN]
    nd_rates = df.loc[nd_mask, FIRING_RATE_COLUMN]

    assert len(pd_rates) > 0, "no PD trials in tuning_curves.csv"
    assert len(nd_rates) > 0, "no ND trials in tuning_curves.csv"

    mean_pd = float(pd_rates.mean())
    mean_nd = float(nd_rates.mean())
    std_pd = float(pd_rates.std(ddof=0))
    std_nd = float(nd_rates.std(ddof=0))

    denom = mean_pd + mean_nd
    assert denom > 0.0, (
        f"mean_PD + mean_ND is zero; DSI undefined. mean_PD={mean_pd}, mean_ND={mean_nd}"
    )
    dsi = (mean_pd - mean_nd) / denom
    peak_hz = mean_pd

    dsi_min, dsi_max = DSI_ENVELOPE
    peak_min, peak_max = PEAK_ENVELOPE_HZ
    dsi_in_range = dsi_min <= dsi <= dsi_max
    peak_in_range = peak_min <= peak_hz <= peak_max

    gate = GateResult(
        dsi_min=dsi_min,
        dsi_max=dsi_max,
        peak_min_hz=peak_min,
        peak_max_hz=peak_max,
        dsi_in_range=dsi_in_range,
        peak_in_range=peak_in_range,
        passed=dsi_in_range and peak_in_range,
    )
    return ScoreReport(
        protocol=PROTOCOL_NAME,
        n_trials_per_condition=N_TRIALS_PER_CONDITION,
        n_pd_trials=int(len(pd_rates)),
        n_nd_trials=int(len(nd_rates)),
        mean_pd_hz=mean_pd,
        mean_nd_hz=mean_nd,
        std_pd_hz=std_pd,
        std_nd_hz=std_nd,
        dsi=dsi,
        peak_hz=peak_hz,
        gate=gate,
    )


def _write_metrics_json(*, report: ScoreReport) -> None:
    payload: dict[str, float | bool] = {
        METRIC_KEY_DSI: report.dsi,
        METRIC_KEY_PEAK_HZ: report.peak_hz,
        METRIC_KEY_MEAN_PD_HZ: report.mean_pd_hz,
        METRIC_KEY_MEAN_ND_HZ: report.mean_nd_hz,
        METRIC_KEY_GATE_PASSED: report.gate.passed,
    }
    METRICS_JSON.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    if not TUNING_CURVES_CSV.exists():
        print(
            f"ERROR: tuning curve CSV missing at {TUNING_CURVES_CSV}",
            flush=True,
        )
        return 1

    print(f"Scoring {TUNING_CURVES_CSV} vs literature envelope...", flush=True)
    df = _load_tuning_curves()
    report = _build_score_report(df=df)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SCORE_REPORT_JSON.write_text(
        report.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"  wrote {SCORE_REPORT_JSON}", flush=True)

    _write_metrics_json(report=report)
    print(f"  wrote {METRICS_JSON}", flush=True)

    print(
        "\nSummary:\n"
        f"  protocol                = {report.protocol}\n"
        f"  n_PD / n_ND             = {report.n_pd_trials} / {report.n_nd_trials}\n"
        f"  mean_PD (Hz)            = {report.mean_pd_hz:.2f} "
        f"(std {report.std_pd_hz:.2f})\n"
        f"  mean_ND (Hz)            = {report.mean_nd_hz:.2f} "
        f"(std {report.std_nd_hz:.2f})\n"
        f"  DSI                     = {report.dsi:.4f} "
        f"(envelope {report.gate.dsi_min}-{report.gate.dsi_max})\n"
        f"  peak (Hz)               = {report.peak_hz:.2f} "
        f"(envelope {report.gate.peak_min_hz}-{report.gate.peak_max_hz})\n"
        f"  dsi_in_range            = {report.gate.dsi_in_range}\n"
        f"  peak_in_range           = {report.gate.peak_in_range}\n"
        f"  gate.passed             = {report.gate.passed}\n",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
