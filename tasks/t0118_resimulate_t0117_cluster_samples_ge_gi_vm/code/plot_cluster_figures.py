"""Render the 4 per-cluster trace grids and 1 cross-cluster median summary (REQ-12, REQ-13).

Per-cluster figure: 10 rows (cells, ascending DSI) x 3 columns (g_E, g_I, V_m). Each panel plots
PD (solid) and ND (dashed) traces. Panel annotation: ``(DSI=..., PD=... Hz)``.

Cross-cluster figure: 4 rows (clusters) x 3 columns (g_E, g_I, V_m). Each panel plots the pointwise
median trace over the 10 cells of that cluster.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.constants import (
    CLUSTER_ID_COL,
    CROSS_CLUSTER_FIGSIZE_INCHES,
    DSI_COL,
    EXPECTED_TRACE_ROWS,
    FIGURE_DPI,
    G_E_US_COL,
    G_I_US_COL,
    GENERATION_COL,
    INDIVIDUAL_IDX_COL,
    N_CLUSTERS,
    ND_LINESTYLE,
    PD_LINESTYLE,
    PD_RATE_COL,
    PER_CLUSTER_FIGSIZE_INCHES,
    SEED_COL,
    SOURCE_TASK_COL,
    T_MS_COL,
    TRACE_COLOR_BY_CLUSTER,
    V_M_MV_COL,
    Direction,
    TrialMode,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.paths import (
    CLUSTER_TRACES_FIGURE_TEMPLATE,
    CROSS_CLUSTER_FIGURE,
    RESULTS_IMAGES_DIR,
    SELECTED_CELLS_CSV,
    TRACES_ROOT,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.simulate_cell import (
    cell_key,
    trace_parquet_path,
)


def _load_trace_column(
    *,
    cluster_id: int,
    cell_key_str: str,
    mode: TrialMode,
    direction_deg: int,
    column: str,
) -> tuple[np.ndarray, np.ndarray] | None:
    """Return (t_ms, value) arrays if parquet exists and has the expected column; else None."""
    path: Path = trace_parquet_path(
        traces_root=TRACES_ROOT,
        cluster_id=cluster_id,
        cell_key_str=cell_key_str,
        mode=mode,
        direction_deg=direction_deg,
    )
    if not path.exists():
        return None
    df: pd.DataFrame = pd.read_parquet(path=path)
    if column not in df.columns:
        return None
    return df[T_MS_COL].to_numpy(), df[column].to_numpy()


def _plot_one_panel(
    *,
    ax: Any,
    cluster_id: int,
    cell_key_str: str,
    mode: TrialMode,
    column: str,
    color: str,
    y_label: str,
    title_annotation: str | None,
) -> None:
    """Plot PD (solid) and ND (dashed) traces for one (cell, mode, column) combination."""
    plotted: bool = False
    for direction, linestyle in (
        (Direction.PD_DEG, PD_LINESTYLE),
        (Direction.ND_DEG, ND_LINESTYLE),
    ):
        loaded = _load_trace_column(
            cluster_id=cluster_id,
            cell_key_str=cell_key_str,
            mode=mode,
            direction_deg=int(direction.value),
            column=column,
        )
        if loaded is None:
            continue
        t_ms, vals = loaded
        ax.plot(t_ms, vals, color=color, linestyle=linestyle, linewidth=0.9, alpha=0.85)
        plotted = True
    if not plotted:
        ax.text(
            0.5,
            0.5,
            "missing",
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=8,
            color="#aa0000",
        )
    ax.set_xlim(0, 1400)
    ax.set_ylabel(y_label, fontsize=7)
    ax.tick_params(axis="both", labelsize=6)
    if title_annotation is not None:
        ax.text(
            0.98,
            0.95,
            title_annotation,
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=6,
            bbox={"facecolor": "white", "alpha": 0.7, "edgecolor": "none", "pad": 1.5},
        )


def render_cluster_figure(*, cluster_id: int, manifest: pd.DataFrame) -> Path:
    """Render one per-cluster 10x3 figure for the given cluster_id."""
    cells: pd.DataFrame = (
        manifest.loc[manifest[CLUSTER_ID_COL] == cluster_id]
        .sort_values(by=DSI_COL, ascending=True)
        .reset_index(drop=True)
    )
    color: str = TRACE_COLOR_BY_CLUSTER[cluster_id % len(TRACE_COLOR_BY_CLUSTER)]
    fig, axes = plt.subplots(
        nrows=len(cells),
        ncols=3,
        figsize=PER_CLUSTER_FIGSIZE_INCHES,
        sharex=True,
    )
    if len(cells) == 1:
        axes = np.array([axes])
    for row_idx, (_idx, cell_row) in enumerate(cells.iterrows()):
        cell_key_str: str = cell_key(
            source_task=str(cell_row[SOURCE_TASK_COL]),
            seed=int(cell_row[SEED_COL]),
            generation=int(cell_row[GENERATION_COL]),
            individual_idx=int(cell_row[INDIVIDUAL_IDX_COL]),
        )
        dsi: float = float(cell_row[DSI_COL])
        pd_rate: float = float(cell_row[PD_RATE_COL])
        annotation: str = f"DSI={dsi:.2f}\nPD={pd_rate:.1f}Hz"
        # Column 0: g_E (EPSP_PASSIVE)
        _plot_one_panel(
            ax=axes[row_idx, 0],
            cluster_id=cluster_id,
            cell_key_str=cell_key_str,
            mode=TrialMode.EPSP_PASSIVE,
            column=G_E_US_COL,
            color=color,
            y_label=r"$g_E$ ($\mu$S)",
            title_annotation=annotation if row_idx == 0 else annotation,
        )
        # Column 1: g_I (IPSP_PASSIVE)
        _plot_one_panel(
            ax=axes[row_idx, 1],
            cluster_id=cluster_id,
            cell_key_str=cell_key_str,
            mode=TrialMode.IPSP_PASSIVE,
            column=G_I_US_COL,
            color=color,
            y_label=r"$g_I$ ($\mu$S)",
            title_annotation=None,
        )
        # Column 2: V_m (FULL)
        _plot_one_panel(
            ax=axes[row_idx, 2],
            cluster_id=cluster_id,
            cell_key_str=cell_key_str,
            mode=TrialMode.FULL,
            column=V_M_MV_COL,
            color=color,
            y_label=r"$V_m$ (mV)",
            title_annotation=None,
        )
    for col in range(3):
        axes[-1, col].set_xlabel("t (ms)", fontsize=7)
    column_titles: tuple[str, ...] = (r"$g_E$(t)", r"$g_I$(t)", r"$V_m$(t)")
    for col, title in enumerate(column_titles):
        axes[0, col].set_title(title, fontsize=10)
    fig.suptitle(
        f"Cluster {cluster_id} - n={len(cells)} cells, PD (solid) vs ND (dashed)",
        fontsize=12,
        y=0.995,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.985))
    out_path: Path = Path(CLUSTER_TRACES_FIGURE_TEMPLATE.format(c=cluster_id))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=FIGURE_DPI)
    plt.close(fig)
    return out_path


def _median_trace_for_cluster(
    *,
    cluster_id: int,
    cells: pd.DataFrame,
    mode: TrialMode,
    column: str,
    direction_deg: int,
) -> np.ndarray | None:
    """Pointwise median over the cluster's cells. Returns None if no trace loaded."""
    stack: list[np.ndarray] = []
    for _idx, cell_row in cells.iterrows():
        ck: str = cell_key(
            source_task=str(cell_row[SOURCE_TASK_COL]),
            seed=int(cell_row[SEED_COL]),
            generation=int(cell_row[GENERATION_COL]),
            individual_idx=int(cell_row[INDIVIDUAL_IDX_COL]),
        )
        loaded = _load_trace_column(
            cluster_id=cluster_id,
            cell_key_str=ck,
            mode=mode,
            direction_deg=direction_deg,
            column=column,
        )
        if loaded is None:
            continue
        _t_ms, vals = loaded
        # Pad or truncate to expected sample count for safe stacking.
        if vals.shape[0] != EXPECTED_TRACE_ROWS:
            padded: np.ndarray = np.zeros(EXPECTED_TRACE_ROWS, dtype=np.float64)
            n_copy: int = min(vals.shape[0], EXPECTED_TRACE_ROWS)
            padded[:n_copy] = vals[:n_copy]
            vals = padded
        stack.append(vals)
    if len(stack) == 0:
        return None
    return np.median(np.stack(stack, axis=0), axis=0)


