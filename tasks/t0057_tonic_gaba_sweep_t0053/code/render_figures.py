"""Per-(gaba, direction) and cross-conductance figures for the t0057 minimal DSGC.

Adapted from ``tasks/t0053_minimal_dsgc_spatial_gaba/code/render_figures.py``. Each per-direction
figure family becomes per-(gaba, direction): the inner loop over 12 angles is wrapped by an outer
loop over ``GABA_BASE_NS_VALUES``, and PNG names encode both. Six figure families per conductance:

1. ``v_soma_gaba_<g>_dir_<deg>.png``     — mean +/- SD soma V(t) across 10 FULL trials.
2. ``epsp_gaba_<g>_dir_<deg>.png``       — same for AMPA_ONLY voltage traces.
3. ``ipsp_gaba_<g>_dir_<deg>.png``       — same for GABA_ONLY voltage traces (the new headline).
4. ``psth_gaba_<g>_dir_<deg>.png``       — 5 ms-bin firing-rate PSTH across 10 FULL trials.
5. ``activation_gaba_<g>_dir_<deg>.png`` — synapse onset-time histogram with is_fired highlighted.
6. ``polar_tuning_curve_gaba_<g>.png``    — polar tuning curve via t0011 ``tuning_curve_viz``.

Plus three new families:

* ``cartesian_tuning_curve_gaba_<g>.png`` — Cartesian per-conductance overlay vs t0004 target.
* ``active_fraction_polar.png``           — single PNG, conductance-independent.
* Cross-conductance summary plots (6 PNGs): DSI primary, DSI vector-sum, peak Hz, null Hz, HWHM,
  RMSE, all vs ``GABA_BASE_NS``.
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
from tasks.t0057_tonic_gaba_sweep_t0053.code.constants import (  # noqa: E402
    ANGLES_DEG,
    COL_ACTIVE_FRACTION,
    COL_ANGLE_DEG,
    COL_GABA_BASE_NS,
    COL_IS_FIRED,
    COL_ONSET_TIME_MS,
    COL_SAMPLE_IDX,
    COL_SPIKE_TIME_S,
    COL_T_MS,
    COL_TRIAL_INDEX,
    COL_TRIAL_SEED,
    COL_VOLTAGE_MV,
    GABA_BASE_NS_VALUES,
    TSTOP_MS,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.paths import (  # noqa: E402
    ACTIVATION_TIMES_CSV,
    ACTIVE_FRACTION_CSV,
    DERIVED_QUANTITIES_JSON,
    DSI_PRIMARY_VS_GABA_PNG,
    DSI_VECTOR_SUM_VS_GABA_PNG,
    HWHM_VS_GABA_PNG,
    IMAGES_DIR,
    NULL_HZ_VS_GABA_PNG,
    PEAK_HZ_VS_GABA_PNG,
    RESULTS_DIR,
    RMSE_VS_GABA_PNG,
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


def _gaba_token(gaba_base_ns: float) -> str:
    """Encode a GABA value as a filename-safe token (e.g., ``0.50``)."""
    return f"{gaba_base_ns:.2f}"


def _voltage_pivot_per_angle_gaba(
    *,
    df: pd.DataFrame,
    angle_deg: int,
    gaba_base_ns: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (t_ms, mean_v, sd_v) arrays for the given (angle, gaba_base_ns)."""
    sub: pd.DataFrame = df[
        (df[COL_ANGLE_DEG] == angle_deg)
        & (np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6))
    ]
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


def _render_voltage_per_direction_per_gaba(
    *,
    voltage_csv: Path,
    out_dir: Path,
    prefix: str,
    title_prefix: str,
) -> None:
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=voltage_csv)
    for gaba_base_ns in GABA_BASE_NS_VALUES:
        token: str = _gaba_token(gaba_base_ns)
        for angle_deg in ANGLES_DEG:
            t_ms, mean_v, sd_v = _voltage_pivot_per_angle_gaba(
                df=df,
                angle_deg=angle_deg,
                gaba_base_ns=gaba_base_ns,
            )
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
                f"{title_prefix} GABA={token} nS dir={angle_deg} deg (n=10 trials, mean +/- SD)",
            )
            ax.legend(loc="lower right", frameon=False)
            out_path: Path = out_dir / f"{prefix}_gaba_{token}_dir_{angle_deg:03d}.png"
            fig.tight_layout()
            fig.savefig(fname=out_path)
            plt.close(fig=fig)


