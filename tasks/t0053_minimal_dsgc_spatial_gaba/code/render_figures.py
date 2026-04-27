"""Per-direction figures for the t0053 minimal DSGC (spatial centripetal-gating GABA).

Adapted from t0052's ``render_figures.py``. The six existing figure families behave identically:

1. ``v_soma_dir_<deg>.png``       — mean +/- SD soma V(t) across 10 FULL trials (12 PNGs).
2. ``epsp_dir_<deg>.png``         — same for AMPA_ONLY voltage traces (12 PNGs).
3. ``ipsp_dir_<deg>.png``         — same for GABA_ONLY voltage traces (12 PNGs).
4. ``psth_dir_<deg>.png``         — 5 ms-bin firing-rate PSTH across 10 FULL trials (12 PNGs).
5. ``activation_dir_<deg>.png``   — per-direction synapse onset-time histogram, with the
   ``is_fired`` rows split into a coloured facet (12 PNGs).
6. Tuning-curve overview figures via the ``tuning_curve_viz`` library:
   ``polar_tuning_curve.png``, ``cartesian_tuning_curve.png``, plus
   ``raster_psth_dir_<deg>.png`` per direction (12 more PNGs).

Plus one new family added in this task (REQ-21):

7. ``active_fraction_polar.png``  — closed-polygon polar plot of the per-direction fraction of I
   synapses fired in FULL mode (1 PNG total).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from tasks.t0011_response_visualization_library.code.tuning_curve_viz import (  # noqa: E402
    plot_angle_raster_psth,
    plot_cartesian_tuning_curve,
    plot_polar_tuning_curve,
)
from tasks.t0053_minimal_dsgc_spatial_gaba.code.constants import (  # noqa: E402
    ANGLES_DEG,
    COL_ACTIVE_FRACTION,
    COL_ANGLE_DEG,
    COL_IS_FIRED,
    COL_ONSET_TIME_MS,
    COL_SAMPLE_IDX,
    COL_SPIKE_TIME_S,
    COL_T_MS,
    COL_TRIAL_INDEX,
    COL_TRIAL_SEED,
    COL_VOLTAGE_MV,
    TSTOP_MS,
)
from tasks.t0053_minimal_dsgc_spatial_gaba.code.paths import (  # noqa: E402
    ACTIVATION_TIMES_CSV,
    ACTIVE_FRACTION_CSV,
    IMAGES_DIR,
    SPIKE_TIMES_FULL_CSV,
    TARGET_TUNING_CURVE_CSV,
    TUNING_CURVE_FULL_CSV,
    VOLTAGE_TRACES_AMPA_ONLY_CSV,
    VOLTAGE_TRACES_FULL_CSV,
    VOLTAGE_TRACES_GABA_ONLY_CSV,
)

FIG_DPI: int = 100
FIG_SIZE_INCHES: tuple[float, float] = (6.0, 4.0)
PSTH_BIN_MS: float = 5.0


def _ensure_images_dir() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def _voltage_pivot_per_angle(
    *,
    df: pd.DataFrame,
    angle_deg: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (t_ms, mean_v, sd_v) arrays for the given angle."""
    sub: pd.DataFrame = df[df[COL_ANGLE_DEG] == angle_deg]
    if len(sub) == 0:
        return (np.zeros(0), np.zeros(0), np.zeros(0))
    pivot: pd.DataFrame = sub.pivot_table(
        index=COL_SAMPLE_IDX,
        columns=COL_TRIAL_SEED,
        values=COL_VOLTAGE_MV,
    )
    pivot = pivot.dropna(axis=0, how="any")
    sample_indices: np.ndarray = pivot.index.to_numpy(dtype=np.int64)
    voltage_matrix: np.ndarray = pivot.to_numpy(dtype=np.float64)
    mean_v: np.ndarray = voltage_matrix.mean(axis=1)
    sd_v: np.ndarray = voltage_matrix.std(axis=1, ddof=0)
    representative_seed = pivot.columns[0]
    t_lookup: pd.DataFrame = sub[sub[COL_TRIAL_SEED] == representative_seed][
        [COL_SAMPLE_IDX, COL_T_MS]
    ].drop_duplicates(subset=COL_SAMPLE_IDX)
    t_lookup = t_lookup.set_index(COL_SAMPLE_IDX).reindex(sample_indices)
    t_ms: np.ndarray = t_lookup[COL_T_MS].to_numpy(dtype=np.float64)
    return (t_ms, mean_v, sd_v)


