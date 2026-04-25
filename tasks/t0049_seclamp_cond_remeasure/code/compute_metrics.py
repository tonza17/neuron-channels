"""Aggregate per-trial SEClamp current into per-channel conductance and verdicts.

Reads ``results/data/seclamp_trials.csv``, computes per-channel somatic-equivalent
conductance using ``g_nS = abs(i_pA) / abs(V_clamp - E_rev)``, aggregates across the 4
trials per (direction, channel) cell, derives the H0/H1/H2 verdict per cell, writes the
comparison table CSV, and emits ``results/metrics.json`` in the explicit multi-variant
format (6 channel x direction variants + 3 DSI roll-ups).
"""

from __future__ import annotations

import json
import math
from typing import Any

import pandas as pd

from tasks.t0049_seclamp_cond_remeasure.code.constants import (
    AMPA_ND_TARGET_NS,
    AMPA_PD_TARGET_NS,
    B2GNMDA_NS,
    CHANNEL_AMPA_LABEL,
    CHANNEL_GABA_LABEL,
    CHANNEL_NMDA_LABEL,
    COL_BASELINE_I_PA,
    COL_CHANNEL,
    COL_CHANNEL_ON,
    COL_CLAMP_V_SD_MV,
    COL_DELTA_PAPER_FRAC,
    COL_DELTA_T0047_FRAC,
    COL_DIRECTION,
    COL_G_SECLAMP_MEAN_NS,
    COL_G_SECLAMP_SD_NS,
    COL_N,
    COL_PAPER_TARGET_NS,
    COL_PEAK_I_MINUS_BASELINE_PA,
    COL_PEAK_I_PA,
    COL_T0047_PER_SYN_MEAN_NS,
    COL_T0047_SUMMED_NS,
    COL_TRIAL_SEED,
    COL_VERDICT,
    CONDUCTANCE_TOLERANCE_FRAC,
    DIRECTION_ND_LABEL,
    DIRECTION_PD_LABEL,
    E_AMPA_MV,
    E_GABA_MV,
    E_NMDA_MV,
    GABA_ND_TARGET_NS,
    GABA_PD_TARGET_NS,
    H0_TOLERANCE_FRAC,
    METRIC_KEY_DSI,
    NMDA_ND_TARGET_NS,
    NMDA_PD_TARGET_NS,
    T0047_AMPA_ND_NS,
    T0047_AMPA_PD_NS,
    T0047_GABA_ND_NS,
    T0047_GABA_PD_NS,
    T0047_NMDA_ND_NS,
    T0047_NMDA_PD_NS,
    T0047_NUM_SYNAPSES,
    TRIALS_PER_CONDITION,
    V_CLAMP_MV,
    VERDICT_H0,
    VERDICT_H1,
    VERDICT_H2,
    ChannelIsolation,
)
from tasks.t0049_seclamp_cond_remeasure.code.dsi import compute_dsi_pd_nd
from tasks.t0049_seclamp_cond_remeasure.code.paths import (
    METRICS_JSON,
    SECLAMP_COMPARISON_CSV,
    SECLAMP_TRIALS_CSV,
)

# Channel-isolation -> per-channel reversal potential mapping.
# (We only convert AMPA_ONLY / NMDA_ONLY / GABA_ONLY rows; the ALL row is kept in the
# per-trial CSV but excluded from the per-channel comparison table.)
ISOLATION_TO_E_REV_MV: dict[ChannelIsolation, float] = {
    ChannelIsolation.AMPA_ONLY: E_AMPA_MV,
    ChannelIsolation.NMDA_ONLY: E_NMDA_MV,
    ChannelIsolation.GABA_ONLY: E_GABA_MV,
}

# Channel-isolation -> short channel label.
ISOLATION_TO_CHANNEL_LABEL: dict[ChannelIsolation, str] = {
    ChannelIsolation.AMPA_ONLY: CHANNEL_AMPA_LABEL,
    ChannelIsolation.NMDA_ONLY: CHANNEL_NMDA_LABEL,
    ChannelIsolation.GABA_ONLY: CHANNEL_GABA_LABEL,
}