def render_soma_voltage_per_direction(*, out_dir: Path) -> None:
    _render_voltage_per_direction_per_gaba(
        voltage_csv=VOLTAGE_TRACES_FULL_CSV,
        out_dir=out_dir,
        prefix="v_soma",
        title_prefix="Soma V(t) FULL",
    )


def render_aggregate_epsp(*, out_dir: Path) -> None:
    _render_voltage_per_direction_per_gaba(
        voltage_csv=VOLTAGE_TRACES_AMPA_ONLY_CSV,
        out_dir=out_dir,
        prefix="epsp",
        title_prefix="Aggregate EPSP (AMPA-only)",
    )


def render_aggregate_ipsp(*, out_dir: Path) -> None:
    _render_voltage_per_direction_per_gaba(
        voltage_csv=VOLTAGE_TRACES_GABA_ONLY_CSV,
        out_dir=out_dir,
        prefix="ipsp",
        title_prefix="Aggregate IPSP (GABA-only)",
    )


def render_psth(*, out_dir: Path) -> None:
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=SPIKE_TIMES_FULL_CSV)
    bin_edges_ms: np.ndarray = np.arange(0.0, TSTOP_MS + PSTH_BIN_MS, PSTH_BIN_MS)
    bin_centers_ms: np.ndarray = bin_edges_ms[:-1] + 0.5 * PSTH_BIN_MS
    bin_width_s: float = PSTH_BIN_MS / 1000.0
    for gaba_base_ns in GABA_BASE_NS_VALUES:
        token: str = _gaba_token(gaba_base_ns)
        sub_g: pd.DataFrame = df[np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6)]
        n_trials_per_angle: int = (
            int(sub_g.groupby(COL_ANGLE_DEG)[COL_TRIAL_INDEX].nunique().max())
            if len(sub_g) > 0
            else 1
        )
        n_trials_per_angle = max(1, n_trials_per_angle)
        for angle_deg in ANGLES_DEG:
            sub = sub_g[sub_g[COL_ANGLE_DEG] == angle_deg]
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
            ax.set_title(f"PSTH FULL GABA={token} nS dir={angle_deg} deg (5 ms bins)")
            out_path: Path = out_dir / f"psth_gaba_{token}_dir_{angle_deg:03d}.png"
            fig.tight_layout()
            fig.savefig(fname=out_path)
            plt.close(fig=fig)


def render_activation_histogram(*, out_dir: Path) -> None:
    """Per-(gaba, direction) synapse activation histogram with is_fired overlay."""
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=ACTIVATION_TIMES_CSV)
    bin_edges_ms: np.ndarray = np.arange(0.0, TSTOP_MS + 10.0, 10.0)
    for gaba_base_ns in GABA_BASE_NS_VALUES:
        token: str = _gaba_token(gaba_base_ns)
        sub_g: pd.DataFrame = df[np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6)]
        for angle_deg in ANGLES_DEG:
            sub = sub_g[sub_g[COL_ANGLE_DEG] == angle_deg]
            onsets_ms: np.ndarray = sub[COL_ONSET_TIME_MS].to_numpy(dtype=np.float64)
            fired_onsets_ms: np.ndarray = sub.loc[
                sub[COL_IS_FIRED] == 1, COL_ONSET_TIME_MS
            ].to_numpy(dtype=np.float64)
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
            ax.set_title(
                f"Synapse activation GABA={token} nS dir={angle_deg} deg",
            )
            ax.legend(loc="upper right", frameon=False)
            out_path: Path = out_dir / f"activation_gaba_{token}_dir_{angle_deg:03d}.png"
            fig.tight_layout()
            fig.savefig(fname=out_path)
            plt.close(fig=fig)