def _render_voltage_per_direction(
    *,
    voltage_csv: Path,
    out_dir: Path,
    prefix: str,
    title_prefix: str,
) -> None:
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=voltage_csv)
    for angle_deg in ANGLES_DEG:
        t_ms, mean_v, sd_v = _voltage_pivot_per_angle(df=df, angle_deg=angle_deg)
        if len(t_ms) == 0:
            continue
        fig, ax = plt.subplots(figsize=FIG_SIZE_INCHES, dpi=FIG_DPI)
        ax.plot(t_ms, mean_v, color="tab:blue", linewidth=1.0, label="mean")
        ax.fill_between(
            t_ms,
            mean_v - sd_v,
            mean_v + sd_v,
            color="tab:blue",
            alpha=0.25,
            linewidth=0.0,
            label="+/- SD",
        )
        ax.set_xlabel("time (ms)")
        ax.set_ylabel("V_soma (mV)")
        ax.set_title(f"{title_prefix} dir = {angle_deg} deg (n=10 trials, mean +/- SD)")
        ax.legend(loc="lower right", frameon=False)
        out_path: Path = out_dir / f"{prefix}_dir_{angle_deg:03d}.png"
        fig.tight_layout()
        fig.savefig(fname=out_path)
        plt.close(fig=fig)


def render_soma_voltage_per_direction(*, out_dir: Path) -> None:
    _render_voltage_per_direction(
        voltage_csv=VOLTAGE_TRACES_FULL_CSV,
        out_dir=out_dir,
        prefix="v_soma",
        title_prefix="Soma V(t) FULL",
    )


def render_aggregate_epsp(*, out_dir: Path) -> None:
    _render_voltage_per_direction(
        voltage_csv=VOLTAGE_TRACES_AMPA_ONLY_CSV,
        out_dir=out_dir,
        prefix="epsp",
        title_prefix="Aggregate EPSP (AMPA-only)",
    )


def render_aggregate_ipsp(*, out_dir: Path) -> None:
    _render_voltage_per_direction(
        voltage_csv=VOLTAGE_TRACES_GABA_ONLY_CSV,
        out_dir=out_dir,
        prefix="ipsp",
        title_prefix="Aggregate IPSP (GABA-only)",
    )


def render_psth(*, out_dir: Path) -> None:
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=SPIKE_TIMES_FULL_CSV)
    bin_edges_ms: np.ndarray = np.arange(0.0, TSTOP_MS + PSTH_BIN_MS, PSTH_BIN_MS)
    bin_centers_ms: np.ndarray = bin_edges_ms[:-1] + 0.5 * PSTH_BIN_MS
    n_trials_per_angle: int = (
        df.groupby(COL_ANGLE_DEG)[COL_TRIAL_INDEX].nunique().max() if len(df) > 0 else 1
    )
    n_trials_per_angle = max(1, int(n_trials_per_angle))
    bin_width_s: float = PSTH_BIN_MS / 1000.0
    for angle_deg in ANGLES_DEG:
        sub = df[df[COL_ANGLE_DEG] == angle_deg]
        spike_times_ms: np.ndarray = sub[COL_SPIKE_TIME_S].to_numpy(dtype=np.float64) * 1000.0
        counts, _ = np.histogram(spike_times_ms, bins=bin_edges_ms)
        rate_hz: np.ndarray = counts.astype(np.float64) / float(n_trials_per_angle) / bin_width_s
        fig, ax = plt.subplots(figsize=FIG_SIZE_INCHES, dpi=FIG_DPI)
        ax.bar(bin_centers_ms, rate_hz, width=PSTH_BIN_MS, color="tab:purple", edgecolor="none")
        ax.set_xlabel("time (ms)")
        ax.set_ylabel("firing rate (Hz)")
        ax.set_title(f"PSTH FULL dir = {angle_deg} deg (5 ms bins)")
        out_path: Path = out_dir / f"psth_dir_{angle_deg:03d}.png"
        fig.tight_layout()
        fig.savefig(fname=out_path)
        plt.close(fig=fig)


def render_activation_histogram(*, out_dir: Path) -> None:
    """Per-direction synapse activation histogram, with ``is_fired`` synapses highlighted.

    Two stacked bars per bin: blue = all synapses, orange overlay = only synapses that fired
    (E synapses always fire; I synapses fire only when the spatial gate fires). The orange bar
    therefore reflects the per-direction active subset across the full pair set.
    """
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=ACTIVATION_TIMES_CSV)
    bin_edges_ms: np.ndarray = np.arange(0.0, TSTOP_MS + 10.0, 10.0)
    for angle_deg in ANGLES_DEG:
        sub = df[df[COL_ANGLE_DEG] == angle_deg]
        onsets_ms: np.ndarray = sub[COL_ONSET_TIME_MS].to_numpy(dtype=np.float64)
        fired_onsets_ms: np.ndarray = sub.loc[sub[COL_IS_FIRED] == 1, COL_ONSET_TIME_MS].to_numpy(
            dtype=np.float64
        )
        fig, ax = plt.subplots(figsize=FIG_SIZE_INCHES, dpi=FIG_DPI)
        ax.hist(
            onsets_ms,
            bins=bin_edges_ms,
            color="tab:orange",
            edgecolor="none",
            alpha=0.45,
            label="all synapses",
        )
        ax.hist(
            fired_onsets_ms,
            bins=bin_edges_ms,
            color="tab:red",
            edgecolor="none",
            alpha=0.85,
            label="is_fired = 1",
        )
        ax.set_xlabel("synapse onset time (ms)")
        ax.set_ylabel("n synapses")
        ax.set_title(f"Synapse activation histogram dir = {angle_deg} deg")
        ax.legend(loc="upper right", frameon=False)
        out_path: Path = out_dir / f"activation_dir_{angle_deg:03d}.png"
        fig.tight_layout()
        fig.savefig(fname=out_path)
        plt.close(fig=fig)


