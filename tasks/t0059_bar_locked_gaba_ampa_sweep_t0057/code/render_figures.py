"""Per-(gampa, gaba, direction) and cross-grid figures for the t0059 minimal DSGC.

Adapted from ``tasks/t0057_tonic_gaba_sweep_t0053/code/render_figures.py``. The inner per-direction
loop is wrapped by an outer loop over the 5x5 (gampa, gaba) grid. Five per-cell figure families
per (gampa, gaba) cell, plus six cross-grid heatmaps and a regime-boundary contour overlay:

Per-cell (25 cells x [12 + 12 + 12 + 12 + 1] = 1225 PNGs):
  * ``soma_v_gampa_<g>_gaba_<b>_theta_<a>.png``     soma V(t) FULL.
  * ``epsp_gampa_<g>_gaba_<b>_theta_<a>.png``       aggregate EPSP at soma (EPSP_PASSIVE).
  * ``ipsp_gampa_<g>_gaba_<b>_theta_<a>.png``       aggregate IPSP at soma (IPSP_PASSIVE).
  * ``psth_gampa_<g>_gaba_<b>_theta_<a>.png``       firing-rate PSTH FULL.
  * ``polar_tuning_curve_gampa_<g>_gaba_<b>.png``   polar tuning curve FULL.

Cross-grid (8 PNGs):
  * ``heatmap_dsi_primary.png``, ``heatmap_dsi_vector_sum.png``, ``heatmap_peak_hz.png``,
    ``heatmap_null_hz.png``, ``heatmap_hwhm.png``, ``heatmap_rmse.png`` — pcolormesh.
  * ``regime_boundary_contour.png`` — contour overlay on FULL peak Hz grid.
  * ``active_fraction_polar.png`` — single PNG, conductance-independent.
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
    plot_polar_tuning_curve,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants import (  # noqa: E402
    AMPA_PEAK_NS_VALUES,
    ANGLES_DEG,
    COL_ACTIVE_FRACTION,
    COL_ANGLE_DEG,
    COL_GABA_BASE_NS,
    COL_GAMPA_NS,
    COL_SAMPLE_IDX,
    COL_SPIKE_TIME_S,
    COL_T_MS,
    COL_TRIAL_INDEX,
    COL_TRIAL_SEED,
    COL_VOLTAGE_MV,
    GABA_BASE_NS_VALUES,
    TSTOP_MS,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.paths import (  # noqa: E402
    ACTIVE_FRACTION_CSV,
    DERIVED_QUANTITIES_JSON,
    HEATMAP_DSI_PRIMARY_PNG,
    HEATMAP_DSI_VECTOR_SUM_PNG,
    HEATMAP_HWHM_PNG,
    HEATMAP_NULL_HZ_PNG,
    HEATMAP_PEAK_HZ_PNG,
    HEATMAP_RMSE_PNG,
    IMAGES_DIR,
    REGIME_BOUNDARY_CONTOUR_PNG,
    RESULTS_DIR,
    SPIKE_TIMES_FULL_CSV,
    TARGET_TUNING_CURVE_CSV,
    TUNING_CURVE_FULL_CSV,
    VOLTAGE_TRACES_EPSP_PASSIVE_CSV,
    VOLTAGE_TRACES_FULL_CSV,
    VOLTAGE_TRACES_IPSP_PASSIVE_CSV,
)

FIG_DPI: int = 100
FIG_SIZE_INCHES: tuple[float, float] = (6.0, 4.0)
PSTH_BIN_MS: float = 5.0


def _ensure_images_dir() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def _gampa_token(gampa_ns: float) -> str:
    return f"{gampa_ns:.2f}"


def _gaba_token(gaba_base_ns: float) -> str:
    return f"{gaba_base_ns:.2f}"


def _voltage_pivot_per_angle_cell(
    *,
    df: pd.DataFrame,
    gampa_ns: float,
    gaba_base_ns: float,
    angle_deg: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (t_ms, mean_v, sd_v) arrays for the given (gampa, gaba, angle)."""
    sub: pd.DataFrame = df[
        (df[COL_ANGLE_DEG] == angle_deg)
        & np.isclose(df[COL_GAMPA_NS], gampa_ns, atol=1e-6)
        & np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6)
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


