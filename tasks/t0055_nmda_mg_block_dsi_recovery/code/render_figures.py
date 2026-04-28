"""Per-(gNMDA × direction) figures and sweep-summary plots for t0055 minimal DSGC Mg-block NMDA.

Adapted from ``tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/render_figures.py``. Three
existing sweep-summary functions gain a t0054 overlay curve (loaded from t0054's
``derived_quantities.json`` and ``metrics.json``); a new fourth sweep-summary function
``render_mg_block_g_v_curve`` plots the analytical Boltzmann factor alongside the empirical peak
gNMDA values from the voltage-dependence sanity gate.
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
from tasks.t0055_nmda_mg_block_dsi_recovery.code.constants import (  # noqa: E402
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
    MG_BLOCK_GAMMA,
    MG_BLOCK_N,
    NMDA_PEAK_NS_VALUES,
    TSTOP_MS,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.paths import (  # noqa: E402
    ACTIVATION_TIMES_CSV,
    DERIVED_QUANTITIES_JSON,
    DSI_VS_GNMDA_PNG,
    EPSP_DECAY_VS_GNMDA_PNG,
    IMAGES_DIR,
    METRICS_JSON,
    MG_BLOCK_G_V_EMPIRICAL_JSON,
    MG_BLOCK_G_V_PNG,
    PEAK_HZ_VS_GNMDA_PNG,
    SPIKE_TIMES_FULL_CSV,
    T0054_DERIVED_QUANTITIES_JSON,
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


def _load_t0054_derived() -> dict[str, object] | None:
    """Return t0054's derived_quantities.json (for overlay curves) or None if missing."""
    if not T0054_DERIVED_QUANTITIES_JSON.exists():
        return None
    return json.loads(T0054_DERIVED_QUANTITIES_JSON.read_text(encoding="utf-8"))


def _t0054_per_variant_field(*, field: str) -> dict[float, float]:
    """Return ``{gnmda_ns: <field>}`` from t0054's derived_quantities.json FULL variants."""
    derived: dict[str, object] | None = _load_t0054_derived()
    out: dict[float, float] = {}
    if derived is None:
        return out
    per_variant: object = derived.get("per_variant", {})
    if not isinstance(per_variant, dict):
        return out
    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        key: str = f"gnmda_{gnmda_ns:.2f}_full"
        if key not in per_variant:
            continue
        variant: object = per_variant[key]
        if not isinstance(variant, dict):
            continue
        value: object = variant.get(field)
        if value is None:
            continue
        out[gnmda_ns] = float(value)  # type: ignore[arg-type]
    return out


def _t0054_per_gnmda_field(*, field: str) -> dict[float, float]:
    """Return ``{gnmda_ns: <field>}`` from t0054's derived_quantities.json per-gNMDA block."""
    derived: dict[str, object] | None = _load_t0054_derived()
    out: dict[float, float] = {}
    if derived is None:
        return out
    per_gnmda: object = derived.get("per_gnmda", {})
    if not isinstance(per_gnmda, dict):
        return out
    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        key: str = f"{gnmda_ns:.2f}"
        if key not in per_gnmda:
            continue
        block: object = per_gnmda[key]
        if not isinstance(block, dict):
            continue
        value: object = block.get(field)
        if value is None:
            continue
        out[gnmda_ns] = float(value)  # type: ignore[arg-type]
    return out


