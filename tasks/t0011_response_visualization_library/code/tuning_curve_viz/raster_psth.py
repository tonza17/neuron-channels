"""Per-angle spike raster + PSTH plot."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec

from tasks.t0011_response_visualization_library.code.tuning_curve_viz.constants import (
    DEFAULT_BBOX_INCHES,
    DEFAULT_DPI,
    DEFAULT_FACECOLOR,
    MODEL_COLORS,
    PSTH_BIN_WIDTH_S,
)

# Spike-time CSV columns. No canonical schema is registered elsewhere in the project
# (no task has yet produced a spike-time CSV), so we define the schema here.
ANGLE_DEG_COLUMN: str = "angle_deg"
TRIAL_INDEX_COLUMN: str = "trial_index"
SPIKE_TIME_COLUMN: str = "spike_time_s"


def _load_spike_times(
    *,
    spike_times_csv: Path,
    angle_deg: float,
) -> list[np.ndarray]:
    """Load spike-time rows for ``angle_deg`` and group them by ``trial_index``.

    Returns a list with one 1-D NumPy array per trial, indexed by sorted ``trial_index``
    so repeated calls produce deterministic order.
    """
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=spike_times_csv)
    required_columns: set[str] = {
        ANGLE_DEG_COLUMN,
        TRIAL_INDEX_COLUMN,
        SPIKE_TIME_COLUMN,
    }
    missing: set[str] = required_columns - set(df.columns)
    if len(missing) > 0:
        raise ValueError(
            f"Spike-time CSV {spike_times_csv} missing columns {sorted(missing)}; "
            f"expected {sorted(required_columns)}"
        )
    angle_rows: pd.DataFrame = df.loc[
        np.isclose(df[ANGLE_DEG_COLUMN].to_numpy(dtype=np.float64), angle_deg)
    ].copy()
    if len(angle_rows) == 0:
        raise ValueError(f"No spike-time rows match angle_deg={angle_deg} in {spike_times_csv}")
    trial_ids: list[int] = sorted(set(angle_rows[TRIAL_INDEX_COLUMN].astype(dtype=int)))
    return [
        angle_rows.loc[
            angle_rows[TRIAL_INDEX_COLUMN].astype(dtype=int) == trial_id,
            SPIKE_TIME_COLUMN,
        ].to_numpy(dtype=np.float64)
        for trial_id in trial_ids
    ]


def plot_angle_raster_psth(
    spike_times_csv: Path,
    out_png: Path,
    *,
    angle_deg: float,
) -> None:
    """Per-angle trial raster above a PSTH histogram.

    Reads a spike-time CSV with columns ``(angle_deg, trial_index, spike_time_s)``,
    filters rows to ``angle_deg``, and draws a :func:`matplotlib.axes.Axes.eventplot`
    raster (one row per trial) above a PSTH with :data:`PSTH_BIN_WIDTH_S` bins.

    Parameters
    ----------
    spike_times_csv:
        CSV path. Must contain columns ``angle_deg``, ``trial_index``, ``spike_time_s``.
    out_png:
        Destination PNG path; parent directory must exist.
    angle_deg:
        The direction for which the raster+PSTH is drawn.
    """
    trial_spike_times: list[np.ndarray] = _load_spike_times(
        spike_times_csv=spike_times_csv,
        angle_deg=angle_deg,
    )
    if len(trial_spike_times) == 0:
        raise ValueError(f"No trials for angle_deg={angle_deg} in {spike_times_csv}")

    # Compute display time range from all spike times at this angle plus a small pad.
    all_spike_times: np.ndarray = (
        np.concatenate(
            [t for t in trial_spike_times if t.size > 0],
            dtype=np.float64,
        )
        if any(t.size > 0 for t in trial_spike_times)
        else np.array([], dtype=np.float64)
    )
    if all_spike_times.size > 0:
        t_max: float = float(np.ceil(all_spike_times.max() * 10.0) / 10.0) + 0.1
    else:
        t_max = 1.0
    t_min: float = 0.0

    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(8.0, 6.0))
    gs: GridSpec = GridSpec(
        nrows=2,
        ncols=1,
        height_ratios=[3, 1],
        figure=fig,
    )
    raster_ax = fig.add_subplot(gs[0, 0])
    psth_ax = fig.add_subplot(gs[1, 0], sharex=raster_ax)

    # Raster: one row per trial.
    lineoffsets: list[float] = [float(i) for i in range(1, len(trial_spike_times) + 1)]
    raster_ax.eventplot(
        positions=trial_spike_times,
        colors="black",
        lineoffsets=lineoffsets,
        linelengths=0.8,
    )
    raster_ax.set_ylabel("Trial")
    raster_ax.set_title(f"Spike raster + PSTH at angle = {angle_deg:.0f} deg")
    raster_ax.set_xlim(left=t_min, right=t_max)
    raster_ax.set_ylim(bottom=0.5, top=len(trial_spike_times) + 0.5)
    raster_ax.grid(visible=False)

    # PSTH: pooled histogram over all trials, 10 ms bins.
    if all_spike_times.size > 0:
        n_bins: int = max(1, int(np.ceil((t_max - t_min) / PSTH_BIN_WIDTH_S)))
        psth_ax.hist(
            x=all_spike_times,
            bins=n_bins,
            range=(t_min, t_max),
            color=MODEL_COLORS[0],
            edgecolor="none",
        )
    psth_ax.set_xlabel("Time (s)")
    psth_ax.set_ylabel("Spike count")
    psth_ax.set_xlim(left=t_min, right=t_max)
    psth_ax.grid(visible=True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(
        fname=out_png,
        dpi=DEFAULT_DPI,
        facecolor=DEFAULT_FACECOLOR,
        bbox_inches=DEFAULT_BBOX_INCHES,
    )
    plt.close(fig=fig)