def _render_voltage_per_cell(
    *,
    voltage_csv: Path,
    out_dir: Path,
    prefix: str,
    title_prefix: str,
) -> None:
    if not voltage_csv.exists():
        print(f"[render] skip {prefix}: {voltage_csv} not found", flush=True)
        return
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=voltage_csv)
    for gampa_ns in AMPA_PEAK_NS_VALUES:
        for gaba_base_ns in GABA_BASE_NS_VALUES:
            ga_tok: str = _gampa_token(gampa_ns)
            gb_tok: str = _gaba_token(gaba_base_ns)
            for angle_deg in ANGLES_DEG:
                t_ms, mean_v, sd_v = _voltage_pivot_per_angle_cell(
                    df=df,
                    gampa_ns=gampa_ns,
                    gaba_base_ns=gaba_base_ns,
                    angle_deg=angle_deg,
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
                    f"{title_prefix} gAMPA={ga_tok} gGABA={gb_tok} theta={angle_deg} deg",
                )
                ax.legend(loc="lower right", frameon=False)
                out_path: Path = (
                    out_dir / f"{prefix}_gampa_{ga_tok}_gaba_{gb_tok}_theta_{angle_deg:03d}.png"
                )
                fig.tight_layout()
                fig.savefig(fname=out_path)
                plt.close(fig=fig)


def render_soma_voltage_per_cell(*, out_dir: Path) -> None:
    _render_voltage_per_cell(
        voltage_csv=VOLTAGE_TRACES_FULL_CSV,
        out_dir=out_dir,
        prefix="soma_v",
        title_prefix="Soma V(t) FULL",
    )


def render_aggregate_epsp(*, out_dir: Path) -> None:
    _render_voltage_per_cell(
        voltage_csv=VOLTAGE_TRACES_EPSP_PASSIVE_CSV,
        out_dir=out_dir,
        prefix="epsp",
        title_prefix="Aggregate EPSP (passive)",
    )


def render_aggregate_ipsp(*, out_dir: Path) -> None:
    _render_voltage_per_cell(
        voltage_csv=VOLTAGE_TRACES_IPSP_PASSIVE_CSV,
        out_dir=out_dir,
        prefix="ipsp",
        title_prefix="Aggregate IPSP (passive)",
    )


def render_psth(*, out_dir: Path) -> None:
    if not SPIKE_TIMES_FULL_CSV.exists():
        print("[render] skip PSTH: spike_times_full.csv not found", flush=True)
        return
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=SPIKE_TIMES_FULL_CSV)
    bin_edges_ms: np.ndarray = np.arange(0.0, TSTOP_MS + PSTH_BIN_MS, PSTH_BIN_MS)
    bin_centers_ms: np.ndarray = bin_edges_ms[:-1] + 0.5 * PSTH_BIN_MS
    bin_width_s: float = PSTH_BIN_MS / 1000.0
    for gampa_ns in AMPA_PEAK_NS_VALUES:
        for gaba_base_ns in GABA_BASE_NS_VALUES:
            ga_tok: str = _gampa_token(gampa_ns)
            gb_tok: str = _gaba_token(gaba_base_ns)
            sub_cell: pd.DataFrame = df[
                np.isclose(df[COL_GAMPA_NS], gampa_ns, atol=1e-6)
                & np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6)
            ]
            n_trials_per_angle: int = (
                int(sub_cell.groupby(COL_ANGLE_DEG)[COL_TRIAL_INDEX].nunique().max())
                if len(sub_cell) > 0
                else 1
            )
            n_trials_per_angle = max(1, n_trials_per_angle)
            for angle_deg in ANGLES_DEG:
                sub = sub_cell[sub_cell[COL_ANGLE_DEG] == angle_deg]
                spike_times_ms: np.ndarray = (
                    sub[COL_SPIKE_TIME_S].to_numpy(dtype=np.float64) * 1000.0
                )
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
                    f"PSTH FULL gAMPA={ga_tok} gGABA={gb_tok} theta={angle_deg} deg",
                )
                out_path: Path = (
                    out_dir / f"psth_gampa_{ga_tok}_gaba_{gb_tok}_theta_{angle_deg:03d}.png"
                )
                fig.tight_layout()
                fig.savefig(fname=out_path)
                plt.close(fig=fig)