def render_epsp_decay_vs_gnmda(*, out_path: Path) -> None:
    derived: dict[str, object] = _load_derived()
    per_gnmda: dict[str, dict[str, object]] = derived["per_gnmda"]  # type: ignore[assignment]
    xs_t0055: list[float] = []
    ys_t0055: list[float] = []
    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        key: str = f"{gnmda_ns:.2f}"
        if key not in per_gnmda:
            continue
        decay_obj: object = per_gnmda[key].get("epsp_decay_to_1e_ms")
        if decay_obj is None:
            continue
        xs_t0055.append(gnmda_ns)
        ys_t0055.append(float(decay_obj))  # type: ignore[arg-type]

    t0054_decay: dict[float, float] = _t0054_per_gnmda_field(field="epsp_decay_to_1e_ms")
    xs_t0054: list[float] = sorted(t0054_decay.keys())
    ys_t0054: list[float] = [t0054_decay[x] for x in xs_t0054]

    fig, ax = plt.subplots(figsize=FIG_SIZE_INCHES, dpi=FIG_DPI)
    if len(xs_t0055) > 0:
        ax.plot(xs_t0055, ys_t0055, marker="o", color="tab:blue", label="t0055 (Mg-block NMDA)")
    if len(xs_t0054) > 0:
        ax.plot(
            xs_t0054,
            ys_t0054,
            marker="s",
            linestyle="--",
            color="tab:gray",
            label="t0054 (no Mg block)",
        )
    if len(xs_t0055) == 0 and len(xs_t0054) == 0:
        ax.text(
            0.5,
            0.5,
            "no data: both t0055 and t0054 EPSP decays are null\n"
            "(likely tau2 = 80 ms exceeds the 1500 ms trial window)",
            ha="center",
            va="center",
            transform=ax.transAxes,
        )
    ax.set_xlabel("gNMDA (nS)")
    ax.set_ylabel("EPSP decay-to-1/e (ms)")
    ax.set_title("EPSP decay-to-1/e vs gNMDA (E_ONLY at preferred direction)")
    ax.grid(visible=True, alpha=0.3)
    ax.legend(loc="best", frameon=False)
    fig.tight_layout()
    fig.savefig(fname=out_path)
    plt.close(fig=fig)


def render_peak_hz_vs_gnmda(*, out_path: Path) -> None:
    derived: dict[str, object] = _load_derived()
    per_variant: dict[str, dict[str, object]] = derived["per_variant"]  # type: ignore[assignment]
    xs_t0055: list[float] = []
    ys_t0055: list[float] = []
    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        key: str = f"gnmda_{gnmda_ns:.2f}_full"
        if key not in per_variant:
            continue
        peak_hz_obj: object = per_variant[key].get("peak_hz")
        if peak_hz_obj is None:
            continue
        xs_t0055.append(gnmda_ns)
        ys_t0055.append(float(peak_hz_obj))  # type: ignore[arg-type]

    t0054_peak: dict[float, float] = _t0054_per_variant_field(field="peak_hz")
    xs_t0054: list[float] = sorted(t0054_peak.keys())
    ys_t0054: list[float] = [t0054_peak[x] for x in xs_t0054]

    fig, ax = plt.subplots(figsize=FIG_SIZE_INCHES, dpi=FIG_DPI)
    ax.plot(xs_t0055, ys_t0055, marker="o", color="tab:purple", label="t0055 (Mg-block NMDA)")
    if len(xs_t0054) > 0:
        ax.plot(
            xs_t0054,
            ys_t0054,
            marker="s",
            linestyle="--",
            color="tab:gray",
            label="t0054 (no Mg block)",
        )
    ax.set_xlabel("gNMDA (nS)")
    ax.set_ylabel("peak firing rate (Hz)")
    ax.set_title("Peak Hz vs gNMDA (FULL mode)")
    ax.grid(visible=True, alpha=0.3)
    ax.legend(loc="best", frameon=False)
    fig.tight_layout()
    fig.savefig(fname=out_path)
    plt.close(fig=fig)