# Paper Fig 3A-E targets per (channel, direction).
PAPER_TARGETS_NS: dict[tuple[str, str], float] = {
    (CHANNEL_NMDA_LABEL, DIRECTION_PD_LABEL): NMDA_PD_TARGET_NS,
    (CHANNEL_NMDA_LABEL, DIRECTION_ND_LABEL): NMDA_ND_TARGET_NS,
    (CHANNEL_AMPA_LABEL, DIRECTION_PD_LABEL): AMPA_PD_TARGET_NS,
    (CHANNEL_AMPA_LABEL, DIRECTION_ND_LABEL): AMPA_ND_TARGET_NS,
    (CHANNEL_GABA_LABEL, DIRECTION_PD_LABEL): GABA_PD_TARGET_NS,
    (CHANNEL_GABA_LABEL, DIRECTION_ND_LABEL): GABA_ND_TARGET_NS,
}

# t0047 per-synapse-summed baseline values per (channel, direction).
T0047_SUMMED_NS: dict[tuple[str, str], float] = {
    (CHANNEL_NMDA_LABEL, DIRECTION_PD_LABEL): T0047_NMDA_PD_NS,
    (CHANNEL_NMDA_LABEL, DIRECTION_ND_LABEL): T0047_NMDA_ND_NS,
    (CHANNEL_AMPA_LABEL, DIRECTION_PD_LABEL): T0047_AMPA_PD_NS,
    (CHANNEL_AMPA_LABEL, DIRECTION_ND_LABEL): T0047_AMPA_ND_NS,
    (CHANNEL_GABA_LABEL, DIRECTION_PD_LABEL): T0047_GABA_PD_NS,
    (CHANNEL_GABA_LABEL, DIRECTION_ND_LABEL): T0047_GABA_ND_NS,
}


def _verdict_for(*, g_mean_ns: float, paper_target_ns: float, t0047_summed_ns: float) -> str:
    delta_paper_frac: float = abs(g_mean_ns - paper_target_ns) / paper_target_ns
    delta_t0047_frac: float = abs(g_mean_ns - t0047_summed_ns) / t0047_summed_ns
    if delta_paper_frac <= CONDUCTANCE_TOLERANCE_FRAC:
        return VERDICT_H1
    if delta_t0047_frac <= H0_TOLERANCE_FRAC:
        return VERDICT_H0
    return VERDICT_H2


def _e_rev_for_label(*, channel_label: str) -> float:
    if channel_label == CHANNEL_NMDA_LABEL:
        return E_NMDA_MV
    if channel_label == CHANNEL_AMPA_LABEL:
        return E_AMPA_MV
    if channel_label == CHANNEL_GABA_LABEL:
        return E_GABA_MV
    raise ValueError(f"Unknown channel label: {channel_label}")


def _per_trial_conductances(*, df_trials: pd.DataFrame) -> pd.DataFrame:
    """Add a g_ns column to per-channel-isolation rows; ALL rows get NaN."""
    rows: list[dict[str, Any]] = []
    for _, row in df_trials.iterrows():
        channel_on_value: str = str(row[COL_CHANNEL_ON])
        try:
            isolation: ChannelIsolation = ChannelIsolation(channel_on_value)
        except ValueError as exc:
            raise ValueError(
                f"Unrecognized channel_on value in trials CSV: {channel_on_value}",
            ) from exc
        if isolation == ChannelIsolation.ALL:
            channel_label: str | None = None
            g_ns: float | None = None
        else:
            channel_label = ISOLATION_TO_CHANNEL_LABEL[isolation]
            e_rev: float = ISOLATION_TO_E_REV_MV[isolation]
            driving_force_mv: float = abs(V_CLAMP_MV - e_rev)
            peak_pa: float = float(row[COL_PEAK_I_MINUS_BASELINE_PA])
            # NEURON unit identity: i[nA] = g[uS] * V[mV] -> g[nS] = 1000*i[nA]/V[mV] =
            # i[pA] / V[mV]. The peak_i_pa column already contains current in pA.
            g_ns = peak_pa / driving_force_mv
        new_row: dict[str, Any] = {
            COL_DIRECTION: str(row[COL_DIRECTION]),
            COL_CHANNEL_ON: channel_on_value,
            COL_CHANNEL: channel_label,
            COL_TRIAL_SEED: int(row[COL_TRIAL_SEED]),
            "g_ns": g_ns,
            COL_PEAK_I_PA: float(row[COL_PEAK_I_PA]),
            COL_BASELINE_I_PA: float(row[COL_BASELINE_I_PA]),
            COL_PEAK_I_MINUS_BASELINE_PA: float(row[COL_PEAK_I_MINUS_BASELINE_PA]),
            COL_CLAMP_V_SD_MV: float(row[COL_CLAMP_V_SD_MV]),
        }
        rows.append(new_row)
    return pd.DataFrame(rows)


