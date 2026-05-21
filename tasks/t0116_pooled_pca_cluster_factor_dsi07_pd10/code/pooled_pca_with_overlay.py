"""Fit three PCAs on the union-pool (combined / electrophys / morphology), render the 1x3 PCA
figure and the gen-0 overlay figure, persist the fitted PCAs for reuse downstream, and emit
per-seed Euclidean displacement table comparing NSGA-II survivors to gen-0 random init.

Inputs:
    data/pooled_survivors.parquet
    data/pooled_gen0.parquet
    data/pooled_standardiser.npz

Outputs:
    data/pca_models.pkl
    results/images/pca_combined.png
    results/images/pca_with_gen0_overlay.png
    results/data/gen0_displacement.csv

Usage:
    uv run python -u -m \
        tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.pooled_pca_with_overlay
"""

from __future__ import annotations

import pickle
from dataclasses import dataclass

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.typing import NDArray
from sklearn.decomposition import PCA

from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.cluster_helpers import (
    PooledStandardiser,
    load_standardiser,
)
from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.constants import (
    ALL_PARAM_NAMES,
    CHART_DPI,
    KMEANS_RANDOM_STATE,
    N_ELECTROPHYS_DIMS,
    N_MORPHOLOGY_DIMS,
    SEED_COLORS,
    SOURCES,
)
from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.paths import (
    GEN0_DISPLACEMENT_CSV,
    PCA_COMBINED_PNG,
    PCA_MODELS_PKL,
    PCA_WITH_GEN0_OVERLAY_PNG,
    POOLED_GEN0_PARQUET,
    POOLED_STANDARDISER_NPZ,
    POOLED_SURVIVORS_PARQUET,
)

SEED_COLUMN: str = "seed"


@dataclass(frozen=True, slots=True)
class PCABundle:
    """The three union-pool PCAs needed by every downstream chart."""

    pca_combined: PCA  # 68-d -> 2 components
    pca_ephys: PCA  # 54-d -> 2 components
    pca_morph: PCA  # 14-d -> 2 components
    pca_ephys_3d: PCA  # 54-d -> 3 components (for morphology-cluster representative tables)


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


def _scatter_survivors_by_seed(
    *,
    ax: plt.Axes,
    scores: NDArray[np.float64],
    seeds: NDArray[np.int_],
) -> None:
    for seed_idx, (source_task, seed, _) in enumerate(SOURCES):
        mask: NDArray[np.bool_] = seeds == int(seed)
        if mask.sum() == 0:
            continue
        ax.scatter(
            scores[mask, 0],
            scores[mask, 1],
            s=24,
            color=SEED_COLORS[seed_idx],
            alpha=0.75,
            edgecolors="black",
            linewidths=0.3,
            marker="o",
            label=f"{source_task} (seed {seed}, n={int(mask.sum())})",
            zorder=2,
        )


def _scatter_gen0_by_seed(
    *,
    ax: plt.Axes,
    scores: NDArray[np.float64],
    seeds: NDArray[np.int_],
) -> None:
    for seed_idx, (_, seed, _) in enumerate(SOURCES):
        mask: NDArray[np.bool_] = seeds == int(seed)
        if mask.sum() == 0:
            continue
        ax.scatter(
            scores[mask, 0],
            scores[mask, 1],
            s=24,
            color=SEED_COLORS[seed_idx],
            alpha=0.3,
            edgecolors="none",
            marker="x",
            linewidths=0.8,
            zorder=1,
        )


def _render_pca_combined(
    *,
    bundle: PCABundle,
    scores_combined: NDArray[np.float64],
    scores_ephys: NDArray[np.float64],
    scores_morph: NDArray[np.float64],
    seeds: NDArray[np.int_],
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), dpi=CHART_DPI)
    _scatter_survivors_by_seed(ax=axes[0], scores=scores_combined, seeds=seeds)
    axes[0].set_xlabel(_label_with_pct(prefix="PC1", pca=bundle.pca_combined, idx=0))
    axes[0].set_ylabel(_label_with_pct(prefix="PC2", pca=bundle.pca_combined, idx=1))
    axes[0].set_title("Combined 68-d PCA")
    axes[0].grid(True, alpha=0.3)

    _scatter_survivors_by_seed(ax=axes[1], scores=scores_ephys, seeds=seeds)
    axes[1].set_xlabel(_label_with_pct(prefix="PC1", pca=bundle.pca_ephys, idx=0))
    axes[1].set_ylabel(_label_with_pct(prefix="PC2", pca=bundle.pca_ephys, idx=1))
    axes[1].set_title("Electrophys-only 54-d PCA")
    axes[1].grid(True, alpha=0.3)

    _scatter_survivors_by_seed(ax=axes[2], scores=scores_morph, seeds=seeds)
    axes[2].set_xlabel(_label_with_pct(prefix="PC1", pca=bundle.pca_morph, idx=0))
    axes[2].set_ylabel(_label_with_pct(prefix="PC2", pca=bundle.pca_morph, idx=1))
    axes[2].set_title("Morphology-only 14-d PCA")
    axes[2].grid(True, alpha=0.3)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=9, frameon=False)
    fig.suptitle(
        "Pooled DSI > 0.7 ∧ PD > 10 Hz cohort across 4 seeds — PC1 vs PC2",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 0.96))
    PCA_COMBINED_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PCA_COMBINED_PNG, dpi=CHART_DPI)
    plt.close(fig)
    print(f"Wrote {PCA_COMBINED_PNG}", flush=True)


