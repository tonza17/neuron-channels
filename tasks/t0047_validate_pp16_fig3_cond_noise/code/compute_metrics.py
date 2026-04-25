"""Compute aggregated tables and metrics for t0047.

Inputs (CSVs from drivers):
    * ``GNMDA_TRIALS_CSV``      — 56 rows (7 gNMDA x 2 dir x 4 trials)
    * ``NOISE_TRIALS_CSV``      — 96 rows (3 cond x 4 noise x 2 dir x 4 trials)

Outputs:
    * ``CONDUCTANCE_TABLE_CSV`` — per-(channel, direction, gnmda) summary with
      mean / std and the +/-25% verdict against paper Fig 3A-E targets.
    * ``DSI_BY_GNMDA_JSON``     — DSI per gNMDA value (Fig 3F bottom).
    * ``DSI_AUC_BY_COND_NOISE_JSON`` — DSI and AUC per (condition, flickerVAR) cell.
    * ``METRICS_JSON``          — explicit-multi-variant metrics file.
"""

from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from typing import Any

import pandas as pd

from tasks.t0047_validate_pp16_fig3_cond_noise.code.constants import (
    AMPA_ND_TARGET_NS,
    AMPA_PD_TARGET_NS,
    B2GNMDA_GRID_NS,
    COL_BASELINE_MEAN_MV,
    COL_CONDITION,
    COL_DIRECTION,
    COL_FLICKER_VAR,
    COL_PEAK_G_AMPA_SUMMED_NS,
    COL_PEAK_G_NMDA_SUMMED_NS,
    COL_PEAK_G_SACINHIB_SUMMED_NS,
    COL_PEAK_PSP_MV,
    CONDUCTANCE_TOLERANCE_FRAC,
    DIRECTION_ND_LABEL,
    DIRECTION_PD_LABEL,
    GABA_ND_TARGET_NS,
    GABA_PD_TARGET_NS,
    METRIC_KEY_DSI,
    NMDA_ND_TARGET_NS,
    NMDA_PD_TARGET_NS,
    NoiseCondition,
)
from tasks.t0047_validate_pp16_fig3_cond_noise.code.dsi import compute_dsi_pd_nd
from tasks.t0047_validate_pp16_fig3_cond_noise.code.paths import (
    CONDUCTANCE_TABLE_CSV,
    DSI_AUC_BY_COND_NOISE_JSON,
    DSI_BY_GNMDA_JSON,
    GNMDA_TRIALS_CSV,
    METRICS_JSON,
    NOISE_TRIALS_CSV,
    RESULTS_DATA_DIR,
)
from tasks.t0047_validate_pp16_fig3_cond_noise.code.scoring import (
    compute_roc_auc_pd_vs_baseline,
)


@dataclass(frozen=True, slots=True)
class ChannelTarget:
    """Paper Fig 3A-E target per channel per direction."""

    channel_label: str  # "NMDA" / "AMPA" / "GABA"
    target_pd_ns: float
    target_nd_ns: float
    csv_column: str


_CHANNELS: tuple[ChannelTarget, ...] = (
    ChannelTarget(
        channel_label="NMDA",
        target_pd_ns=NMDA_PD_TARGET_NS,
        target_nd_ns=NMDA_ND_TARGET_NS,
        csv_column=COL_PEAK_G_NMDA_SUMMED_NS,
    ),
    ChannelTarget(
        channel_label="AMPA",
        target_pd_ns=AMPA_PD_TARGET_NS,
        target_nd_ns=AMPA_ND_TARGET_NS,
        csv_column=COL_PEAK_G_AMPA_SUMMED_NS,
    ),
    ChannelTarget(
        channel_label="GABA",
        target_pd_ns=GABA_PD_TARGET_NS,
        target_nd_ns=GABA_ND_TARGET_NS,
        csv_column=COL_PEAK_G_SACINHIB_SUMMED_NS,
    ),
)


def _load_gnmda_trials() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(GNMDA_TRIALS_CSV)
    return df


def _load_noise_trials() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(NOISE_TRIALS_CSV)
    return df


def _gnmda_to_variant_id(b2gnmda_ns: float) -> str:
    """Format e.g. 0.5 -> 'gnmda_0p5ns', 1.0 -> 'gnmda_1p0ns'."""
    return f"gnmda_{b2gnmda_ns:.1f}ns".replace(".", "p")