def _aggregate_per_channel(*, df_per_trial_g: pd.DataFrame) -> pd.DataFrame:
    """Group by (channel, direction); compute mean, sd, n. Excludes ALL rows."""
    df_filtered: pd.DataFrame = df_per_trial_g[df_per_trial_g[COL_CHANNEL].notna()]
    grouped = df_filtered.groupby([COL_CHANNEL, COL_DIRECTION])["g_ns"].agg(
        [("g_seclamp_mean_ns", "mean"), ("g_seclamp_sd_ns", "std"), ("n", "count")],
    )
    grouped = grouped.reset_index()

    rows: list[dict[str, Any]] = []
    for _, row in grouped.iterrows():
        channel_label: str = str(row[COL_CHANNEL])
        direction_label: str = str(row[COL_DIRECTION])
        key: tuple[str, str] = (channel_label, direction_label)
        paper_target_ns: float = PAPER_TARGETS_NS[key]
        t0047_summed_ns: float = T0047_SUMMED_NS[key]
        t0047_per_syn_mean_ns: float = t0047_summed_ns / float(T0047_NUM_SYNAPSES)
        g_mean_ns: float = float(row["g_seclamp_mean_ns"])
        g_sd_ns: float = (
            float(row["g_seclamp_sd_ns"])
            if not math.isnan(
                float(row["g_seclamp_sd_ns"]),
            )
            else 0.0
        )
        delta_paper_frac: float = abs(g_mean_ns - paper_target_ns) / paper_target_ns
        delta_t0047_frac: float = abs(g_mean_ns - t0047_summed_ns) / t0047_summed_ns
        verdict: str = _verdict_for(
            g_mean_ns=g_mean_ns,
            paper_target_ns=paper_target_ns,
            t0047_summed_ns=t0047_summed_ns,
        )
        rows.append(
            {
                COL_CHANNEL: channel_label,
                COL_DIRECTION: direction_label,
                COL_G_SECLAMP_MEAN_NS: g_mean_ns,
                COL_G_SECLAMP_SD_NS: g_sd_ns,
                COL_N: int(row["n"]),
                COL_PAPER_TARGET_NS: paper_target_ns,
                COL_T0047_SUMMED_NS: t0047_summed_ns,
                COL_T0047_PER_SYN_MEAN_NS: t0047_per_syn_mean_ns,
                COL_DELTA_PAPER_FRAC: delta_paper_frac,
                COL_DELTA_T0047_FRAC: delta_t0047_frac,
                COL_VERDICT: verdict,
            },
        )
    return pd.DataFrame(rows)