def _render_pca_with_gen0_overlay(
    *,
    bundle: PCABundle,
    scores_combined: NDArray[np.float64],
    scores_ephys: NDArray[np.float64],
    scores_morph: NDArray[np.float64],
    seeds: NDArray[np.int_],
    gen0_scores_combined: NDArray[np.float64],
    gen0_scores_ephys: NDArray[np.float64],
    gen0_scores_morph: NDArray[np.float64],
    gen0_seeds: NDArray[np.int_],
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), dpi=CHART_DPI)
    # Gen-0 first (zorder=1), then survivors on top (zorder=2).
    _scatter_gen0_by_seed(ax=axes[0], scores=gen0_scores_combined, seeds=gen0_seeds)
    _scatter_survivors_by_seed(ax=axes[0], scores=scores_combined, seeds=seeds)
    axes[0].set_xlabel(_label_with_pct(prefix="PC1", pca=bundle.pca_combined, idx=0))
    axes[0].set_ylabel(_label_with_pct(prefix="PC2", pca=bundle.pca_combined, idx=1))
    axes[0].set_title("Combined 68-d PCA (survivors o, gen-0 x)")
    axes[0].grid(True, alpha=0.3)

    _scatter_gen0_by_seed(ax=axes[1], scores=gen0_scores_ephys, seeds=gen0_seeds)
    _scatter_survivors_by_seed(ax=axes[1], scores=scores_ephys, seeds=seeds)
    axes[1].set_xlabel(_label_with_pct(prefix="PC1", pca=bundle.pca_ephys, idx=0))
    axes[1].set_ylabel(_label_with_pct(prefix="PC2", pca=bundle.pca_ephys, idx=1))
    axes[1].set_title("Electrophys 54-d PCA (survivors o, gen-0 x)")
    axes[1].grid(True, alpha=0.3)

    _scatter_gen0_by_seed(ax=axes[2], scores=gen0_scores_morph, seeds=gen0_seeds)
    _scatter_survivors_by_seed(ax=axes[2], scores=scores_morph, seeds=seeds)
    axes[2].set_xlabel(_label_with_pct(prefix="PC1", pca=bundle.pca_morph, idx=0))
    axes[2].set_ylabel(_label_with_pct(prefix="PC2", pca=bundle.pca_morph, idx=1))
    axes[2].set_title("Morphology 14-d PCA (survivors o, gen-0 x)")
    axes[2].grid(True, alpha=0.3)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=9, frameon=False)
    fig.suptitle(
        "Pooled DSI > 0.7 ∧ PD > 10 Hz cohort vs gen-0 random init (4 seeds)",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 0.96))
    PCA_WITH_GEN0_OVERLAY_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PCA_WITH_GEN0_OVERLAY_PNG, dpi=CHART_DPI)
    plt.close(fig)
    print(f"Wrote {PCA_WITH_GEN0_OVERLAY_PNG}", flush=True)