def render_dsi_vs_gnmda(*, out_path: Path) -> None:
    derived: dict[str, object] = _load_derived()
    per_variant: dict[str, dict[str, object]] = derived["per_variant"]  # type: ignore[assignment]
    xs_t0055: list[float] = []
    vector_dsi: list[float] = []
    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        key: str = f"gnmda_{gnmda_ns:.2f}_full"
        if key not in per_variant:
            continue
        vsd_obj: object = per_variant[key].get("vector_sum_dsi")
        if vsd_obj is None:
            continue
        xs_t0055.append(gnmda_ns)
        vector_dsi.append(float(vsd_obj))  # type: ignore[arg-type]

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

    t0054_vsd: dict[float, float] = _t0054_per_variant_field(field="vector_sum_dsi")
    xs_t0054: list[float] = sorted(t0054_vsd.keys())
    ys_t0054: list[float] = [t0054_vsd[x] for x in xs_t0054]

    fig, ax = plt.subplots(figsize=FIG_SIZE_INCHES, dpi=FIG_DPI)
    ax.plot(xs_t0055, vector_dsi, marker="o", color="tab:blue", label="t0055 vector-sum DSI")
    if len(primary_xs) > 0:
        ax.plot(
            primary_xs,
            primary_ys,
            marker="s",
            color="tab:red",
            label="t0055 primary DSI (registered)",
        )
    if len(xs_t0054) > 0:
        ax.plot(
            xs_t0054,
            ys_t0054,
            marker="^",
            linestyle="--",
            color="tab:gray",
            label="t0054 vector-sum DSI (no Mg)",
        )
    ax.axhline(y=0.50, color="black", linestyle=":", alpha=0.5, linewidth=1.0)
    ax.set_xlabel("gNMDA (nS)")
    ax.set_ylabel("DSI")
    ax.set_title("DSI vs gNMDA (FULL mode)")
    ax.legend(loc="best", frameon=False)
    ax.grid(visible=True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(fname=out_path)
    plt.close(fig=fig)


def render_mg_block_g_v_curve(*, out_path: Path) -> None:
    """Plot the analytical Boltzmann factor and the empirical peak gNMDA from Step 13."""
    if not MG_BLOCK_G_V_EMPIRICAL_JSON.exists():
        print(
            f"[render] {MG_BLOCK_G_V_EMPIRICAL_JSON.name} not found; cannot render Mg-block g(v).",
            flush=True,
        )
        return
    payload: object = json.loads(MG_BLOCK_G_V_EMPIRICAL_JSON.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        print("[render] mg_block_g_v_empirical.json is malformed; skipping.", flush=True)
        return

    v_clamp: list[float] = []
    peak_g: list[float] = []
    for entry in payload:
        if not isinstance(entry, dict):
            continue
        v_clamp.append(float(entry["v_clamp_mv"]))
        peak_g.append(float(entry["peak_g_us"]))

    v_clamp_arr: np.ndarray = np.asarray(v_clamp, dtype=np.float64)
    peak_g_arr: np.ndarray = np.asarray(peak_g, dtype=np.float64)
    # Normalise empirical curve to its value at +20 mV so it is directly comparable to the
    # analytical Boltzmann factor f(v) which approaches 1.0 at high v.
    if peak_g_arr.size == 0:
        return
    norm_idx: int = int(np.argmax(v_clamp_arr))
    norm_value: float = float(peak_g_arr[norm_idx])
    if norm_value > 0.0:
        peak_g_norm: np.ndarray = peak_g_arr / norm_value
    else:
        peak_g_norm = peak_g_arr

    v_dense: np.ndarray = np.linspace(-90.0, 30.0, 241)
    boltzmann: np.ndarray = 1.0 / (1.0 + MG_BLOCK_N * np.exp(-MG_BLOCK_GAMMA * v_dense))
    # Normalise analytical curve at v = +20 mV for the same reference.
    boltzmann_at_norm: float = float(
        1.0 / (1.0 + MG_BLOCK_N * np.exp(-MG_BLOCK_GAMMA * float(v_clamp_arr[norm_idx])))
    )
    if boltzmann_at_norm > 0.0:
        boltzmann_norm: np.ndarray = boltzmann / boltzmann_at_norm
    else:
        boltzmann_norm = boltzmann

    fig, ax = plt.subplots(figsize=FIG_SIZE_INCHES, dpi=FIG_DPI)
    ax.plot(
        v_dense,
        boltzmann_norm,
        color="tab:blue",
        linewidth=1.5,
        label=(
            f"Boltzmann 1 / (1 + {MG_BLOCK_N:.2f} * exp(-{MG_BLOCK_GAMMA:.2f} * v)),\n"
            "normalised at +20 mV"
        ),
    )
    ax.plot(
        v_clamp_arr,
        peak_g_norm,
        marker="o",
        linestyle="",
        color="tab:red",
        label="empirical peak g (normalised)",
    )
    ax.set_xlabel("clamp voltage (mV)")
    ax.set_ylabel("Mg-block factor (normalised)")
    ax.set_title("NMDA Mg-block g(v) sanity: analytical vs SEClamp peak g")
    ax.grid(visible=True, alpha=0.3)
    ax.legend(loc="lower right", frameon=False)
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
    print(
        "[render] sweep summaries: epsp_decay / peak_hz / dsi vs gNMDA + Mg-block g(v)...",
        flush=True,
    )
    render_epsp_decay_vs_gnmda(out_path=EPSP_DECAY_VS_GNMDA_PNG)
    render_peak_hz_vs_gnmda(out_path=PEAK_HZ_VS_GNMDA_PNG)
    render_dsi_vs_gnmda(out_path=DSI_VS_GNMDA_PNG)
    render_mg_block_g_v_curve(out_path=MG_BLOCK_G_V_PNG)
    print(f"[render] Done. PNGs written under {IMAGES_DIR}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
