"""Render a 5x3 grid of full dendrite trees for the top 15 representatives of each electrophys
KMeans cluster. Representatives ranked descending by `dsi * pd_rate_hz` within cluster (the
canonical rule from t0109's `_select_top_per_cluster`).

Inputs:
    results/data/electrophys_clusters.csv
    data/pooled_survivors.parquet

Outputs:
    results/images/electrophys_cluster_<cluster_id>_morphs.png  (one per cluster id)

Usage:
    uv run python -u -m \
        tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.render_electrophys_cluster_morphs
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.constants import (
    ALL_PARAM_NAMES,
    CHART_DPI,
    N_REPRESENTATIVES_PER_CLUSTER,
)
from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.morphology_rendering import (
    BuiltMorph,
    CellLabel,
    build_and_extract,
    global_extents,
    plot_cell,
    to_morph_params,
)
from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.paths import (
    ELECTROPHYS_CLUSTERS_CSV,
    POOLED_SURVIVORS_PARQUET,
    electrophys_cluster_morphs_png,
)

SOURCE_TASK_COLUMN: str = "source_task"
SEED_COLUMN: str = "seed"
GENERATION_COLUMN: str = "generation"
INDIVIDUAL_IDX_COLUMN: str = "individual_idx"
DSI_COLUMN: str = "dsi_vector_sum"
PD_COLUMN: str = "pd_rate_hz"
CLUSTER_ID_COLUMN: str = "cluster_id"

N_ROWS_GRID: int = 5
N_COLS_GRID: int = 3
PANEL_W_IN: float = 2.6
PANEL_H_IN: float = 2.8


def _select_top_per_cluster(
    *,
    df_with_clusters: pd.DataFrame,
    n_per_cluster: int,
) -> dict[int, pd.DataFrame]:
    df_sorted: pd.DataFrame = df_with_clusters.assign(
        _rank_score=df_with_clusters[DSI_COLUMN] * df_with_clusters[PD_COLUMN]
    ).sort_values(by="_rank_score", ascending=False)
    out: dict[int, pd.DataFrame] = {}
    for cluster_id, group in df_sorted.groupby(CLUSTER_ID_COLUMN, sort=True):
        out[int(cluster_id)] = group.head(n_per_cluster).reset_index(drop=True)
    return out


def _render_cluster_grid(
    *,
    cluster_id: int,
    cluster_df: pd.DataFrame,
    cluster_size_total: int,
    output_path: Path,
) -> None:
    n_panels: int = N_ROWS_GRID * N_COLS_GRID
    fig, axes_2d = plt.subplots(
        N_ROWS_GRID,
        N_COLS_GRID,
        figsize=(N_COLS_GRID * PANEL_W_IN, N_ROWS_GRID * PANEL_H_IN),
        dpi=CHART_DPI,
    )

    # Build all cells first so we can normalise axes to a common extent.
    built_per_panel: dict[int, BuiltMorph | None] = {}
    label_per_panel: dict[int, CellLabel | None] = {}
    all_built: list[BuiltMorph] = []
    for i in range(n_panels):
        if i >= len(cluster_df):
            built_per_panel[i] = None
            label_per_panel[i] = None
            continue
        row: pd.Series[float] = cluster_df.iloc[i]
        vec: tuple[float, ...] = tuple(float(row[name]) for name in ALL_PARAM_NAMES)
        label = CellLabel(
            source_task=str(row[SOURCE_TASK_COLUMN]),
            seed=int(row[SEED_COLUMN]),
            generation=int(row[GENERATION_COLUMN]),
            dsi=float(row[DSI_COLUMN]),
            pd_rate_hz=float(row[PD_COLUMN]),
        )
        print(
            f"  cluster {cluster_id} cell {i + 1}/{min(n_panels, len(cluster_df))}: "
            f"{label.source_task}/s{label.seed} gen={label.generation} "
            f"DSI={label.dsi:.3f} PD={label.pd_rate_hz:.1f} ...",
            flush=True,
        )
        try:
            params = to_morph_params(vec=vec)
            built: BuiltMorph = build_and_extract(params=params)
            built_per_panel[i] = built
            label_per_panel[i] = label
            all_built.append(built)
        except (RuntimeError, ValueError, AssertionError) as exc:
            print(f"    FAILED ({type(exc).__name__}): {exc}", flush=True)
            built_per_panel[i] = None
            label_per_panel[i] = label

    xlo: float = 0.0
    xhi: float = 1.0
    ylo: float = 0.0
    yhi: float = 1.0
    if len(all_built) > 0:
        xlo, xhi, ylo, yhi = global_extents(all_built)

    for i in range(n_panels):
        row_idx, col_idx = divmod(i, N_COLS_GRID)
        ax: plt.Axes = axes_2d[row_idx, col_idx]
        built = built_per_panel[i]
        label = label_per_panel[i]
        if built is None:
            if label is not None:
                ax.text(
                    0.5,
                    0.5,
                    "build\nfailed",
                    ha="center",
                    va="center",
                    transform=ax.transAxes,
                    fontsize=8,
                )
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_aspect("equal")
            continue
        assert label is not None
        plot_cell(ax=ax, built=built, label=label)
        ax.set_xlim(xlo, xhi)
        ax.set_ylim(ylo, yhi)

    fig.suptitle(
        f"Electrophys cluster {cluster_id} — top {len(cluster_df)} by DSI*PD "
        f"(cluster size n={cluster_size_total})",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)
    print(f"Wrote {output_path}", flush=True)


def main() -> None:
    clusters_df: pd.DataFrame = pd.read_csv(ELECTROPHYS_CLUSTERS_CSV)
    pool_df: pd.DataFrame = pd.read_parquet(POOLED_SURVIVORS_PARQUET)

    join_keys: list[str] = [
        SOURCE_TASK_COLUMN,
        SEED_COLUMN,
        GENERATION_COLUMN,
        INDIVIDUAL_IDX_COLUMN,
    ]
    # The clusters CSV has dsi_vector_sum / pd_rate_hz / pc1_combined / pc2_combined which would
    # conflict with the pool merge; drop the overlapping pool columns before join.
    pool_df_no_overlap: pd.DataFrame = pool_df.drop(columns=[DSI_COLUMN, PD_COLUMN])
    joined: pd.DataFrame = clusters_df.merge(
        pool_df_no_overlap,
        on=join_keys,
        how="left",
        validate="one_to_one",
    )
    assert len(joined) == len(clusters_df), (
        f"join mismatch: clusters={len(clusters_df)}, joined={len(joined)}"
    )
    assert joined[list(ALL_PARAM_NAMES)].isna().sum().sum() == 0, (
        "missing vector columns after join"
    )

    cluster_sizes: pd.Series[int] = joined.groupby(CLUSTER_ID_COLUMN).size()
    print(f"Cluster sizes total: {cluster_sizes.to_dict()}", flush=True)

    picks_by_cluster: dict[int, pd.DataFrame] = _select_top_per_cluster(
        df_with_clusters=joined,
        n_per_cluster=N_REPRESENTATIVES_PER_CLUSTER,
    )

    cluster_ids: list[int] = sorted(picks_by_cluster.keys())
    n_morphs_built: int = 0
    for cid in cluster_ids:
        cdf: pd.DataFrame = picks_by_cluster[cid]
        size_total: int = int(cluster_sizes.get(cid, 0))
        out_path: Path = electrophys_cluster_morphs_png(cluster_id=cid)
        _render_cluster_grid(
            cluster_id=cid,
            cluster_df=cdf,
            cluster_size_total=size_total,
            output_path=out_path,
        )
        n_morphs_built += min(N_REPRESENTATIVES_PER_CLUSTER, len(cdf))
    print(f"\nBuilt {n_morphs_built} morphologies across {len(cluster_ids)} clusters", flush=True)


if __name__ == "__main__":
    main()
