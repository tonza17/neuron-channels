"""Fit three PCAs (combined / electrophys / morphology) on the full cohort, render four PCA
figures (coloured by MI, by ATP-log10, by MI x ATP corner, and a gen-0 overlay), persist the
fitted PCAs, and write the gen-0 displacement table segmented by corner.

Inputs:
    data/t0125_cells.parquet
    data/t0125_gen0.parquet
    data/t0125_standardiser.npz
    results/data/group_thresholds.json

Outputs:
    data/pca_models.pkl
    results/images/pca_combined_color_mi.png
    results/images/pca_combined_color_atp.png
    results/images/pca_combined_color_corner.png
    results/images/pca_with_gen0_overlay.png
    results/data/gen0_displacement.csv
"""

from __future__ import annotations

import json
import pickle
from dataclasses import dataclass

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm, Normalize
from numpy.typing import NDArray
from sklearn.decomposition import PCA

from tasks.t0125_t0123_cluster_factor_mi_atp.code.cluster_helpers import (
    PooledStandardiser,
    load_standardiser,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.constants import (
    ALL_PARAM_NAMES,
    CHART_DPI,
    CORNER_COLORS,
    CORNER_LABELS,
    KMEANS_RANDOM_STATE,
    N_ELECTROPHYS_DIMS,
    N_MORPHOLOGY_DIMS,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.group_thresholds import (
    GroupThresholds,
    assign_corner_label,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.load_t0123_cells import (
    ATP_PER_SPIKE_COLUMN,
    MI_COLUMN,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.paths import (
    GEN0_DISPLACEMENT_CSV,
    GROUP_THRESHOLDS_JSON,
    PCA_COMBINED_COLOR_ATP_PNG,
    PCA_COMBINED_COLOR_CORNER_PNG,
    PCA_COMBINED_COLOR_MI_PNG,
    PCA_MODELS_PKL,
    PCA_WITH_GEN0_OVERLAY_PNG,
    T0123_CELLS_PARQUET,
    T0123_GEN0_PARQUET,
    T0123_STANDARDISER_NPZ,
)


@dataclass(frozen=True, slots=True)
class PCABundle:
    """The three union-pool PCAs needed by every downstream chart."""

    pca_combined: PCA  # 68-d -> 2 components
    pca_ephys: PCA  # 54-d -> 2 components
    pca_morph: PCA  # 14-d -> 2 components
    pca_ephys_3d: PCA  # 54-d -> 3 components


def _fit_pcas(*, z_full: NDArray[np.float64]) -> PCABundle:
    z_ephys: NDArray[np.float64] = z_full[:, :N_ELECTROPHYS_DIMS]
    z_morph: NDArray[np.float64] = z_full[:, N_ELECTROPHYS_DIMS:]
    assert z_morph.shape[1] == N_MORPHOLOGY_DIMS

    pca_combined: PCA = PCA(n_components=2, random_state=KMEANS_RANDOM_STATE).fit(z_full)
    pca_ephys: PCA = PCA(n_components=2, random_state=KMEANS_RANDOM_STATE).fit(z_ephys)
    pca_morph: PCA = PCA(n_components=2, random_state=KMEANS_RANDOM_STATE).fit(z_morph)
    pca_ephys_3d: PCA = PCA(n_components=3, random_state=KMEANS_RANDOM_STATE).fit(z_ephys)
    return PCABundle(
        pca_combined=pca_combined,
        pca_ephys=pca_ephys,
        pca_morph=pca_morph,
        pca_ephys_3d=pca_ephys_3d,
    )


def _label_with_pct(*, prefix: str, pca: PCA, idx: int) -> str:
    pct: float = 100.0 * float(pca.explained_variance_ratio_[idx])
    return f"{prefix} ({pct:.1f}%)"


def _scatter_cells_by_value(
    *,
    ax: plt.Axes,
    scores: NDArray[np.float64],
    value: NDArray[np.float64],
    cmap: str,
    norm: Normalize | LogNorm | None = None,
    cbar_label: str = "",
) -> None:
    sc = ax.scatter(
        scores[:, 0],
        scores[:, 1],
        c=value,
        s=8,
        cmap=cmap,
        alpha=0.7,
        edgecolors="none",
        norm=norm,
    )
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label(cbar_label, fontsize=8)


def _scatter_cells_by_corner(
    *,
    ax: plt.Axes,
    scores: NDArray[np.float64],
    corner_labels_arr: NDArray[np.str_],
) -> None:
    for color, corner_label in zip(CORNER_COLORS, CORNER_LABELS, strict=True):
        mask: NDArray[np.bool_] = corner_labels_arr == corner_label
        if mask.sum() == 0:
            continue
        ax.scatter(
            scores[mask, 0],
            scores[mask, 1],
            s=10,
            color=color,
            alpha=0.6,
            edgecolors="none",
            label=f"{corner_label} (n={int(mask.sum())})",
        )


def _render_three_panel_continuous(
    *,
    bundle: PCABundle,
    scores_combined: NDArray[np.float64],
    scores_ephys: NDArray[np.float64],
    scores_morph: NDArray[np.float64],
    value: NDArray[np.float64],
    cmap: str,
    suptitle: str,
    cbar_label: str,
    output_path,
    log_scale: bool = False,
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=CHART_DPI)
    norm: Normalize | LogNorm | None = None
    if log_scale:
        positive_value: NDArray[np.float64] = np.where(value > 0, value, np.nan)
        vmin: float = float(np.nanmin(positive_value))
        vmax: float = float(np.nanmax(positive_value))
        norm = LogNorm(vmin=vmin, vmax=vmax)
    for ax, scores, pca, title in zip(
        axes,
        [scores_combined, scores_ephys, scores_morph],
        [bundle.pca_combined, bundle.pca_ephys, bundle.pca_morph],
        ["Combined 68-d PCA", "Electrophys-only 54-d PCA", "Morphology-only 14-d PCA"],
        strict=True,
    ):
        _scatter_cells_by_value(
            ax=ax,
            scores=scores,
            value=value,
            cmap=cmap,
            norm=norm,
            cbar_label=cbar_label,
        )
        ax.set_xlabel(_label_with_pct(prefix="PC1", pca=pca, idx=0))
        ax.set_ylabel(_label_with_pct(prefix="PC2", pca=pca, idx=1))
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
    fig.suptitle(suptitle, fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)
    print(f"Wrote {output_path}", flush=True)


def _render_three_panel_corner(
    *,
    bundle: PCABundle,
    scores_combined: NDArray[np.float64],
    scores_ephys: NDArray[np.float64],
    scores_morph: NDArray[np.float64],
    corner_labels_arr: NDArray[np.str_],
    suptitle: str,
    output_path,
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=CHART_DPI)
    for ax, scores, pca, title in zip(
        axes,
        [scores_combined, scores_ephys, scores_morph],
        [bundle.pca_combined, bundle.pca_ephys, bundle.pca_morph],
        ["Combined 68-d PCA", "Electrophys-only 54-d PCA", "Morphology-only 14-d PCA"],
        strict=True,
    ):
        _scatter_cells_by_corner(ax=ax, scores=scores, corner_labels_arr=corner_labels_arr)
        ax.set_xlabel(_label_with_pct(prefix="PC1", pca=pca, idx=0))
        ax.set_ylabel(_label_with_pct(prefix="PC2", pca=pca, idx=1))
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=9, frameon=False)
    fig.suptitle(suptitle, fontsize=12)
    fig.tight_layout(rect=(0, 0.06, 1, 0.96))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)
    print(f"Wrote {output_path}", flush=True)


def _render_gen0_overlay(
    *,
    bundle: PCABundle,
    scores_combined: NDArray[np.float64],
    scores_ephys: NDArray[np.float64],
    scores_morph: NDArray[np.float64],
    gen0_scores_combined: NDArray[np.float64],
    gen0_scores_ephys: NDArray[np.float64],
    gen0_scores_morph: NDArray[np.float64],
    corner_labels_arr: NDArray[np.str_],
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=CHART_DPI)
    for ax, scores, gen0_scores, pca, title in zip(
        axes,
        [scores_combined, scores_ephys, scores_morph],
        [gen0_scores_combined, gen0_scores_ephys, gen0_scores_morph],
        [bundle.pca_combined, bundle.pca_ephys, bundle.pca_morph],
        ["Combined 68-d PCA", "Electrophys 54-d PCA", "Morphology 14-d PCA"],
        strict=True,
    ):
        _scatter_cells_by_corner(ax=ax, scores=scores, corner_labels_arr=corner_labels_arr)
        ax.scatter(
            gen0_scores[:, 0],
            gen0_scores[:, 1],
            s=40,
            color="#000000",
            alpha=0.8,
            marker="x",
            linewidths=1.0,
            label=f"gen-0 (n={len(gen0_scores)})",
            zorder=5,
        )
        ax.set_xlabel(_label_with_pct(prefix="PC1", pca=pca, idx=0))
        ax.set_ylabel(_label_with_pct(prefix="PC2", pca=pca, idx=1))
        ax.set_title(title + " (cells o by corner; gen-0 x)")
        ax.grid(True, alpha=0.3)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=5, fontsize=9, frameon=False)
    fig.suptitle(
        "t0123 full cohort vs gen-0 random init (cells coloured by MI x ATP corner)",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 0.96))
    PCA_WITH_GEN0_OVERLAY_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PCA_WITH_GEN0_OVERLAY_PNG, dpi=CHART_DPI)
    plt.close(fig)
    print(f"Wrote {PCA_WITH_GEN0_OVERLAY_PNG}", flush=True)