def _write_per_cell_curve_csv(
    *,
    gampa_ns: float,
    gaba_base_ns: float,
    out_csv: Path,
) -> bool:
    """Pivot the FULL tuning-curve CSV to a single-cell per-direction curve.

    Writes a CSV with the schema expected by ``plot_polar_tuning_curve`` (angle_deg, trial_seed,
    firing_rate_hz). Returns True iff at least one row was written.
    """
    if not TUNING_CURVE_FULL_CSV.exists():
        return False
    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=TUNING_CURVE_FULL_CSV)
    sub: pd.DataFrame = df[
        np.isclose(df[COL_GAMPA_NS], gampa_ns, atol=1e-6)
        & np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6)
    ]
    if len(sub) == 0:
        return False
    sub_out = sub[[COL_ANGLE_DEG, COL_TRIAL_SEED, "firing_rate_hz"]].copy()
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    sub_out.to_csv(out_csv, index=False)
    return True


def render_polar_tuning_curves(*, out_dir: Path) -> None:
    target_csv: Path | None = TARGET_TUNING_CURVE_CSV if TARGET_TUNING_CURVE_CSV.exists() else None
    for gampa_ns in AMPA_PEAK_NS_VALUES:
        for gaba_base_ns in GABA_BASE_NS_VALUES:
            ga_tok: str = _gampa_token(gampa_ns)
            gb_tok: str = _gaba_token(gaba_base_ns)
            per_cell_csv: Path = (
                RESULTS_DIR / f"_tmp_tuning_curve_full_gampa_{ga_tok}_gaba_{gb_tok}.csv"
            )
            if not _write_per_cell_curve_csv(
                gampa_ns=gampa_ns,
                gaba_base_ns=gaba_base_ns,
                out_csv=per_cell_csv,
            ):
                continue
            out_path: Path = out_dir / f"polar_tuning_curve_gampa_{ga_tok}_gaba_{gb_tok}.png"
            try:
                plot_polar_tuning_curve(per_cell_csv, out_path, target_csv=target_csv)
            except (ValueError, ZeroDivisionError) as exc:
                print(
                    f"[render] polar plot at gampa={ga_tok}, gaba={gb_tok} failed: {exc}",
                    flush=True,
                )


def render_active_fraction_polar(*, active_fraction_csv: Path, out_dir: Path) -> None:
    """Polar plot of the per-direction fraction of I synapses fired (single PNG)."""
    if not active_fraction_csv.exists():
        return
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


def _grid_to_masked(grid: list[list[float | None]]) -> np.ma.MaskedArray:
    """Convert a 2D Python list (with None entries) to a numpy masked array."""
    arr: np.ndarray = np.full(
        shape=(len(grid), len(grid[0]) if len(grid) > 0 else 0),
        fill_value=np.nan,
        dtype=np.float64,
    )
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val is None:
                arr[i, j] = np.nan
            else:
                arr[i, j] = float(val)
    return np.ma.masked_invalid(arr)