def render_cross_cluster_figure(*, manifest: pd.DataFrame) -> Path:
    """Render the 4x3 cross-cluster median-trace summary."""
    fig, axes = plt.subplots(
        nrows=N_CLUSTERS,
        ncols=3,
        figsize=CROSS_CLUSTER_FIGSIZE_INCHES,
        sharex=True,
    )
    t_ms_axis: np.ndarray = np.arange(EXPECTED_TRACE_ROWS, dtype=np.float64)
    for cluster_id in range(N_CLUSTERS):
        color: str = TRACE_COLOR_BY_CLUSTER[cluster_id]
        cells: pd.DataFrame = manifest.loc[manifest[CLUSTER_ID_COL] == cluster_id]
        for col_idx, (mode, column, label) in enumerate(
            (
                (TrialMode.EPSP_PASSIVE, G_E_US_COL, r"$g_E$ ($\mu$S)"),
                (TrialMode.IPSP_PASSIVE, G_I_US_COL, r"$g_I$ ($\mu$S)"),
                (TrialMode.FULL, V_M_MV_COL, r"$V_m$ (mV)"),
            )
        ):
            ax = axes[cluster_id, col_idx]
            for direction_deg, linestyle in (
                (int(Direction.PD_DEG.value), PD_LINESTYLE),
                (int(Direction.ND_DEG.value), ND_LINESTYLE),
            ):
                median = _median_trace_for_cluster(
                    cluster_id=cluster_id,
                    cells=cells,
                    mode=mode,
                    column=column,
                    direction_deg=direction_deg,
                )
                if median is None:
                    continue
                ax.plot(t_ms_axis, median, color=color, linestyle=linestyle, linewidth=1.0)
            ax.set_xlim(0, 1400)
            ax.set_ylabel(label, fontsize=8)
            ax.tick_params(axis="both", labelsize=7)
            if cluster_id == 0:
                ax.set_title(
                    [r"$g_E$(t)", r"$g_I$(t)", r"$V_m$(t)"][col_idx],
                    fontsize=10,
                )
            if cluster_id == N_CLUSTERS - 1:
                ax.set_xlabel("t (ms)", fontsize=8)
        axes[cluster_id, 0].text(
            -0.16,
            0.5,
            f"cluster {cluster_id}",
            transform=axes[cluster_id, 0].transAxes,
            rotation=90,
            ha="center",
            va="center",
            fontsize=10,
        )
    fig.suptitle(
        "Cross-cluster median traces - k=4 t0117 clusters (PD solid, ND dashed)",
        fontsize=12,
        y=0.995,
    )
    fig.tight_layout(rect=(0.02, 0, 1, 0.96))
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(CROSS_CLUSTER_FIGURE, dpi=FIGURE_DPI)
    plt.close(fig)
    return CROSS_CLUSTER_FIGURE


def main() -> None:
    """CLI entry: render all 5 figures (4 per-cluster + 1 cross-cluster)."""
    manifest: pd.DataFrame = pd.read_csv(filepath_or_buffer=SELECTED_CELLS_CSV)
    out_paths: list[Path] = []
    for cluster_id in range(N_CLUSTERS):
        out_paths.append(render_cluster_figure(cluster_id=cluster_id, manifest=manifest))
    out_paths.append(render_cross_cluster_figure(manifest=manifest))
    for p in out_paths:
        print(f"wrote {p}")


if __name__ == "__main__":
    main()