def _flicker_to_variant_id(*, condition: NoiseCondition, flicker_var: float) -> str:
    """Format e.g. (CONTROL, 0.3) -> 'control_flicker_0p3'.

    Variant IDs must be lowercase letters, digits, dots, hyphens, and underscores per
    arf/specifications/task_results_specification.md (verify_task_metrics enforces TM-E003).
    """
    cond_slug: str = condition.value.lower().replace("0mg", "zero_mg")
    return f"{cond_slug}_flicker_{flicker_var:.1f}".replace(".", "p")


def _build_conductance_table(*, df_gnmda: pd.DataFrame) -> list[dict[str, Any]]:
    """One row per (channel, direction, b2gnmda_ns) cell."""
    rows: list[dict[str, Any]] = []
    for channel in _CHANNELS:
        for dir_label, target_ns in (
            (DIRECTION_PD_LABEL, channel.target_pd_ns),
            (DIRECTION_ND_LABEL, channel.target_nd_ns),
        ):
            for b2gnmda_ns in B2GNMDA_GRID_NS:
                cell: pd.DataFrame = df_gnmda[
                    (df_gnmda[COL_DIRECTION] == dir_label)
                    & (df_gnmda["b2gnmda_ns"].round(6) == round(float(b2gnmda_ns), 6))
                ]
                obs_summed: pd.Series = cell[channel.csv_column].astype(float)
                if len(obs_summed) == 0:
                    rows.append(
                        {
                            "channel": channel.channel_label,
                            "direction": dir_label,
                            "b2gnmda_ns": float(b2gnmda_ns),
                            "n_trials": 0,
                            "mean_summed_ns": None,
                            "std_summed_ns": None,
                            "paper_target_ns": float(target_ns),
                            "diff_pct": None,
                            "verdict_within_25pct": None,
                        },
                    )
                    continue
                mean_ns: float = float(obs_summed.mean())
                std_ns: float = float(obs_summed.std(ddof=1)) if len(obs_summed) > 1 else 0.0
                diff_pct: float = (mean_ns - float(target_ns)) / float(target_ns) * 100.0
                verdict: bool = (
                    abs(mean_ns - float(target_ns)) / float(target_ns) <= CONDUCTANCE_TOLERANCE_FRAC
                )
                rows.append(
                    {
                        "channel": channel.channel_label,
                        "direction": dir_label,
                        "b2gnmda_ns": float(b2gnmda_ns),
                        "n_trials": int(len(obs_summed)),
                        "mean_summed_ns": mean_ns,
                        "std_summed_ns": std_ns,
                        "paper_target_ns": float(target_ns),
                        "diff_pct": diff_pct,
                        "verdict_within_25pct": verdict,
                    },
                )
    return rows


def _write_conductance_table(*, rows: list[dict[str, Any]]) -> None:
    CONDUCTANCE_TABLE_CSV.parent.mkdir(parents=True, exist_ok=True)
    if len(rows) == 0:
        CONDUCTANCE_TABLE_CSV.write_text("", encoding="utf-8")
        return
    with CONDUCTANCE_TABLE_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer: csv.DictWriter[str] = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _compute_dsi_by_gnmda(*, df_gnmda: pd.DataFrame) -> dict[str, float | None]:
    out: dict[str, float | None] = {}
    for b2gnmda_ns in B2GNMDA_GRID_NS:
        pd_psp: list[float] = (
            df_gnmda[
                (df_gnmda[COL_DIRECTION] == DIRECTION_PD_LABEL)
                & (df_gnmda["b2gnmda_ns"].round(6) == round(float(b2gnmda_ns), 6))
            ][COL_PEAK_PSP_MV]
            .astype(float)
            .tolist()
        )
        nd_psp: list[float] = (
            df_gnmda[
                (df_gnmda[COL_DIRECTION] == DIRECTION_ND_LABEL)
                & (df_gnmda["b2gnmda_ns"].round(6) == round(float(b2gnmda_ns), 6))
            ][COL_PEAK_PSP_MV]
            .astype(float)
            .tolist()
        )
        dsi: float | None = compute_dsi_pd_nd(pd_values=pd_psp, nd_values=nd_psp)
        out[f"{b2gnmda_ns:.2f}"] = dsi
    return out


