"""Build the two diagnostic charts for the t0103 DS-cell dataset.

* `results/images/cell_counts_and_ipl.png` — top: bar chart of per-group cell
  count; bottom: bar chart of per-group mean RF diameter (the closest per-cell
  spatial-stratification proxy actually available in the Dryad release,
  standing in for the per-cell IPL stratification depth profile that the
  Dryad release does NOT provide — see the dataset description's
  "Content & Annotation" gap list).
* `results/images/representative_traces.png` — 8-panel grid of cluster-mean
  moving-bar responses (one panel per DS group), drawn from the real `bar_tc`
  per-cell traces in the produced Parquet. The moving-bar stimulus is the
  one Baden 2016 uses to define DS, hence the chosen stimulus.

Both charts read from the produced Parquet and Parquet-level metadata. No
external fallback / placeholder data is used.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from tasks.t0103_extract_baden_2016_ds_morphologies.code.constants import (
    DS_GROUP_IDS,
    DS_GROUP_LABELS,
    FIELD_BAR_TC,
    FIELD_GROUP_ID,
    FIELD_RF_SIZE,
)
from tasks.t0103_extract_baden_2016_ds_morphologies.code.paths import (
    CELL_COUNTS_IPL_PNG_PATH,
    DATASET_OUT_PARQUET_PATH,
    REPRESENTATIVE_TRACES_PNG_PATH,
    RESULTS_IMAGES_DIR,
)


@dataclass(frozen=True, slots=True)
class _GroupSummary:
    """Per-group aggregates used by the diagnostic charts."""

    group_id: int
    label: str
    n_cells: int
    mean_rf_diameter_um: float
    bar_tc_mean: np.ndarray  # (T_bar,) cluster mean of the moving-bar response
    bar_tc_std: np.ndarray  # (T_bar,) cluster std of the moving-bar response


def _load_dataset() -> pd.DataFrame:
    """Load the per-cell Parquet into a Pandas DataFrame."""
    table = pq.read_table(source=str(DATASET_OUT_PARQUET_PATH))
    return table.to_pandas()


def _load_bar_time_axis() -> np.ndarray:
    """Read the moving-bar time axis from the Parquet file-level metadata."""
    meta_bytes = pq.read_metadata(str(DATASET_OUT_PARQUET_PATH)).metadata
    raw = meta_bytes[b"baden_2016_ds_cells_metadata"]
    meta = json.loads(raw.decode("utf-8"))
    return np.asarray(meta["bar_time_s"], dtype=np.float64)


def _summarise_group(*, df: pd.DataFrame, group_id: int) -> _GroupSummary:
    """Aggregate one DS group: count, mean RF size, mean ± std moving-bar."""
    rows: pd.DataFrame = df[df[FIELD_GROUP_ID] == group_id]
    assert len(rows) > 0, f"no cells found for group {group_id}"
    traces: np.ndarray = np.asarray(
        [np.asarray(t, dtype=np.float64) for t in rows[FIELD_BAR_TC].tolist()],
    )  # shape (n_cells, T_bar)
    mean_rf: float = float(np.nanmean(rows[FIELD_RF_SIZE].to_numpy(dtype=np.float64)))
    return _GroupSummary(
        group_id=group_id,
        label=DS_GROUP_LABELS[group_id],
        n_cells=int(len(rows)),
        mean_rf_diameter_um=mean_rf,
        bar_tc_mean=traces.mean(axis=0),
        bar_tc_std=traces.std(axis=0),
    )


def _build_count_and_rf_chart(*, summaries: list[_GroupSummary]) -> None:
    """Write the cell-counts + per-group mean RF diameter figure."""
    labels: list[str] = [f"G{s.group_id}\n{s.label}" for s in summaries]
    counts: list[int] = [s.n_cells for s in summaries]
    rf_means: list[float] = [s.mean_rf_diameter_um for s in summaries]
    fig: Figure
    axes: np.ndarray
    fig, axes = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(10.5, 7.5),
        gridspec_kw={"height_ratios": [1.0, 1.0]},
    )

    ax_top: Axes = axes[0]
    bars_top = ax_top.bar(
        x=range(len(labels)),
        height=counts,
        color="#1f77b4",
        edgecolor="black",
        linewidth=0.5,
    )
    for bar, c in zip(bars_top, counts, strict=True):
        ax_top.text(
            x=bar.get_x() + bar.get_width() / 2.0,
            y=bar.get_height() + 5,
            s=str(c),
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax_top.set_xticks(range(len(labels)))
    ax_top.set_xticklabels(labels, rotation=20, ha="right", fontsize=8)
    ax_top.set_ylabel("Cells per group")
    ax_top.set_title(
        f"t0103 — Per-group cell counts in the Baden 2016 DS subset (N = {sum(counts)} cells)"
    )
    ax_top.grid(axis="y", alpha=0.3)

    ax_bot: Axes = axes[1]
    bars_bot = ax_bot.bar(
        x=range(len(labels)),
        height=rf_means,
        color="#2ca02c",
        edgecolor="black",
        linewidth=0.5,
    )
    for bar, v in zip(bars_bot, rf_means, strict=True):
        ax_bot.text(
            x=bar.get_x() + bar.get_width() / 2.0,
            y=bar.get_height() + 2,
            s=f"{v:.0f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax_bot.set_xticks(range(len(labels)))
    ax_bot.set_xticklabels(labels, rotation=20, ha="right", fontsize=8)
    ax_bot.set_ylabel("Mean RF diameter (μm)")
    ax_bot.set_title(
        "Mean RF diameter per DS group "
        "(no per-cell IPL profile in the Dryad release — RF diameter is the "
        "closest per-cell spatial proxy)",
        fontsize=10,
    )
    ax_bot.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(CELL_COUNTS_IPL_PNG_PATH, dpi=120)
    plt.close(fig=fig)


def _build_trace_grid(
    *,
    summaries: list[_GroupSummary],
    bar_time: np.ndarray,
) -> None:
    """Write the 2x4 grid of cluster-mean moving-bar responses."""
    fig: Figure
    axes: np.ndarray
    fig, axes = plt.subplots(
        nrows=2,
        ncols=4,
        figsize=(13.5, 6.5),
        sharex=True,
        sharey=True,
    )
    flat_axes: list[Axes] = list(axes.flatten())
    for ax, s in zip(flat_axes, summaries, strict=True):
        ax.plot(
            bar_time,
            s.bar_tc_mean,
            color="#1f77b4",
            linewidth=1.4,
        )
        ax.fill_between(
            x=bar_time,
            y1=s.bar_tc_mean - s.bar_tc_std,
            y2=s.bar_tc_mean + s.bar_tc_std,
            color="#1f77b4",
            alpha=0.2,
            linewidth=0,
        )
        ax.axhline(y=0.0, color="black", linestyle=":", linewidth=0.5)
        # Moving-bar stimulus is on at t=1..2s by the Baden 2016 protocol.
        ax.axvline(x=1.0, color="grey", linestyle=":", linewidth=0.5)
        ax.axvline(x=2.0, color="grey", linestyle=":", linewidth=0.5)
        ax.set_title(f"G{s.group_id} {s.label}\n(n={s.n_cells})", fontsize=9)
        ax.tick_params(axis="both", labelsize=8)
    for ax in axes[1, :]:
        ax.set_xlabel("Time (s)")
    for ax in axes[:, 0]:
        ax.set_ylabel("Normalised response")
    fig.suptitle(
        "t0103 — Cluster-mean moving-bar response per Baden 2016 DS group "
        "(mean ± 1 SD; the moving-bar stimulus defines DS in Baden 2016)",
        fontsize=11,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.93))
    fig.savefig(REPRESENTATIVE_TRACES_PNG_PATH, dpi=120)
    plt.close(fig=fig)


def main() -> None:
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    df: pd.DataFrame = _load_dataset()
    bar_time: np.ndarray = _load_bar_time_axis()
    summaries: list[_GroupSummary] = [_summarise_group(df=df, group_id=g) for g in DS_GROUP_IDS]
    _build_count_and_rf_chart(summaries=summaries)
    _build_trace_grid(summaries=summaries, bar_time=bar_time)
    print(f"Wrote {CELL_COUNTS_IPL_PNG_PATH}")
    print(f"Wrote {REPRESENTATIVE_TRACES_PNG_PATH}")


if __name__ == "__main__":
    main()