def _write_per_gaba_curve_csv(*, gaba_base_ns: float, out_csv: Path) -> bool:
    """Pivot the FULL tuning-curve CSV to a single-conductance per-direction curve.

    Writes a CSV with the schema expected by ``plot_polar_tuning_curve`` /
    ``plot_cartesian_tuning_curve`` (angle_deg, trial_seed, firing_rate_hz). Returns True iff at
    least one row was written.
    """
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=TUNING_CURVE_FULL_CSV)
    sub: pd.DataFrame = df[np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6)]
    if len(sub) == 0:
        return False
    sub = sub[[COL_ANGLE_DEG, COL_TRIAL_SEED, "firing_rate_hz"]].copy()
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    sub.to_csv(out_csv, index=False)
    return True


def render_tuning_curves(*, out_dir: Path) -> None:
    target_csv: Path | None = TARGET_TUNING_CURVE_CSV if TARGET_TUNING_CURVE_CSV.exists() else None
    for gaba_base_ns in GABA_BASE_NS_VALUES:
        token: str = _gaba_token(gaba_base_ns)
        per_gaba_csv: Path = RESULTS_DIR / f"_tmp_tuning_curve_full_gaba_{token}.csv"
        if not _write_per_gaba_curve_csv(gaba_base_ns=gaba_base_ns, out_csv=per_gaba_csv):
            continue
        plot_polar_tuning_curve(
            per_gaba_csv,
            out_dir / f"polar_tuning_curve_gaba_{token}.png",
            target_csv=target_csv,
        )
        plot_cartesian_tuning_curve(
            per_gaba_csv,
            out_dir / f"cartesian_tuning_curve_gaba_{token}.png",
            target_csv=target_csv,
        )


def render_raster_psth(*, out_dir: Path) -> None:
    """Per-(gaba, direction) trial raster + PSTH via the t0011 ``tuning_curve_viz`` library.

    Writes a per-(gaba) temporary spike CSV (filtered to one conductance) then renders one PNG
    per direction.
    """
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=SPIKE_TIMES_FULL_CSV)
    for gaba_base_ns in GABA_BASE_NS_VALUES:
        token: str = _gaba_token(gaba_base_ns)
        sub: pd.DataFrame = df[np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6)]
        if len(sub) == 0:
            continue
        per_gaba_spike_csv: Path = RESULTS_DIR / f"_tmp_spike_times_full_gaba_{token}.csv"
        sub[[COL_ANGLE_DEG, COL_TRIAL_INDEX, COL_SPIKE_TIME_S]].to_csv(
            per_gaba_spike_csv,
            index=False,
        )
        for angle_deg in ANGLES_DEG:
            out_path: Path = out_dir / f"raster_psth_gaba_{token}_dir_{angle_deg:03d}.png"
            try:
                plot_angle_raster_psth(
                    per_gaba_spike_csv,
                    out_path,
                    angle_deg=float(angle_deg),
                )
            except ValueError:
                continue


def render_active_fraction_polar(
    *,
    active_fraction_csv: Path,
    out_dir: Path,
) -> None:
    """Polar plot of the per-direction fraction of I synapses fired (single PNG)."""
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=active_fraction_csv)
    df_sorted: pd.DataFrame = df.sort_values(by=COL_ANGLE_DEG).reset_index(drop=True)
    angles_deg: np.ndarray = df_sorted[COL_ANGLE_DEG].to_numpy(dtype=np.float64)
    fractions: np.ndarray = df_sorted[COL_ACTIVE_FRACTION].to_numpy(dtype=np.float64)

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


def _render_scalar_vs_gaba(
    *,
    gaba_axis: list[float],
    values: list[float | None],
    out_path: Path,
    y_label: str,
    title: str,
) -> None:
    """Render a single-curve scalar-vs-GABA_BASE_NS line plot with markers.

    Skips ``None`` entries (rendered as gaps) so the chart does not lie about uncomputed metrics.
    """
    xs: list[float] = []
    ys: list[float] = []
    for x, y in zip(gaba_axis, values, strict=True):
        if y is None:
            continue
        xs.append(x)
        ys.append(float(y))
    fig, ax = plt.subplots(figsize=FIG_SIZE_INCHES, dpi=FIG_DPI)
    ax.plot(xs, ys, color="tab:blue", linewidth=1.4, marker="o")
    ax.set_xlabel("GABA_BASE_NS (nS)")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(fname=out_path)
    plt.close(fig=fig)