def _compute_displacement_table(
    *,
    survivor_pc12: NDArray[np.float64],
    survivor_z68: NDArray[np.float64],
    survivor_seeds: NDArray[np.int_],
    gen0_pc12: NDArray[np.float64],
    gen0_z68: NDArray[np.float64],
    gen0_seeds: NDArray[np.int_],
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for _, seed, _ in SOURCES:
        seed_i: int = int(seed)
        s_mask: NDArray[np.bool_] = survivor_seeds == seed_i
        g_mask: NDArray[np.bool_] = gen0_seeds == seed_i
        n_surv: int = int(s_mask.sum())
        n_gen0: int = int(g_mask.sum())
        if n_surv == 0 or n_gen0 == 0:
            mean_pc12: float = float("nan")
            mean_z68: float = float("nan")
            p95_pc12: float = float("nan")
            p95_z68: float = float("nan")
        else:
            gen0_mean_pc12: NDArray[np.float64] = gen0_pc12[g_mask].mean(axis=0)
            gen0_mean_z68: NDArray[np.float64] = gen0_z68[g_mask].mean(axis=0)
            disp_pc12: NDArray[np.float64] = np.linalg.norm(
                survivor_pc12[s_mask] - gen0_mean_pc12[None, :], axis=1
            )
            disp_z68: NDArray[np.float64] = np.linalg.norm(
                survivor_z68[s_mask] - gen0_mean_z68[None, :], axis=1
            )
            mean_pc12 = float(disp_pc12.mean())
            mean_z68 = float(disp_z68.mean())
            p95_pc12 = float(np.percentile(disp_pc12, 95))
            p95_z68 = float(np.percentile(disp_z68, 95))
        rows.append(
            {
                "seed": seed_i,
                "mean_disp_pc12": mean_pc12,
                "mean_disp_68d": mean_z68,
                "p95_disp_pc12": p95_pc12,
                "p95_disp_68d": p95_z68,
                "n_survivors": n_surv,
                "n_gen0": n_gen0,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    df_surv: pd.DataFrame = pd.read_parquet(POOLED_SURVIVORS_PARQUET)
    df_gen0: pd.DataFrame = pd.read_parquet(POOLED_GEN0_PARQUET)
    standardiser: PooledStandardiser = load_standardiser(path=POOLED_STANDARDISER_NPZ)
    print(
        f"Loaded {len(df_surv)} survivors, {len(df_gen0)} gen-0 rows, "
        f"standardiser mean.shape={standardiser.mean.shape}",
        flush=True,
    )

    surv_matrix: NDArray[np.float64] = df_surv[list(ALL_PARAM_NAMES)].to_numpy(dtype=np.float64)
    z_surv: NDArray[np.float64] = standardiser.transform(surv_matrix)
    seeds_surv: NDArray[np.int_] = df_surv[SEED_COLUMN].to_numpy(dtype=np.int_)

    bundle: PCABundle = _fit_pcas(z_full=z_surv)

    # Print variance-explained percentages.
    print("\nVariance explained per PCA:")
    print(
        f"  combined PCA: PC1={bundle.pca_combined.explained_variance_ratio_[0]:.4f} "
        f"PC2={bundle.pca_combined.explained_variance_ratio_[1]:.4f} "
        f"(cumulative={float(bundle.pca_combined.explained_variance_ratio_.sum()):.4f})",
        flush=True,
    )
    print(
        f"  ephys PCA: PC1={bundle.pca_ephys.explained_variance_ratio_[0]:.4f} "
        f"PC2={bundle.pca_ephys.explained_variance_ratio_[1]:.4f}",
        flush=True,
    )
    print(
        f"  morph PCA: PC1={bundle.pca_morph.explained_variance_ratio_[0]:.4f} "
        f"PC2={bundle.pca_morph.explained_variance_ratio_[1]:.4f}",
        flush=True,
    )
    ephys_3d_cum: float = float(bundle.pca_ephys_3d.explained_variance_ratio_.sum())
    print(f"  ephys 3d: PCs cumulative={ephys_3d_cum:.4f}", flush=True)

    # Project survivors onto the three 2-component PCAs.
    scores_combined: NDArray[np.float64] = bundle.pca_combined.transform(z_surv)
    scores_ephys: NDArray[np.float64] = bundle.pca_ephys.transform(z_surv[:, :N_ELECTROPHYS_DIMS])
    scores_morph: NDArray[np.float64] = bundle.pca_morph.transform(z_surv[:, N_ELECTROPHYS_DIMS:])
    assert scores_combined.shape == (len(z_surv), 2)

    _render_pca_combined(
        bundle=bundle,
        scores_combined=scores_combined,
        scores_ephys=scores_ephys,
        scores_morph=scores_morph,
        seeds=seeds_surv,
    )

    # Persist PCAs for use by Step 7 + Step 9.
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

    # Step 6: gen-0 overlay.
    gen0_matrix: NDArray[np.float64] = df_gen0[list(ALL_PARAM_NAMES)].to_numpy(dtype=np.float64)
    z_gen0: NDArray[np.float64] = standardiser.transform(gen0_matrix)
    seeds_gen0: NDArray[np.int_] = df_gen0[SEED_COLUMN].to_numpy(dtype=np.int_)

    gen0_scores_combined: NDArray[np.float64] = bundle.pca_combined.transform(z_gen0)
    gen0_scores_ephys: NDArray[np.float64] = bundle.pca_ephys.transform(
        z_gen0[:, :N_ELECTROPHYS_DIMS]
    )
    gen0_scores_morph: NDArray[np.float64] = bundle.pca_morph.transform(
        z_gen0[:, N_ELECTROPHYS_DIMS:]
    )

    _render_pca_with_gen0_overlay(
        bundle=bundle,
        scores_combined=scores_combined,
        scores_ephys=scores_ephys,
        scores_morph=scores_morph,
        seeds=seeds_surv,
        gen0_scores_combined=gen0_scores_combined,
        gen0_scores_ephys=gen0_scores_ephys,
        gen0_scores_morph=gen0_scores_morph,
        gen0_seeds=seeds_gen0,
    )

    # Displacement table.
    disp_df: pd.DataFrame = _compute_displacement_table(
        survivor_pc12=scores_combined,
        survivor_z68=z_surv,
        survivor_seeds=seeds_surv,
        gen0_pc12=gen0_scores_combined,
        gen0_z68=z_gen0,
        gen0_seeds=seeds_gen0,
    )
    GEN0_DISPLACEMENT_CSV.parent.mkdir(parents=True, exist_ok=True)
    disp_df.to_csv(GEN0_DISPLACEMENT_CSV, index=False)
    print(f"\nWrote {GEN0_DISPLACEMENT_CSV}", flush=True)
    print(disp_df.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