def _build_metrics_json(
    *,
    df_per_trial_g: pd.DataFrame,
    df_compare: pd.DataFrame,
) -> dict[str, Any]:
    """Build the explicit multi-variant metrics.json (6 channel x direction + 3 DSI)."""
    variants: list[dict[str, Any]] = []

    # 6 per-cell variants with empty metrics (the registered metric DSI is reported as a
    # roll-up; conductance amplitudes live in the comparison CSV).
    for _, row in df_compare.iterrows():
        channel_label: str = str(row[COL_CHANNEL])
        direction_label: str = str(row[COL_DIRECTION])
        variant_id: str = f"{channel_label}_{direction_label.lower()}"
        label: str = f"{channel_label.upper()}, {direction_label} direction (SEClamp at -65 mV)"
        variants.append(
            {
                "variant_id": variant_id,
                "label": label,
                "dimensions": {
                    "channel": channel_label,
                    "direction": direction_label,
                    "v_clamp_mv": float(V_CLAMP_MV),
                    "b2gnmda_ns": float(B2GNMDA_NS),
                },
                "metrics": {},
            },
        )

    # 3 DSI roll-ups per channel using per-trial conductances.
    df_isol: pd.DataFrame = df_per_trial_g[df_per_trial_g[COL_CHANNEL].notna()]
    for channel_label in (CHANNEL_NMDA_LABEL, CHANNEL_AMPA_LABEL, CHANNEL_GABA_LABEL):
        pd_values: list[float] = [
            float(v)
            for v in df_isol[
                (df_isol[COL_CHANNEL] == channel_label)
                & (df_isol[COL_DIRECTION] == DIRECTION_PD_LABEL)
            ]["g_ns"].tolist()
        ]
        nd_values: list[float] = [
            float(v)
            for v in df_isol[
                (df_isol[COL_CHANNEL] == channel_label)
                & (df_isol[COL_DIRECTION] == DIRECTION_ND_LABEL)
            ]["g_ns"].tolist()
        ]
        dsi_value: float | None = compute_dsi_pd_nd(
            pd_values=pd_values,
            nd_values=nd_values,
        )
        variants.append(
            {
                "variant_id": f"{channel_label}_dsi",
                "label": f"{channel_label.upper()} conductance DSI (SEClamp)",
                "dimensions": {
                    "channel": channel_label,
                    "metric_kind": "conductance_dsi",
                },
                "metrics": {
                    METRIC_KEY_DSI: dsi_value,
                },
            },
        )

    return {"variants": variants}


def main() -> None:
    print(f"[metrics] Reading {SECLAMP_TRIALS_CSV}", flush=True)
    df_trials: pd.DataFrame = pd.read_csv(SECLAMP_TRIALS_CSV)
    expected_total: int = 2 * 4 * TRIALS_PER_CONDITION
    assert len(df_trials) == expected_total, (
        f"Expected {expected_total} per-trial rows, got {len(df_trials)}"
    )

    df_per_trial_g: pd.DataFrame = _per_trial_conductances(df_trials=df_trials)

    df_compare: pd.DataFrame = _aggregate_per_channel(df_per_trial_g=df_per_trial_g)

    # Validation gate.
    assert len(df_compare) == 6, f"Expected 6 (channel, direction) cells, got {len(df_compare)}"
    assert df_compare[COL_G_SECLAMP_MEAN_NS].notna().all(), "NaN found in g_seclamp_mean_ns"
    assert (df_compare[COL_N] == TRIALS_PER_CONDITION).all(), (
        f"Each cell must have n=={TRIALS_PER_CONDITION} trials; got {df_compare[COL_N].tolist()}"
    )
    assert df_compare[COL_VERDICT].isin([VERDICT_H0, VERDICT_H1, VERDICT_H2]).all(), (
        f"Unknown verdict label(s): {df_compare[COL_VERDICT].unique().tolist()}"
    )

    df_compare.to_csv(SECLAMP_COMPARISON_CSV, index=False)
    print(f"[metrics] Wrote {SECLAMP_COMPARISON_CSV}", flush=True)

    metrics: dict[str, Any] = _build_metrics_json(
        df_per_trial_g=df_per_trial_g,
        df_compare=df_compare,
    )
    METRICS_JSON.write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )
    print(f"[metrics] Wrote {METRICS_JSON}", flush=True)

    print("\n[metrics] Per-channel SEClamp conductance summary:")
    print(
        df_compare[
            [
                COL_CHANNEL,
                COL_DIRECTION,
                COL_G_SECLAMP_MEAN_NS,
                COL_G_SECLAMP_SD_NS,
                COL_PAPER_TARGET_NS,
                COL_T0047_SUMMED_NS,
                COL_DELTA_PAPER_FRAC,
                COL_DELTA_T0047_FRAC,
                COL_VERDICT,
            ]
        ].to_string(index=False),
    )


if __name__ == "__main__":
    main()