def _compute_dsi_auc_by_condition_noise(
    *,
    df_noise: pd.DataFrame,
) -> dict[str, dict[str, dict[str, float | None]]]:
    """Return {condition_value: {flickerVAR_str: {dsi: x, auc: y}}}."""
    out: dict[str, dict[str, dict[str, float | None]]] = {}
    for condition in NoiseCondition:
        out[condition.value] = {}
        for flicker_var in sorted(df_noise[COL_FLICKER_VAR].unique()):
            cell: pd.DataFrame = df_noise[
                (df_noise[COL_CONDITION] == condition.value)
                & (df_noise[COL_FLICKER_VAR].round(6) == round(float(flicker_var), 6))
            ]
            pd_psp: list[float] = (
                cell[cell[COL_DIRECTION] == DIRECTION_PD_LABEL][COL_PEAK_PSP_MV]
                .astype(float)
                .tolist()
            )
            nd_psp: list[float] = (
                cell[cell[COL_DIRECTION] == DIRECTION_ND_LABEL][COL_PEAK_PSP_MV]
                .astype(float)
                .tolist()
            )
            baselines: list[float] = cell[COL_BASELINE_MEAN_MV].astype(float).tolist()
            dsi: float | None = compute_dsi_pd_nd(pd_values=pd_psp, nd_values=nd_psp)
            auc: float | None = compute_roc_auc_pd_vs_baseline(
                pd_values=pd_psp,
                baselines=baselines,
            )
            out[condition.value][f"{float(flicker_var):.2f}"] = {
                "dsi": dsi,
                "auc": auc,
                "n_pd": len(pd_psp),
                "n_nd": len(nd_psp),
            }
    return out


def _build_metrics_json(
    *,
    dsi_by_gnmda: dict[str, float | None],
    dsi_auc_by_cond_noise: dict[str, dict[str, dict[str, float | None]]],
) -> dict[str, Any]:
    variants: list[dict[str, Any]] = []

    # Seven gNMDA-sweep variants.
    for b2gnmda_ns in B2GNMDA_GRID_NS:
        variant_id: str = _gnmda_to_variant_id(float(b2gnmda_ns))
        dsi_value: float | None = dsi_by_gnmda.get(f"{b2gnmda_ns:.2f}")
        variants.append(
            {
                "variant_id": variant_id,
                "label": f"gNMDA = {b2gnmda_ns:.2f} nS",
                "dimensions": {
                    "sweep": "gnmda",
                    "b2gnmda_ns": float(b2gnmda_ns),
                    "condition": "control",
                    "flicker_var": 0.0,
                },
                "metrics": {METRIC_KEY_DSI: dsi_value},
            },
        )

    # 3 conditions x 4 noise levels = 12 variants.
    for condition in NoiseCondition:
        for flicker_var_str, payload in dsi_auc_by_cond_noise[condition.value].items():
            flicker_var: float = float(flicker_var_str)
            variant_id = _flicker_to_variant_id(
                condition=condition,
                flicker_var=flicker_var,
            )
            variants.append(
                {
                    "variant_id": variant_id,
                    "label": f"{condition.value}, flickerVAR = {flicker_var:.2f}",
                    "dimensions": {
                        "sweep": "noise_extension",
                        "condition": condition.value,
                        "flicker_var": float(flicker_var),
                    },
                    "metrics": {METRIC_KEY_DSI: payload["dsi"]},
                },
            )

    return {"variants": variants}


def main() -> int:
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)

    df_gnmda: pd.DataFrame = _load_gnmda_trials()
    df_noise: pd.DataFrame = _load_noise_trials()

    rows: list[dict[str, Any]] = _build_conductance_table(df_gnmda=df_gnmda)
    _write_conductance_table(rows=rows)
    print(f"[compute_metrics] wrote {len(rows)} rows to {CONDUCTANCE_TABLE_CSV}", flush=True)

    dsi_by_gnmda: dict[str, float | None] = _compute_dsi_by_gnmda(df_gnmda=df_gnmda)
    DSI_BY_GNMDA_JSON.write_text(
        json.dumps(dsi_by_gnmda, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(f"[compute_metrics] DSI by gNMDA: {dsi_by_gnmda}", flush=True)

    dsi_auc_by_cond_noise: dict[str, dict[str, dict[str, float | None]]] = (
        _compute_dsi_auc_by_condition_noise(df_noise=df_noise)
    )
    DSI_AUC_BY_COND_NOISE_JSON.write_text(
        json.dumps(dsi_auc_by_cond_noise, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(
        f"[compute_metrics] DSI/AUC by condition x noise: {dsi_auc_by_cond_noise}",
        flush=True,
    )

    metrics_payload: dict[str, Any] = _build_metrics_json(
        dsi_by_gnmda=dsi_by_gnmda,
        dsi_auc_by_cond_noise=dsi_auc_by_cond_noise,
    )
    METRICS_JSON.write_text(
        json.dumps(metrics_payload, indent=2),
        encoding="utf-8",
    )
    print(
        f"[compute_metrics] wrote {len(metrics_payload['variants'])} variants to {METRICS_JSON}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