def render_cross_conductance_summary(*, out_dir: Path) -> None:
    """Render the 6 cross-conductance summary plots from derived_quantities.json."""
    if not DERIVED_QUANTITIES_JSON.exists():
        print(
            f"[render] Skipping cross-conductance summary plots; "
            f"{DERIVED_QUANTITIES_JSON} not found.",
            flush=True,
        )
        return
    import json  # noqa: PLC0415

    derived: dict[str, object] = json.loads(DERIVED_QUANTITIES_JSON.read_text(encoding="utf-8"))
    gaba_axis: list[float] = list(derived["gaba_base_ns_values"])  # type: ignore[arg-type]
    panels: tuple[tuple[str, str, str, Path], ...] = (
        (
            "dsi_primary_vs_gaba",
            "DSI (primary)",
            "Primary DSI vs GABA_BASE_NS (FULL mode)",
            DSI_PRIMARY_VS_GABA_PNG,
        ),
        (
            "dsi_vector_sum_vs_gaba",
            "DSI (vector-sum)",
            "Vector-sum DSI vs GABA_BASE_NS (FULL mode)",
            DSI_VECTOR_SUM_VS_GABA_PNG,
        ),
        (
            "peak_hz_vs_gaba",
            "Peak Hz",
            "Peak firing rate vs GABA_BASE_NS (FULL mode)",
            PEAK_HZ_VS_GABA_PNG,
        ),
        (
            "null_hz_vs_gaba",
            "Null Hz",
            "Null firing rate vs GABA_BASE_NS (FULL mode)",
            NULL_HZ_VS_GABA_PNG,
        ),
        (
            "hwhm_vs_gaba",
            "HWHM (deg)",
            "Tuning HWHM vs GABA_BASE_NS (FULL mode)",
            HWHM_VS_GABA_PNG,
        ),
        (
            "rmse_vs_gaba",
            "RMSE vs t0004 target",
            "RMSE vs t0004 target tuning curve (FULL mode)",
            RMSE_VS_GABA_PNG,
        ),
    )
    _ = out_dir  # kept for symmetry; output paths are absolute via paths.py
    for key, y_label, title, out_path in panels:
        values_obj: object = derived.get(key, [])
        if not isinstance(values_obj, list):
            continue
        # Cast list[object] -> list[float | None]; None entries are skipped.
        coerced: list[float | None] = []
        for v in values_obj:
            if v is None:
                coerced.append(None)
            else:
                coerced.append(float(v))  # type: ignore[arg-type]
        _render_scalar_vs_gaba(
            gaba_axis=gaba_axis,
            values=coerced,
            out_path=out_path,
            y_label=y_label,
            title=title,
        )


def main() -> int:
    _ensure_images_dir()
    print("[render] soma voltage (FULL) per (gaba, direction)...", flush=True)
    render_soma_voltage_per_direction(out_dir=IMAGES_DIR)
    print("[render] aggregate EPSP (AMPA_ONLY) per (gaba, direction)...", flush=True)
    render_aggregate_epsp(out_dir=IMAGES_DIR)
    print("[render] aggregate IPSP (GABA_ONLY) per (gaba, direction)...", flush=True)
    render_aggregate_ipsp(out_dir=IMAGES_DIR)
    print("[render] PSTH (FULL) per (gaba, direction)...", flush=True)
    render_psth(out_dir=IMAGES_DIR)
    print("[render] synapse activation histogram per (gaba, direction)...", flush=True)
    render_activation_histogram(out_dir=IMAGES_DIR)
    print("[render] polar + cartesian tuning curves per gaba...", flush=True)
    render_tuning_curves(out_dir=IMAGES_DIR)
    print("[render] raster+PSTH per (gaba, direction) (t0011 lib)...", flush=True)
    render_raster_psth(out_dir=IMAGES_DIR)
    print("[render] active fraction polar plot...", flush=True)
    render_active_fraction_polar(
        active_fraction_csv=ACTIVE_FRACTION_CSV,
        out_dir=IMAGES_DIR,
    )
    print("[render] cross-conductance summary plots...", flush=True)
    render_cross_conductance_summary(out_dir=IMAGES_DIR)
    print(f"[render] Done. PNGs written under {IMAGES_DIR}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