def _render_heatmap(
    *,
    grid: list[list[float | None]] | list[list[float]],
    gampa_axis: list[float],
    gaba_axis: list[float],
    out_path: Path,
    title: str,
    cbar_label: str,
) -> None:
    """Render one (gampa, gaba) heatmap with masked NaN cells."""
    grid_typed: list[list[float | None]] = [
        [None if v is None else float(v) for v in row]  # type: ignore[union-attr]
        for row in grid
    ]
    masked: np.ma.MaskedArray = _grid_to_masked(grid_typed)

    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=FIG_DPI)
    cmap = matplotlib.cm.get_cmap("viridis").copy()
    cmap.set_bad("lightgray")
    # pcolormesh draws cells centred between coordinates; build edge arrays.
    gaba_edges: np.ndarray = _build_log_edges(gaba_axis)
    gampa_edges: np.ndarray = _build_log_edges(gampa_axis)
    mesh = ax.pcolormesh(
        gaba_edges,
        gampa_edges,
        masked,
        cmap=cmap,
        shading="flat",
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("GABA_BASE_NS (nS)")
    ax.set_ylabel("gAMPA (nS)")
    ax.set_title(title)
    ax.set_xticks(gaba_axis)
    ax.set_xticklabels([f"{g:.2f}" for g in gaba_axis])
    ax.set_yticks(gampa_axis)
    ax.set_yticklabels([f"{g:.2f}" for g in gampa_axis])
    fig.colorbar(mesh, ax=ax, label=cbar_label)
    fig.tight_layout()
    fig.savefig(fname=out_path)
    plt.close(fig=fig)


def _build_log_edges(axis_values: list[float]) -> np.ndarray:
    """Build edges around log-spaced cell centres so pcolormesh draws cells centred on values."""
    arr: np.ndarray = np.asarray(axis_values, dtype=np.float64)
    log_arr: np.ndarray = np.log10(arr)
    edges_log: np.ndarray = np.zeros(len(arr) + 1, dtype=np.float64)
    if len(arr) == 1:
        edges_log[0] = log_arr[0] - 0.5
        edges_log[1] = log_arr[0] + 0.5
    else:
        edges_log[0] = log_arr[0] - 0.5 * (log_arr[1] - log_arr[0])
        edges_log[-1] = log_arr[-1] + 0.5 * (log_arr[-1] - log_arr[-2])
        for i in range(1, len(arr)):
            edges_log[i] = 0.5 * (log_arr[i - 1] + log_arr[i])
    return np.power(10.0, edges_log)


def render_heatmaps(*, out_dir: Path) -> None:
    if not DERIVED_QUANTITIES_JSON.exists():
        print(
            f"[render] Skipping heatmaps; {DERIVED_QUANTITIES_JSON} not found.",
            flush=True,
        )
        return
    derived: dict[str, object] = json.loads(DERIVED_QUANTITIES_JSON.read_text(encoding="utf-8"))
    gampa_axis_obj: object = derived.get("ampa_peak_ns_values", [])
    gaba_axis_obj: object = derived.get("gaba_base_ns_values", [])
    assert isinstance(gampa_axis_obj, list), "ampa_peak_ns_values must be a list"
    assert isinstance(gaba_axis_obj, list), "gaba_base_ns_values must be a list"
    gampa_axis: list[float] = [float(v) for v in gampa_axis_obj]
    gaba_axis: list[float] = [float(v) for v in gaba_axis_obj]

    panels: tuple[tuple[str, str, str, Path], ...] = (
        (
            "dsi_primary_grid",
            "Primary DSI (FULL mode)",
            "DSI",
            HEATMAP_DSI_PRIMARY_PNG,
        ),
        (
            "dsi_vector_sum_grid",
            "Vector-sum DSI (FULL mode)",
            "DSI",
            HEATMAP_DSI_VECTOR_SUM_PNG,
        ),
        (
            "peak_hz_grid",
            "Peak firing rate Hz (FULL mode)",
            "Hz",
            HEATMAP_PEAK_HZ_PNG,
        ),
        (
            "null_hz_grid",
            "Null firing rate Hz (FULL mode)",
            "Hz",
            HEATMAP_NULL_HZ_PNG,
        ),
        (
            "hwhm_grid",
            "Tuning HWHM (deg, FULL mode)",
            "deg",
            HEATMAP_HWHM_PNG,
        ),
        (
            "rmse_grid",
            "RMSE vs t0004 target (Hz, FULL mode)",
            "Hz",
            HEATMAP_RMSE_PNG,
        ),
    )
    for key, title, cbar_label, out_path in panels:
        grid_obj: object = derived.get(key, [])
        if not isinstance(grid_obj, list):
            continue
        # Coerce list[list[?]] -> list[list[float | None]]
        coerced: list[list[float | None]] = []
        for row_obj in grid_obj:
            if not isinstance(row_obj, list):
                continue
            coerced.append([None if v is None else float(v) for v in row_obj])  # type: ignore[arg-type]
        _render_heatmap(
            grid=coerced,
            gampa_axis=gampa_axis,
            gaba_axis=gaba_axis,
            out_path=out_path,
            title=title,
            cbar_label=cbar_label,
        )


def render_regime_boundary_contour(*, out_dir: Path) -> None:
    """Contour overlay: peak Hz on (gampa, gaba) plane with three regime bands."""
    if not DERIVED_QUANTITIES_JSON.exists():
        return
    derived: dict[str, object] = json.loads(DERIVED_QUANTITIES_JSON.read_text(encoding="utf-8"))
    gampa_axis_obj: object = derived.get("ampa_peak_ns_values", [])
    gaba_axis_obj: object = derived.get("gaba_base_ns_values", [])
    grid_obj: object = derived.get("peak_hz_grid", [])
    assert isinstance(gampa_axis_obj, list)
    assert isinstance(gaba_axis_obj, list)
    if not isinstance(grid_obj, list):
        return
    gampa_axis: list[float] = [float(v) for v in gampa_axis_obj]
    gaba_axis: list[float] = [float(v) for v in gaba_axis_obj]
    arr: np.ndarray = np.asarray(
        [
            [float(v) if v is not None else 0.0 for v in row_obj]  # type: ignore[arg-type]
            for row_obj in grid_obj
            if isinstance(row_obj, list)
        ],
        dtype=np.float64,
    )

    fig, ax = plt.subplots(figsize=(7.0, 5.5), dpi=FIG_DPI)
    cmap = matplotlib.cm.get_cmap("magma")
    gampa_grid, gaba_grid = np.meshgrid(gampa_axis, gaba_axis, indexing="ij")
    pc = ax.pcolormesh(
        _build_log_edges(gaba_axis),
        _build_log_edges(gampa_axis),
        arr,
        cmap=cmap,
        shading="flat",
    )
    cs = ax.contour(
        gaba_grid,
        gampa_grid,
        arr,
        levels=[0.5, 5.0, 50.0],
        colors=["white", "cyan", "yellow"],
        linewidths=1.5,
    )
    ax.clabel(cs, inline=True, fontsize=8, fmt="%g Hz")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("GABA_BASE_NS (nS)")
    ax.set_ylabel("gAMPA (nS)")
    ax.set_title(
        "Peak Hz regime boundaries: full-suppression (<0.5), single-spike (0.5-5), "
        "multi-spike (5-50)",
    )
    ax.set_xticks(gaba_axis)
    ax.set_xticklabels([f"{g:.2f}" for g in gaba_axis])
    ax.set_yticks(gampa_axis)
    ax.set_yticklabels([f"{g:.2f}" for g in gampa_axis])
    fig.colorbar(pc, ax=ax, label="peak Hz (FULL)")
    fig.tight_layout()
    fig.savefig(fname=REGIME_BOUNDARY_CONTOUR_PNG)
    plt.close(fig=fig)


def main() -> int:
    _ensure_images_dir()
    print("[render] soma voltage (FULL) per (gampa, gaba, direction)...", flush=True)
    render_soma_voltage_per_cell(out_dir=IMAGES_DIR)
    print("[render] aggregate EPSP (EPSP_PASSIVE) per (gampa, gaba, direction)...", flush=True)
    render_aggregate_epsp(out_dir=IMAGES_DIR)
    print("[render] aggregate IPSP (IPSP_PASSIVE) per (gampa, gaba, direction)...", flush=True)
    render_aggregate_ipsp(out_dir=IMAGES_DIR)
    print("[render] PSTH (FULL) per (gampa, gaba, direction)...", flush=True)
    render_psth(out_dir=IMAGES_DIR)
    print("[render] polar tuning curves per (gampa, gaba)...", flush=True)
    render_polar_tuning_curves(out_dir=IMAGES_DIR)
    print("[render] active fraction polar plot...", flush=True)
    render_active_fraction_polar(
        active_fraction_csv=ACTIVE_FRACTION_CSV,
        out_dir=IMAGES_DIR,
    )
    print("[render] cross-grid heatmaps...", flush=True)
    render_heatmaps(out_dir=IMAGES_DIR)
    print("[render] regime-boundary contour...", flush=True)
    render_regime_boundary_contour(out_dir=IMAGES_DIR)
    print(f"[render] Done. PNGs written under {IMAGES_DIR}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