def render_tuning_curves(*, out_dir: Path) -> None:
    target_csv: Path | None = TARGET_TUNING_CURVE_CSV if TARGET_TUNING_CURVE_CSV.exists() else None
    plot_polar_tuning_curve(
        TUNING_CURVE_FULL_CSV,
        out_dir / "polar_tuning_curve.png",
        target_csv=target_csv,
    )
    plot_cartesian_tuning_curve(
        TUNING_CURVE_FULL_CSV,
        out_dir / "cartesian_tuning_curve.png",
        target_csv=target_csv,
    )


def render_raster_psth(*, out_dir: Path) -> None:
    """Per-direction trial raster + PSTH via the t0011 ``tuning_curve_viz`` library."""
    for angle_deg in ANGLES_DEG:
        out_path: Path = out_dir / f"raster_psth_dir_{angle_deg:03d}.png"
        try:
            plot_angle_raster_psth(
                SPIKE_TIMES_FULL_CSV,
                out_path,
                angle_deg=float(angle_deg),
            )
        except ValueError:
            # Some directions may have no spikes (e.g., null direction). Skip silently.
            continue


def render_active_fraction_polar(
    *,
    active_fraction_csv: Path,
    out_dir: Path,
) -> None:
    """Polar plot of the per-direction fraction of I synapses fired (FULL mode mean over 10 trials).

    Closed polygon with 0..1 radial axis and a faint reference circle at radius 0.5.
    """
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=active_fraction_csv)
    df_sorted: pd.DataFrame = df.sort_values(by=COL_ANGLE_DEG).reset_index(drop=True)
    angles_deg: np.ndarray = df_sorted[COL_ANGLE_DEG].to_numpy(dtype=np.float64)
    fractions: np.ndarray = df_sorted[COL_ACTIVE_FRACTION].to_numpy(dtype=np.float64)

    # Close the polygon by appending the first sample.
    angles_closed: np.ndarray = np.concatenate([angles_deg, angles_deg[:1]])
    fractions_closed: np.ndarray = np.concatenate([fractions, fractions[:1]])

    angles_rad: np.ndarray = np.deg2rad(angles_closed)
    reference_angles_rad: np.ndarray = np.linspace(0.0, 2.0 * np.pi, 361)
    reference_radius: np.ndarray = np.full_like(reference_angles_rad, 0.5)

    fig, ax = plt.subplots(
        figsize=(5.5, 5.5),
        dpi=FIG_DPI,
        subplot_kw={"projection": "polar"},
    )
    ax.plot(reference_angles_rad, reference_radius, color="grey", linewidth=0.8, alpha=0.5)
    ax.plot(angles_rad, fractions_closed, color="tab:blue", linewidth=1.6)
    ax.fill(angles_rad, fractions_closed, color="tab:blue", alpha=0.22)
    ax.scatter(angles_rad, fractions_closed, color="tab:blue", s=18, zorder=3)

    ax.set_rlim(0.0, 1.0)
    ax.set_rticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_rlabel_position(90.0)
    ax.set_title("Active I-synapse fraction vs direction (FULL mode)", pad=18)
    out_path: Path = out_dir / "active_fraction_polar.png"
    fig.tight_layout()
    fig.savefig(fname=out_path)
    plt.close(fig=fig)


def main() -> int:
    _ensure_images_dir()
    print("[render] soma voltage (FULL) per direction...", flush=True)
    render_soma_voltage_per_direction(out_dir=IMAGES_DIR)
    print("[render] aggregate EPSP (AMPA_ONLY) per direction...", flush=True)
    render_aggregate_epsp(out_dir=IMAGES_DIR)
    print("[render] aggregate IPSP (GABA_ONLY) per direction...", flush=True)
    render_aggregate_ipsp(out_dir=IMAGES_DIR)
    print("[render] PSTH (FULL) per direction...", flush=True)
    render_psth(out_dir=IMAGES_DIR)
    print("[render] synapse activation histogram per direction...", flush=True)
    render_activation_histogram(out_dir=IMAGES_DIR)
    print("[render] polar + cartesian tuning curves...", flush=True)
    render_tuning_curves(out_dir=IMAGES_DIR)
    print("[render] raster+PSTH per direction (t0011 lib)...", flush=True)
    render_raster_psth(out_dir=IMAGES_DIR)
    print("[render] active fraction polar plot...", flush=True)
    render_active_fraction_polar(
        active_fraction_csv=ACTIVE_FRACTION_CSV,
        out_dir=IMAGES_DIR,
    )
    print(f"[render] Done. PNGs written under {IMAGES_DIR}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