def _compute_displacement_table(
    *,
    cell_pc12: NDArray[np.float64],
    cell_z68: NDArray[np.float64],
    cell_corner_labels: NDArray[np.str_],
    gen0_pc12: NDArray[np.float64],
    gen0_z68: NDArray[np.float64],
) -> pd.DataFrame:
    """One row per partition: overall + one per corner.

    Displacement is Euclidean distance from each cell to the mean gen-0 position (PC1+PC2 or 68-d).
    """
    rows: list[dict[str, object]] = []
    gen0_mean_pc12: NDArray[np.float64] = gen0_pc12.mean(axis=0)
    gen0_mean_z68: NDArray[np.float64] = gen0_z68.mean(axis=0)

    def _row(*, partition: str, idx_mask: NDArray[np.bool_]) -> dict[str, object]:
        if int(idx_mask.sum()) == 0:
            return {
                "partition": partition,
                "n_cells": 0,
                "mean_pc12_displacement": float("nan"),
                "p95_pc12_displacement": float("nan"),
                "mean_68d_displacement": float("nan"),
                "p95_68d_displacement": float("nan"),
            }
        disp_pc12: NDArray[np.float64] = np.linalg.norm(
            cell_pc12[idx_mask] - gen0_mean_pc12[None, :], axis=1
        )
        disp_z68: NDArray[np.float64] = np.linalg.norm(
            cell_z68[idx_mask] - gen0_mean_z68[None, :], axis=1
        )
        return {
            "partition": partition,
            "n_cells": int(idx_mask.sum()),
            "mean_pc12_displacement": float(disp_pc12.mean()),
            "p95_pc12_displacement": float(np.percentile(disp_pc12, 95)),
            "mean_68d_displacement": float(disp_z68.mean()),
            "p95_68d_displacement": float(np.percentile(disp_z68, 95)),
        }

    overall_mask: NDArray[np.bool_] = np.ones(len(cell_pc12), dtype=bool)
    rows.append(_row(partition="overall", idx_mask=overall_mask))
    for corner_label in CORNER_LABELS:
        mask: NDArray[np.bool_] = cell_corner_labels == corner_label
        rows.append(_row(partition=corner_label, idx_mask=mask))
    return pd.DataFrame(rows)


