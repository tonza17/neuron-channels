"""68 x 4 corner-mean heatmap on the spiking cohort.

Z-score using the full-cohort standardiser, then compute mean z-score per MI x ATP corner
(median splits). Render as RdBu_r symmetric heatmap and persist the underlying matrix.

Outputs:
    results/data/corner_param_means.csv
    results/images/corner_param_heatmap.png
"""

from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.typing import NDArray

from tasks.t0125_t0123_cluster_factor_mi_atp.code.cluster_helpers import (
    PooledStandardiser,
    load_standardiser,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.constants import (
    ALL_PARAM_NAMES,
    CHART_DPI,
    CORNER_LABELS,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.group_thresholds import (
    GroupThresholds,
    assign_corner_label,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.load_t0123_cells import (
    ATP_PER_SPIKE_COLUMN,
    DSI_COLUMN,
    MI_COLUMN,
    PD_COLUMN,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.paths import (
    CORNER_PARAM_HEATMAP_PNG,
    CORNER_PARAM_MEANS_CSV,
    GROUP_THRESHOLDS_JSON,
    T0123_SPIKING_CELLS_PARQUET,
    T0123_STANDARDISER_NPZ,
)

PARAMETER_COLUMN: str = "parameter"


def _build_corner_label_array(
    *,
    df: pd.DataFrame,
    thresholds: GroupThresholds,
) -> NDArray[np.str_]:
    mi_vals: NDArray[np.float64] = df[MI_COLUMN].to_numpy(dtype=np.float64)
    atp_vals: NDArray[np.float64] = df[ATP_PER_SPIKE_COLUMN].to_numpy(dtype=np.float64)
    return np.array(
        [
            assign_corner_label(mi_val=float(m), atp_val=float(a), thresholds=thresholds)
            for m, a in zip(mi_vals.tolist(), atp_vals.tolist(), strict=True)
        ],
        dtype=str,
    )


def main() -> None:
    df_spiking: pd.DataFrame = pd.read_parquet(T0123_SPIKING_CELLS_PARQUET)
    standardiser: PooledStandardiser = load_standardiser(path=T0123_STANDARDISER_NPZ)
    thresholds_payload: dict[str, object] = json.loads(
        GROUP_THRESHOLDS_JSON.read_text(encoding="utf-8")
    )
    thresholds: GroupThresholds = GroupThresholds(
        mi_q1=float(thresholds_payload["mi_q1"]),  # type: ignore[arg-type]
        mi_median=float(thresholds_payload["mi_median"]),  # type: ignore[arg-type]
        mi_q3=float(thresholds_payload["mi_q3"]),  # type: ignore[arg-type]
        atp_q1=float(thresholds_payload["atp_q1"]),  # type: ignore[arg-type]
        atp_median=float(thresholds_payload["atp_median"]),  # type: ignore[arg-type]
        atp_q3=float(thresholds_payload["atp_q3"]),  # type: ignore[arg-type]
    )

    matrix_68d: NDArray[np.float64] = df_spiking[list(ALL_PARAM_NAMES)].to_numpy(dtype=np.float64)
    z_spiking: NDArray[np.float64] = standardiser.transform(matrix_68d)
    corner_labels_arr: NDArray[np.str_] = _build_corner_label_array(
        df=df_spiking, thresholds=thresholds
    )

    # 68 x 4 matrix of mean z-scores per corner.
    matrix_68x4: NDArray[np.float64] = np.zeros((len(ALL_PARAM_NAMES), len(CORNER_LABELS)))
    for col_idx, corner_label in enumerate(CORNER_LABELS):
        mask: NDArray[np.bool_] = corner_labels_arr == corner_label
        if int(mask.sum()) == 0:
            matrix_68x4[:, col_idx] = np.nan
        else:
            matrix_68x4[:, col_idx] = z_spiking[mask, :].mean(axis=0)

    # Build CSV.
    rows: list[dict[str, object]] = []
    for row_idx, name in enumerate(ALL_PARAM_NAMES):
        rows.append(
            {
                PARAMETER_COLUMN: name,
                **{
                    corner_label: float(matrix_68x4[row_idx, col_idx])
                    for col_idx, corner_label in enumerate(CORNER_LABELS)
                },
            }
        )

    # Footer rows for per-corner cell counts and per-corner mean of (MI, ATP, DSI, PD).
    footer_rows: list[dict[str, object]] = []
    cell_count_row: dict[str, object] = {PARAMETER_COLUMN: "__cell_count__"}
    mi_mean_row: dict[str, object] = {PARAMETER_COLUMN: "__mean_mi_count_bits__"}
    atp_mean_row: dict[str, object] = {PARAMETER_COLUMN: "__mean_atp_per_spike_molecules__"}
    dsi_mean_row: dict[str, object] = {PARAMETER_COLUMN: "__mean_dsi_vector_sum__"}
    pd_mean_row: dict[str, object] = {PARAMETER_COLUMN: "__mean_pd_rate_hz__"}
    for corner_label in CORNER_LABELS:
        mask: NDArray[np.bool_] = corner_labels_arr == corner_label
        n_cells: int = int(mask.sum())
        cell_count_row[corner_label] = n_cells
        if n_cells > 0:
            mi_mean_row[corner_label] = float(df_spiking.loc[mask, MI_COLUMN].mean())
            atp_mean_row[corner_label] = float(df_spiking.loc[mask, ATP_PER_SPIKE_COLUMN].mean())
            dsi_mean_row[corner_label] = float(df_spiking.loc[mask, DSI_COLUMN].mean())
            pd_mean_row[corner_label] = float(df_spiking.loc[mask, PD_COLUMN].mean())
        else:
            mi_mean_row[corner_label] = float("nan")
            atp_mean_row[corner_label] = float("nan")
            dsi_mean_row[corner_label] = float("nan")
            pd_mean_row[corner_label] = float("nan")
    footer_rows.extend([cell_count_row, mi_mean_row, atp_mean_row, dsi_mean_row, pd_mean_row])

    out_df: pd.DataFrame = pd.DataFrame(rows + footer_rows)
    CORNER_PARAM_MEANS_CSV.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(CORNER_PARAM_MEANS_CSV, index=False)
    print(f"Wrote {CORNER_PARAM_MEANS_CSV} (n_rows={len(out_df)})", flush=True)

    # Plot.
    vmax: float = float(np.nanmax(np.abs(matrix_68x4)))
    fig, ax = plt.subplots(figsize=(8, 0.18 * len(ALL_PARAM_NAMES) + 1), dpi=CHART_DPI)
    im = ax.imshow(matrix_68x4, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(CORNER_LABELS)))
    ax.set_xticklabels(list(CORNER_LABELS), rotation=30, ha="right")
    ax.set_yticks(range(len(ALL_PARAM_NAMES)))
    ax.set_yticklabels(ALL_PARAM_NAMES, fontsize=6)
    ax.set_title(
        f"68 x 4 parameter z-score means by MI x ATP corner (spiking cohort n={len(df_spiking)})"
    )
    plt.colorbar(im, ax=ax, label="mean z-score (full-cohort standardiser)")
    fig.tight_layout()
    CORNER_PARAM_HEATMAP_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(CORNER_PARAM_HEATMAP_PNG, dpi=CHART_DPI)
    plt.close(fig)
    print(f"Wrote {CORNER_PARAM_HEATMAP_PNG}", flush=True)


if __name__ == "__main__":
    main()
