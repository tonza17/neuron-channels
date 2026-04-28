"""Per-(gNMDA × direction) figures and sweep-summary plots for t0054 minimal DSGC AMPA + NMDA.

Adapted from ``tasks/t0052_minimal_dsgc_scalar_gaba/code/render_figures.py`` and extended with:

* Outer ``gnmda_ns`` loop over every per-direction figure family. Output filename pattern:
  ``{prefix}_gnmda_{gnmda:.2f}_dir_{angle_deg:03d}.png`` (12 directions × 5 plot families × 4
  gNMDA values = 240 PNGs).
* Per-gNMDA polar and Cartesian tuning-curve overviews via the t0011 ``tuning_curve_viz``
  library: 4 + 4 = 8 PNGs.
* Three sweep-summary plots: ``epsp_decay_vs_gnmda.png``, ``peak_hz_vs_gnmda.png``,
  ``dsi_vs_gnmda.png`` (line plots over the four ``gNMDA`` values).

The renderer is invoked AFTER the full sweep and AFTER ``compute_metrics.py`` has produced
``derived_quantities.json``; the sweep-summary plots read decay / DSI values from
``derived_quantities.json``.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from tasks.t0011_response_visualization_library.code.tuning_curve_viz import (  # noqa: E402
    plot_cartesian_tuning_curve,
    plot_polar_tuning_curve,
)
from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.constants import (  # noqa: E402
    ANGLES_DEG,
    COL_ANGLE_DEG,
    COL_GNMDA_NS,
    COL_ONSET_TIME_MS,
    COL_SAMPLE_IDX,
    COL_SPIKE_TIME_S,
    COL_T_MS,
    COL_TRIAL_INDEX,
    COL_TRIAL_SEED,
    COL_VOLTAGE_MV,
    NMDA_PEAK_NS_VALUES,
    TSTOP_MS,
)
from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.paths import (  # noqa: E402
    ACTIVATION_TIMES_CSV,
    DERIVED_QUANTITIES_JSON,
    DSI_VS_GNMDA_PNG,
    EPSP_DECAY_VS_GNMDA_PNG,
    IMAGES_DIR,
    PEAK_HZ_VS_GNMDA_PNG,
    SPIKE_TIMES_FULL_CSV,
    TARGET_TUNING_CURVE_CSV,
    TUNING_CURVE_FULL_CSV,
    VOLTAGE_TRACES_E_ONLY_CSV,
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
    """Return (t_ms, mean_v, sd_v) arrays for a given angle from a single-gNMDA slice.

    Pivots the long-form CSV into a (n_trials, n_samples) matrix and reduces across the
    trial axis. Trials with missing samples are dropped.
    """
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


def _render_voltage_per_direction_per_gnmda(
    *,
    voltage_csv: Path,
    out_dir: Path,
    prefix: str,
    title_prefix: str,
) -> None:
    df_full: pd.DataFrame = pd.read_csv(filepath_or_buffer=voltage_csv)
    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        df: pd.DataFrame = df_full[np.isclose(df_full[COL_GNMDA_NS], gnmda_ns)]
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
            ax.set_title(
                f"{title_prefix} gNMDA={gnmda_ns:.2f} nS dir={angle_deg} deg (n=10, mean +/- SD)",
            )
            ax.legend(loc="lower right", frameon=False)
            out_path: Path = out_dir / f"{prefix}_gnmda_{gnmda_ns:.2f}_dir_{angle_deg:03d}.png"
            fig.tight_layout()
            fig.savefig(fname=out_path)
            plt.close(fig=fig)


def render_soma_voltage_per_direction(*, out_dir: Path) -> None:
    _render_voltage_per_direction_per_gnmda(
        voltage_csv=VOLTAGE_TRACES_FULL_CSV,
        out_dir=out_dir,
        prefix="v_soma",
        title_prefix="Soma V(t) FULL",
    )


def render_aggregate_epsp(*, out_dir: Path) -> None:
    _render_voltage_per_direction_per_gnmda(
        voltage_csv=VOLTAGE_TRACES_E_ONLY_CSV,
        out_dir=out_dir,
        prefix="epsp",
        title_prefix="Aggregate EPSP (E_ONLY)",
    )


def render_aggregate_ipsp(*, out_dir: Path) -> None:
    _render_voltage_per_direction_per_gnmda(
        voltage_csv=VOLTAGE_TRACES_GABA_ONLY_CSV,
        out_dir=out_dir,
        prefix="ipsp",
        title_prefix="Aggregate IPSP (GABA_ONLY)",
    )


def render_psth(*, out_dir: Path) -> None:
    df_full: pd.DataFrame = pd.read_csv(filepath_or_buffer=SPIKE_TIMES_FULL_CSV)
    bin_edges_ms: np.ndarray = np.arange(0.0, TSTOP_MS + PSTH_BIN_MS, PSTH_BIN_MS)
    bin_centers_ms: np.ndarray = bin_edges_ms[:-1] + 0.5 * PSTH_BIN_MS
    bin_width_s: float = PSTH_BIN_MS / 1000.0
    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        df: pd.DataFrame = df_full[np.isclose(df_full[COL_GNMDA_NS], gnmda_ns)]
        if len(df) == 0:
            n_trials_per_angle: int = 1
        else:
            n_trials_per_angle = max(
                1,
                int(df.groupby(COL_ANGLE_DEG)[COL_TRIAL_INDEX].nunique().max()),
            )
        for angle_deg in ANGLES_DEG:
            sub = df[df[COL_ANGLE_DEG] == angle_deg]
            spike_times_ms: np.ndarray = sub[COL_SPIKE_TIME_S].to_numpy(dtype=np.float64) * 1000.0
            counts, _ = np.histogram(spike_times_ms, bins=bin_edges_ms)
            rate_hz: np.ndarray = (
                counts.astype(np.float64) / float(n_trials_per_angle) / bin_width_s
            )
            fig, ax = plt.subplots(figsize=FIG_SIZE_INCHES, dpi=FIG_DPI)
            ax.bar(
                bin_centers_ms,
                rate_hz,
                width=PSTH_BIN_MS,
                color="tab:purple",
                edgecolor="none",
            )
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("firing rate (Hz)")
            ax.set_title(
                f"PSTH FULL gNMDA={gnmda_ns:.2f} nS dir={angle_deg} deg (5 ms bins)",
            )
            out_path: Path = out_dir / f"psth_gnmda_{gnmda_ns:.2f}_dir_{angle_deg:03d}.png"
            fig.tight_layout()
            fig.savefig(fname=out_path)
            plt.close(fig=fig)


def render_activation_histogram(*, out_dir: Path) -> None:
    df_full: pd.DataFrame = pd.read_csv(filepath_or_buffer=ACTIVATION_TIMES_CSV)
    bin_edges_ms: np.ndarray = np.arange(0.0, TSTOP_MS + 10.0, 10.0)
    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        df: pd.DataFrame = df_full[np.isclose(df_full[COL_GNMDA_NS], gnmda_ns)]
        for angle_deg in ANGLES_DEG:
            sub = df[df[COL_ANGLE_DEG] == angle_deg]
            onsets_ms: np.ndarray = sub[COL_ONSET_TIME_MS].to_numpy(dtype=np.float64)
            fig, ax = plt.subplots(figsize=FIG_SIZE_INCHES, dpi=FIG_DPI)
            ax.hist(onsets_ms, bins=bin_edges_ms, color="tab:orange", edgecolor="none")
            ax.set_xlabel("synapse onset time (ms)")
            ax.set_ylabel("n synapses")
            ax.set_title(
                f"Synapse activation histogram gNMDA={gnmda_ns:.2f} nS dir={angle_deg} deg",
            )
            out_path: Path = out_dir / f"activation_gnmda_{gnmda_ns:.2f}_dir_{angle_deg:03d}.png"
            fig.tight_layout()
            fig.savefig(fname=out_path)
            plt.close(fig=fig)


def render_tuning_curves_per_gnmda(*, out_dir: Path) -> None:
    """Render polar + Cartesian overviews per gNMDA from a sliced FULL tuning curve."""
    target_csv: Path | None = TARGET_TUNING_CURVE_CSV if TARGET_TUNING_CURVE_CSV.exists() else None
    df_full: pd.DataFrame = pd.read_csv(filepath_or_buffer=TUNING_CURVE_FULL_CSV)
    tmp_dir: Path = out_dir / "_tuning_curve_slices_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        sub: pd.DataFrame = df_full[np.isclose(df_full[COL_GNMDA_NS], gnmda_ns)].drop(
            columns=[COL_GNMDA_NS]
        )
        slice_csv: Path = tmp_dir / f"tuning_curve_full_gnmda_{gnmda_ns:.2f}.csv"
        sub.to_csv(path_or_buf=slice_csv, index=False)
        plot_polar_tuning_curve(
            slice_csv,
            out_dir / f"polar_tuning_curve_gnmda_{gnmda_ns:.2f}.png",
            target_csv=target_csv,
        )
        plot_cartesian_tuning_curve(
            slice_csv,
            out_dir / f"cartesian_tuning_curve_gnmda_{gnmda_ns:.2f}.png",
            target_csv=target_csv,
        )


def _load_derived() -> dict[str, object]:
    if not DERIVED_QUANTITIES_JSON.exists():
        raise FileNotFoundError(
            f"derived_quantities.json not found at {DERIVED_QUANTITIES_JSON}; "
            f"run compute_metrics.py first.",
        )
    return json.loads(DERIVED_QUANTITIES_JSON.read_text(encoding="utf-8"))


def render_epsp_decay_vs_gnmda(*, out_path: Path) -> None:
    derived: dict[str, object] = _load_derived()
    per_gnmda: dict[str, dict[str, object]] = derived["per_gnmda"]  # type: ignore[assignment]
    xs: list[float] = []
    ys: list[float] = []
    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        key: str = f"{gnmda_ns:.2f}"
        if key not in per_gnmda:
            continue
        decay_obj: object = per_gnmda[key].get("epsp_decay_to_1e_ms")
        if decay_obj is None:
            continue
        xs.append(gnmda_ns)
        ys.append(float(decay_obj))  # type: ignore[arg-type]
    fig, ax = plt.subplots(figsize=FIG_SIZE_INCHES, dpi=FIG_DPI)
    ax.plot(xs, ys, marker="o", color="tab:blue")
    ax.set_xlabel("gNMDA (nS)")
    ax.set_ylabel("EPSP decay-to-1/e (ms)")
    ax.set_title("EPSP decay-to-1/e vs gNMDA (E_ONLY at preferred direction)")
    ax.grid(visible=True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(fname=out_path)
    plt.close(fig=fig)


def render_peak_hz_vs_gnmda(*, out_path: Path) -> None:
    derived: dict[str, object] = _load_derived()
    per_variant: dict[str, dict[str, object]] = derived["per_variant"]  # type: ignore[assignment]
    xs: list[float] = []
    ys: list[float] = []
    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        key: str = f"gnmda_{gnmda_ns:.2f}_full"
        if key not in per_variant:
            continue
        peak_hz_obj: object = per_variant[key].get("peak_hz")
        if peak_hz_obj is None:
            continue
        xs.append(gnmda_ns)
        ys.append(float(peak_hz_obj))  # type: ignore[arg-type]
    fig, ax = plt.subplots(figsize=FIG_SIZE_INCHES, dpi=FIG_DPI)
    ax.plot(xs, ys, marker="o", color="tab:purple")
    ax.set_xlabel("gNMDA (nS)")
    ax.set_ylabel("peak firing rate (Hz)")
    ax.set_title("Peak Hz vs gNMDA (FULL mode)")
    ax.grid(visible=True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(fname=out_path)
    plt.close(fig=fig)


def render_dsi_vs_gnmda(*, out_path: Path) -> None:
    derived: dict[str, object] = _load_derived()
    per_variant: dict[str, dict[str, object]] = derived["per_variant"]  # type: ignore[assignment]
    xs: list[float] = []
    vector_dsi: list[float] = []
    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        key: str = f"gnmda_{gnmda_ns:.2f}_full"
        if key not in per_variant:
            continue
        vsd_obj: object = per_variant[key].get("vector_sum_dsi")
        if vsd_obj is None:
            continue
        xs.append(gnmda_ns)
        vector_dsi.append(float(vsd_obj))  # type: ignore[arg-type]
    # Primary DSI (registered metric) lives in metrics.json; we also load it for the second curve.
    from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.paths import (  # noqa: PLC0415
        METRICS_JSON,
    )

    primary_dsi_by_gnmda: dict[float, float] = {}
    if METRICS_JSON.exists():
        metrics: dict[str, object] = json.loads(METRICS_JSON.read_text(encoding="utf-8"))
        variants: list[dict[str, object]] = metrics["variants"]  # type: ignore[assignment]
        for v in variants:
            dims: dict[str, object] = v["dimensions"]  # type: ignore[assignment]
            if dims.get("mode") != "full":
                continue
            metric_block: dict[str, object] = v["metrics"]  # type: ignore[assignment]
            dsi_obj: object = metric_block.get("direction_selectivity_index")
            if dsi_obj is None:
                continue
            primary_dsi_by_gnmda[float(dims["gnmda_ns"])] = float(  # type: ignore[arg-type]
                dsi_obj,
            )
    primary_xs: list[float] = sorted(primary_dsi_by_gnmda.keys())
    primary_ys: list[float] = [primary_dsi_by_gnmda[x] for x in primary_xs]
    fig, ax = plt.subplots(figsize=FIG_SIZE_INCHES, dpi=FIG_DPI)
    ax.plot(xs, vector_dsi, marker="o", color="tab:blue", label="vector-sum DSI")
    if len(primary_xs) > 0:
        ax.plot(
            primary_xs,
            primary_ys,
            marker="s",
            color="tab:red",
            label="primary DSI (registered)",
        )
    ax.set_xlabel("gNMDA (nS)")
    ax.set_ylabel("DSI")
    ax.set_title("DSI vs gNMDA (FULL mode)")
    ax.legend(loc="best", frameon=False)
    ax.grid(visible=True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(fname=out_path)
    plt.close(fig=fig)


def main() -> int:
    _ensure_images_dir()
    print("[render] soma voltage (FULL) per (gNMDA, direction)...", flush=True)
    render_soma_voltage_per_direction(out_dir=IMAGES_DIR)
    print("[render] aggregate EPSP (E_ONLY) per (gNMDA, direction)...", flush=True)
    render_aggregate_epsp(out_dir=IMAGES_DIR)
    print("[render] aggregate IPSP (GABA_ONLY) per (gNMDA, direction)...", flush=True)
    render_aggregate_ipsp(out_dir=IMAGES_DIR)
    print("[render] PSTH (FULL) per (gNMDA, direction)...", flush=True)
    render_psth(out_dir=IMAGES_DIR)
    print("[render] synapse activation histogram per (gNMDA, direction)...", flush=True)
    render_activation_histogram(out_dir=IMAGES_DIR)
    print("[render] polar + cartesian tuning curves per gNMDA...", flush=True)
    render_tuning_curves_per_gnmda(out_dir=IMAGES_DIR)
    print("[render] sweep summaries: epsp_decay / peak_hz / dsi vs gNMDA...", flush=True)
    render_epsp_decay_vs_gnmda(out_path=EPSP_DECAY_VS_GNMDA_PNG)
    render_peak_hz_vs_gnmda(out_path=PEAK_HZ_VS_GNMDA_PNG)
    render_dsi_vs_gnmda(out_path=DSI_VS_GNMDA_PNG)
    print(f"[render] Done. PNGs written under {IMAGES_DIR}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