def main() -> None:
    df_full: pd.DataFrame = pd.read_parquet(T0123_CELLS_PARQUET)
    df_gen0: pd.DataFrame = pd.read_parquet(T0123_GEN0_PARQUET)
    standardiser: PooledStandardiser = load_standardiser(path=T0123_STANDARDISER_NPZ)
    print(
        f"Loaded {len(df_full)} cells, {len(df_gen0)} gen-0 rows",
        flush=True,
    )

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

    matrix_68d: NDArray[np.float64] = df_full[list(ALL_PARAM_NAMES)].to_numpy(dtype=np.float64)
    z_full: NDArray[np.float64] = standardiser.transform(matrix_68d)

    bundle: PCABundle = _fit_pcas(z_full=z_full)
    print(
        f"  combined PCA: PC1={bundle.pca_combined.explained_variance_ratio_[0]:.4f} "
        f"PC2={bundle.pca_combined.explained_variance_ratio_[1]:.4f}",
        flush=True,
    )

    scores_combined: NDArray[np.float64] = bundle.pca_combined.transform(z_full)
    scores_ephys: NDArray[np.float64] = bundle.pca_ephys.transform(z_full[:, :N_ELECTROPHYS_DIMS])
    scores_morph: NDArray[np.float64] = bundle.pca_morph.transform(z_full[:, N_ELECTROPHYS_DIMS:])

    # Compute MI and ATP colour values on the FULL cohort. For ATP, log10 scale.
    mi_values: NDArray[np.float64] = df_full[MI_COLUMN].to_numpy(dtype=np.float64)
    atp_values: NDArray[np.float64] = df_full[ATP_PER_SPIKE_COLUMN].to_numpy(dtype=np.float64)

    # Corner labels for the FULL cohort (median splits from spiking cohort).
    corner_labels_full: NDArray[np.str_] = np.array(
        [
            assign_corner_label(mi_val=float(m), atp_val=float(a), thresholds=thresholds)
            for m, a in zip(mi_values.tolist(), atp_values.tolist(), strict=True)
        ],
        dtype=str,
    )

    _render_three_panel_continuous(
        bundle=bundle,
        scores_combined=scores_combined,
        scores_ephys=scores_ephys,
        scores_morph=scores_morph,
        value=mi_values,
        cmap="viridis",
        suptitle="t0123 full cohort PCAs coloured by mi_count_bits (ceiling = log2(4) = 2 bits)",
        cbar_label="mi_count_bits",
        output_path=PCA_COMBINED_COLOR_MI_PNG,
        log_scale=False,
    )
    _render_three_panel_continuous(
        bundle=bundle,
        scores_combined=scores_combined,
        scores_ephys=scores_ephys,
        scores_morph=scores_morph,
        value=atp_values,
        cmap="viridis",
        suptitle="t0123 full cohort PCAs coloured by atp_per_spike_molecules (log10)",
        cbar_label="atp_per_spike (log10)",
        output_path=PCA_COMBINED_COLOR_ATP_PNG,
        log_scale=True,
    )
    _render_three_panel_corner(
        bundle=bundle,
        scores_combined=scores_combined,
        scores_ephys=scores_ephys,
        scores_morph=scores_morph,
        corner_labels_arr=corner_labels_full,
        suptitle="t0123 full cohort PCAs coloured by MI x ATP corner (median splits)",
        output_path=PCA_COMBINED_COLOR_CORNER_PNG,
    )

    # Persist PCAs for KMeans + morphology cluster steps.
    PCA_MODELS_PKL.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, PCA] = {
        "pca_combined": bundle.pca_combined,
        "pca_ephys": bundle.pca_ephys,
        "pca_morph": bundle.pca_morph,
        "pca_ephys_3d": bundle.pca_ephys_3d,
    }
    with open(PCA_MODELS_PKL, "wb") as fh:
        pickle.dump(payload, fh)
    print(f"Wrote {PCA_MODELS_PKL}", flush=True)

    # Gen-0 overlay.
    gen0_matrix: NDArray[np.float64] = df_gen0[list(ALL_PARAM_NAMES)].to_numpy(dtype=np.float64)
    z_gen0: NDArray[np.float64] = standardiser.transform(gen0_matrix)
    gen0_scores_combined: NDArray[np.float64] = bundle.pca_combined.transform(z_gen0)
    gen0_scores_ephys: NDArray[np.float64] = bundle.pca_ephys.transform(
        z_gen0[:, :N_ELECTROPHYS_DIMS]
    )
    gen0_scores_morph: NDArray[np.float64] = bundle.pca_morph.transform(
        z_gen0[:, N_ELECTROPHYS_DIMS:]
    )

    _render_gen0_overlay(
        bundle=bundle,
        scores_combined=scores_combined,
        scores_ephys=scores_ephys,
        scores_morph=scores_morph,
        gen0_scores_combined=gen0_scores_combined,
        gen0_scores_ephys=gen0_scores_ephys,
        gen0_scores_morph=gen0_scores_morph,
        corner_labels_arr=corner_labels_full,
    )

    disp_df: pd.DataFrame = _compute_displacement_table(
        cell_pc12=scores_combined,
        cell_z68=z_full,
        cell_corner_labels=corner_labels_full,
        gen0_pc12=gen0_scores_combined,
        gen0_z68=z_gen0,
    )
    GEN0_DISPLACEMENT_CSV.parent.mkdir(parents=True, exist_ok=True)
    disp_df.to_csv(GEN0_DISPLACEMENT_CSV, index=False)
    print(f"Wrote {GEN0_DISPLACEMENT_CSV}", flush=True)
    print(disp_df.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
