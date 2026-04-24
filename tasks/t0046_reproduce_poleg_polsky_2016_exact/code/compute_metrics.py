"""Compute reproduction metrics from results/data/*.csv and write results/metrics.json.

Produces the explicit multi-variant format defined in
``arf/specifications/metrics_specification.md`` v4 and
``arf/specifications/task_results_specification.md`` v8.

Variants:

* ``control_gnmda05``     - Fig 1 control PSP at code's b2gnmda = 0.5 nS.
* ``control_gnmda25``     - Fig 1 control PSP at paper's b2gnmda = 2.5 nS.
* ``ap5_gnmda0``          - Fig 2 AP5 analogue (b2gnmda = 0).
* ``high_cl_exptype3``    - Fig 4 high-Cl- (tuned-excitation analogue).
* ``zero_mg_exptype2``    - Fig 5 0 Mg2+ (Voff_bipNMDA = 1).
* ``noise_control_*``     - Fig 6/7 noise sweep (control + 0Mg + AP5 at 0/0.10/0.30 SD).
* ``fig8_*``              - Fig 8 suprathreshold (control + AP5 + 0Mg, with spikes).

Per-variant metrics include ``direction_selectivity_index`` (computed on PSP peaks for
subthreshold variants and on AP counts for fig8 variants) and ``tuning_curve_hwhm_deg`` for
fig8 variants only (the paper does not report PSP HWHM).

Subthreshold variants explicitly set ``tuning_curve_hwhm_deg``,
``tuning_curve_reliability``, and ``tuning_curve_rmse`` to ``null`` because the paper does not
report a PSP-derived target tuning curve (see plan Approach section).
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (
    METRIC_KEY_DSI,
    METRIC_KEY_HWHM,
    METRIC_KEY_RELIABILITY,
    METRIC_KEY_RMSE,
    TSTOP_MS,
)
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.paths import (
    DATA_DIR,
    METRICS_JSON,
)


@dataclass(frozen=True, slots=True)
class TrialRow:
    notes: str
    direction_label: str
    trial_seed: int
    flicker_var: float
    stim_noise_var: float
    b2gnmda_ns: float
    peak_psp_mv: float
    baseline_psp_mv: float
    spike_count: int
    ap_rate_hz: float
    exptype: int


@dataclass(slots=True)
class GroupStats:
    pd_psps: list[float] = field(default_factory=list)
    nd_psps: list[float] = field(default_factory=list)
    pd_baselines: list[float] = field(default_factory=list)
    nd_baselines: list[float] = field(default_factory=list)
    pd_spikes: list[int] = field(default_factory=list)
    nd_spikes: list[int] = field(default_factory=list)


def _load_csv(*, path: Path) -> list[TrialRow]:
    rows: list[TrialRow] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader: Any = csv.DictReader(fh)
        for r in reader:
            rows.append(
                TrialRow(
                    notes=r["notes"],
                    direction_label=r["direction_label"],
                    trial_seed=int(r["trial_seed"]),
                    flicker_var=float(r["flicker_var"]),
                    stim_noise_var=float(r["stim_noise_var"]),
                    b2gnmda_ns=float(r["b2gnmda_ns"]),
                    peak_psp_mv=float(r["peak_psp_mv"]),
                    baseline_psp_mv=float(r["baseline_psp_mv"]),
                    spike_count=int(r["spike_count"]),
                    ap_rate_hz=float(r["ap_rate_hz"]),
                    exptype=int(r["exptype"]),
                ),
            )
    return rows


def _mean(values: Iterable[float]) -> float | None:
    seq: list[float] = list(values)
    if len(seq) == 0:
        return None
    return float(sum(seq) / len(seq))


def _sd(values: Iterable[float]) -> float | None:
    seq: list[float] = list(values)
    n: int = len(seq)
    if n < 2:
        return None
    m: float = sum(seq) / n
    var: float = sum((x - m) ** 2 for x in seq) / (n - 1)
    return float(var**0.5)


def _dsi(*, pd_values: list[float], nd_values: list[float]) -> float | None:
    pd_mean: float | None = _mean(pd_values)
    nd_mean: float | None = _mean(nd_values)
    if pd_mean is None or nd_mean is None:
        return None
    if pd_mean + nd_mean == 0.0:
        return 0.0
    return float((pd_mean - nd_mean) / (pd_mean + nd_mean))


def _group_by_notes(*, rows: list[TrialRow]) -> dict[str, GroupStats]:
    grouped: dict[str, GroupStats] = defaultdict(GroupStats)
    for r in rows:
        gs: GroupStats = grouped[r.notes]
        if r.direction_label == "PD":
            gs.pd_psps.append(r.peak_psp_mv)
            gs.pd_baselines.append(r.baseline_psp_mv)
            gs.pd_spikes.append(r.spike_count)
        else:
            gs.nd_psps.append(r.peak_psp_mv)
            gs.nd_baselines.append(r.baseline_psp_mv)
            gs.nd_spikes.append(r.spike_count)
    return grouped


def _roc_auc_pd_vs_baseline(*, pd_values: list[float], baselines: list[float]) -> float | None:
    """Compute one-sided ROC AUC of PD-trial peaks vs PD baselines (proxy for noise-free AUC).

    Sklearn-style: positives = PD peaks, negatives = baseline means; AUC = P(peak > baseline).
    """
    n_pos: int = len(pd_values)
    n_neg: int = len(baselines)
    if n_pos == 0 or n_neg == 0:
        return None
    correct: int = 0
    for p in pd_values:
        for b in baselines:
            if p > b:
                correct += 1
            elif p == b:
                correct += 0  # half if tied; ignored for stability.
    return float(correct) / float(n_pos * n_neg)


def _slope_angle_deg(*, pd_psps: list[float], nd_psps: list[float]) -> float | None:
    """Approximate paper's slope-angle metric.

    The paper computes an angle from the PD-vs-ND scatter; values around 45 deg = additive,
    values around 90 deg = multiplicative. Here we approximate by atan2 of (PD mean - rest)
    over (ND mean - rest), expressed in degrees. This is a coarse single-number proxy; full
    scatter slopes require a per-dendrite EPSP series the model does not expose by default.
    """
    import math

    pd_m: float | None = _mean(pd_psps)
    nd_m: float | None = _mean(nd_psps)
    if pd_m is None or nd_m is None:
        return None
    if pd_m == 0.0 and nd_m == 0.0:
        return None
    angle: float = math.degrees(math.atan2(pd_m, nd_m))
    return float(angle)


def _build_subthreshold_variant(*, variant_id: str, label: str, gs: GroupStats) -> dict[str, Any]:
    pd_mean: float | None = _mean(gs.pd_psps)
    pd_sd: float | None = _sd(gs.pd_psps)
    nd_mean: float | None = _mean(gs.nd_psps)
    nd_sd: float | None = _sd(gs.nd_psps)
    dsi: float | None = _dsi(pd_values=gs.pd_psps, nd_values=gs.nd_psps)
    slope: float | None = _slope_angle_deg(pd_psps=gs.pd_psps, nd_psps=gs.nd_psps)
    auc: float | None = _roc_auc_pd_vs_baseline(
        pd_values=gs.pd_psps,
        baselines=gs.pd_baselines + gs.nd_baselines,
    )
    return {
        "variant_id": variant_id,
        "label": label,
        "dimensions": {
            "kind": "subthreshold_psp",
            "n_pd_trials": len(gs.pd_psps),
            "n_nd_trials": len(gs.nd_psps),
            "psp_pd_mean_mv": pd_mean,
            "psp_pd_sd_mv": pd_sd,
            "psp_nd_mean_mv": nd_mean,
            "psp_nd_sd_mv": nd_sd,
            "slope_angle_deg": slope,
            "roc_auc_pd_vs_baseline": auc,
        },
        "metrics": {
            METRIC_KEY_DSI: dsi,
            METRIC_KEY_HWHM: None,
            METRIC_KEY_RELIABILITY: None,
            METRIC_KEY_RMSE: None,
        },
    }


def _build_suprathreshold_variant(
    *,
    variant_id: str,
    label: str,
    gs: GroupStats,
) -> dict[str, Any]:
    pd_rates_hz: list[float] = [c / (TSTOP_MS / 1000.0) for c in gs.pd_spikes]
    nd_rates_hz: list[float] = [c / (TSTOP_MS / 1000.0) for c in gs.nd_spikes]
    pd_mean: float | None = _mean(pd_rates_hz)
    pd_sd: float | None = _sd(pd_rates_hz)
    nd_mean: float | None = _mean(nd_rates_hz)
    nd_sd: float | None = _sd(nd_rates_hz)
    dsi_spikes: float | None = _dsi(pd_values=pd_rates_hz, nd_values=nd_rates_hz)
    pd_failure_rate: float | None = (
        float(sum(1 for c in gs.pd_spikes if c == 0)) / float(len(gs.pd_spikes))
        if len(gs.pd_spikes) > 0
        else None
    )
    return {
        "variant_id": variant_id,
        "label": label,
        "dimensions": {
            "kind": "suprathreshold_spikes",
            "n_pd_trials": len(gs.pd_spikes),
            "n_nd_trials": len(gs.nd_spikes),
            "ap_rate_pd_mean_hz": pd_mean,
            "ap_rate_pd_sd_hz": pd_sd,
            "ap_rate_nd_mean_hz": nd_mean,
            "ap_rate_nd_sd_hz": nd_sd,
            "pd_failure_rate": pd_failure_rate,
        },
        "metrics": {
            METRIC_KEY_DSI: dsi_spikes,
            METRIC_KEY_HWHM: None,  # 8 directions but we run only PD vs ND; no full curve.
            METRIC_KEY_RELIABILITY: None,
            METRIC_KEY_RMSE: None,
        },
    }


def main() -> int:
    variants: list[dict[str, Any]] = []

    fig1_rows: list[TrialRow] = _load_csv(path=DATA_DIR / "fig1_psp.csv")
    fig1_groups: dict[str, GroupStats] = _group_by_notes(rows=fig1_rows)
    if "fig1_control_gnmda05" in fig1_groups:
        variants.append(
            _build_subthreshold_variant(
                variant_id="control_gnmda05",
                label="Fig 1 control (b2gnmda = 0.5 nS, code value)",
                gs=fig1_groups["fig1_control_gnmda05"],
            ),
        )
    if "fig1_control_gnmda25" in fig1_groups:
        variants.append(
            _build_subthreshold_variant(
                variant_id="control_gnmda25",
                label="Fig 1 control (b2gnmda = 2.5 nS, paper value)",
                gs=fig1_groups["fig1_control_gnmda25"],
            ),
        )

    fig2_rows: list[TrialRow] = _load_csv(path=DATA_DIR / "fig2_imk801_psp.csv")
    fig2_groups: dict[str, GroupStats] = _group_by_notes(rows=fig2_rows)
    if "fig2_ap5_gnmda0" in fig2_groups:
        variants.append(
            _build_subthreshold_variant(
                variant_id="ap5_gnmda0",
                label="Fig 2 AP5 analogue (b2gnmda = 0)",
                gs=fig2_groups["fig2_ap5_gnmda0"],
            ),
        )

    fig4_rows: list[TrialRow] = _load_csv(path=DATA_DIR / "fig4_highcl_psp.csv")
    fig4_groups: dict[str, GroupStats] = _group_by_notes(rows=fig4_rows)
    if "fig4_highcl" in fig4_groups:
        variants.append(
            _build_subthreshold_variant(
                variant_id="high_cl_exptype3",
                label="Fig 4 high-Cl- (tuned-excitation analogue, exptype = 3)",
                gs=fig4_groups["fig4_highcl"],
            ),
        )

    fig5_rows: list[TrialRow] = _load_csv(path=DATA_DIR / "fig5_zeromg_psp.csv")
    fig5_groups: dict[str, GroupStats] = _group_by_notes(rows=fig5_rows)
    if "fig5_zeromg" in fig5_groups:
        variants.append(
            _build_subthreshold_variant(
                variant_id="zero_mg_exptype2",
                label="Fig 5 0 Mg2+ (Voff_bipNMDA = 1, exptype = 2)",
                gs=fig5_groups["fig5_zeromg"],
            ),
        )

    fig6_rows: list[TrialRow] = _load_csv(path=DATA_DIR / "fig6_noise.csv")
    fig6_groups: dict[str, GroupStats] = _group_by_notes(rows=fig6_rows)
    for label_prefix in ("fig6_control", "fig6_zeromg", "fig6_ap5"):
        for noise_sd in (0.0, 0.10, 0.30):
            key: str = f"{label_prefix}_noise{noise_sd:.2f}"
            if key in fig6_groups:
                variant_id: str = (
                    f"{label_prefix.replace('fig6_', 'noise_')}_sd{int(noise_sd * 100):02d}"
                )
                variants.append(
                    _build_subthreshold_variant(
                        variant_id=variant_id,
                        label=f"Fig 6/7 {label_prefix} flickerVAR={noise_sd:.2f}",
                        gs=fig6_groups[key],
                    ),
                )

    fig8_rows: list[TrialRow] = _load_csv(path=DATA_DIR / "fig8_spikes.csv")
    fig8_groups: dict[str, GroupStats] = _group_by_notes(rows=fig8_rows)
    for label_prefix in ("fig8_control", "fig8_ap5", "fig8_zeromg"):
        for noise_sd in (0.0, 0.10):
            key = f"{label_prefix}_noise{noise_sd:.2f}"
            if key in fig8_groups:
                variants.append(
                    _build_suprathreshold_variant(
                        variant_id=f"{label_prefix}_sd{int(noise_sd * 100):02d}",
                        label=f"Fig 8 {label_prefix} flickerVAR={noise_sd:.2f}",
                        gs=fig8_groups[key],
                    ),
                )

    out: dict[str, Any] = {
        "spec_version": "2",
        "task_id": "t0046_reproduce_poleg_polsky_2016_exact",
        "variants": variants,
    }
    METRICS_JSON.parent.mkdir(parents=True, exist_ok=True)
    METRICS_JSON.write_text(
        data=json.dumps(obj=out, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {METRICS_JSON} with {len(variants)} variants.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
