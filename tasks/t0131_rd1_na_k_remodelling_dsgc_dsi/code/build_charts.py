"""Step 15: build every chart in results/images/ from the files written by the run scripts."""

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_io import (  # noqa: E402
    load_reference_cells,
    load_trace,
    trace_exists,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (  # noqa: E402
    CLAMP_HOLD_PRE_MS,
    S_K_GRID,
    S_NA_GRID,
    TARGET_SUSTAINED_RATIO,
    TARGET_TRANSIENT_RATIO,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (  # noqa: E402
    ARM_DECISION_JSON,
    BIAS_TUNING_CSV,
    CHOSEN_BIAS_JSON,
    CLAMP_GRID_CSV,
    DSI_HEATMAP_CSV,
    DSI_RESULTS_CSV,
    FI_CURVES_CSV,
    FITTED_SCALINGS_JSON,
    IMAGES_DIR,
    PANEL_D_PSTH_NPZ,
    PANEL_D_PULSES_CSV,
    PANEL_D_SWEEP_CSV,
    PANEL_D_VERDICTS_JSON,
    SPONTANEOUS_SUMMARY_CSV,
    TOY_PARAMS_JSON,
    with_arm_suffix,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.toy_model import (  # noqa: E402
    ToyParams,
    rate_static,
    simulate_pulse_response,
)

C_WT: str = "#1f77b4"
C_RD1: str = "#e8710a"
C_GREY: str = "#6b6b6b"
DPI: int = 160
N_EXAMPLE_CELLS: int = 3


def _save(*, fig: Figure, name: str) -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMAGES_DIR / name, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def _clean(ax: Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def _example_cells() -> list[str]:
    cells = load_reference_cells()
    picked: list[str] = []
    seen: set[str] = set()
    for c in cells:
        if c.seed_label not in seen:
            seen.add(c.seed_label)
            picked.append(c.cell_id)
    return picked[:N_EXAMPLE_CELLS]


def chart_panel_c(*, arm: str) -> None:
    ex = _example_cells()
    fig, axes = plt.subplots(2, len(ex), figsize=(4.2 * len(ex), 6.4), sharex=True, squeeze=False)
    for j, cid in enumerate(ex):
        wt = load_trace(key=f"delta100|{cid}")
        rd = load_trace(key=f"verify|{arm}|{cid}")
        for tr, col, lab in ((wt, C_WT, "WT-like"), (rd, C_RD1, "rd1-like")):
            t = tr["t_ms"] - CLAMP_HOLD_PRE_MS
            pre = (tr["t_ms"] >= CLAMP_HOLD_PRE_MS - 10) & (tr["t_ms"] < CLAMP_HOLD_PRE_MS)
            ax = axes[0, j]
            ax.plot(t, tr["i_mem_na"] - tr["i_mem_na"][pre].mean(), color=col, lw=1.2, label=lab)
            na = tr["ch_soma_na"] + tr["ch_ais_na"]
            axes[1, j].plot(t, na - na[pre].mean(), color=col, lw=1.2, label=lab)
        axes[0, j].set_title(cid, fontsize=9)
        axes[1, j].set_xlim(-10, 100)
        axes[1, j].set_xlabel("time from voltage step onset (ms)")
        for i in range(2):
            _clean(axes[i, j])
    axes[0, 0].set_ylabel("total membrane current (nA)\nbaseline-subtracted, outward +")
    axes[1, 0].set_ylabel("soma+AIS Na channel current (nA)\n(first 100 ms)")
    axes[0, 0].legend(frameon=False)
    fig.suptitle(
        "Panel C replication: +100 mV somatic voltage step (-65 to +35 mV), WT-like vs rd1-like",
        y=0.995,
    )
    fig.tight_layout()
    _save(fig=fig, name="panel_c_clamp_traces.png")


def chart_calibration_grid(*, arm: str) -> None:
    grid = pd.read_csv(with_arm_suffix(path=CLAMP_GRID_CSV, arm=arm))
    fits = json.loads(with_arm_suffix(path=FITTED_SCALINGS_JSON, arm=arm).read_text("utf-8"))
    ex = _example_cells()
    fig, axes = plt.subplots(2, len(ex) + 1, figsize=(4.0 * (len(ex) + 1), 7.0), squeeze=False)
    panels: list[tuple[str, str | None]] = [(c, c) for c in ex] + [("median over cells", None)]
    for j, (title, cid) in enumerate(panels):
        for i, (col, target, label) in enumerate(
            (
                ("sustained_ratio", TARGET_SUSTAINED_RATIO, "sustained current ratio"),
                ("transient_ratio", TARGET_TRANSIENT_RATIO, "Na transient ratio"),
            )
        ):
            sub = grid if cid is None else grid[grid.cell_id == cid]
            piv = sub.pivot_table(index="s_k", columns="s_na", values=col, aggfunc="median")
            ax = axes[i, j]
            im = ax.imshow(
                piv.values,
                origin="lower",
                aspect="auto",
                cmap="viridis",
                extent=(-0.5, len(S_NA_GRID) - 0.5, -0.5, len(S_K_GRID) - 0.5),
            )
            ax.set_xticks(range(len(S_NA_GRID)), [f"{v:.2f}" for v in S_NA_GRID], fontsize=7)
            ax.set_yticks(range(len(S_K_GRID)), [f"{v:.1f}" for v in S_K_GRID], fontsize=7)
            for yi in range(piv.shape[0]):
                for xi in range(piv.shape[1]):
                    ax.text(
                        xi,
                        yi,
                        f"{piv.values[yi, xi]:.2f}",
                        ha="center",
                        va="center",
                        fontsize=6,
                        color="white",
                    )
            f = fits["cells"][cid] if cid is not None else None
            pts = (
                [(f["s_na_fit"], f["s_k_fit"])]
                if f is not None
                else [(v["s_na_fit"], v["s_k_fit"]) for v in fits["cells"].values()]
            )
            for sn, sk in pts:
                x = np.interp(sn, S_NA_GRID, range(len(S_NA_GRID)))
                y = np.interp(sk, S_K_GRID, range(len(S_K_GRID)))
                ax.plot(x, y, marker="*", color="red", ms=9, mec="white", mew=0.5)
            ax.set_title(f"{title}\n{label} (target {target})", fontsize=8)
            ax.set_xlabel("s_Na (soma + AIS)", fontsize=8)
            ax.set_ylabel("s_K (soma + AIS)", fontsize=8)
            fig.colorbar(im, ax=ax, fraction=0.046)
    fig.suptitle("Part 1 clamp grid: ratios to the (1, 1) reference; red stars = fitted points")
    fig.tight_layout()
    _save(fig=fig, name="calibration_grid.png")


def chart_fitted_scalings(*, arm: str) -> None:
    fits = json.loads(with_arm_suffix(path=FITTED_SCALINGS_JSON, arm=arm).read_text("utf-8"))
    cells = list(fits["cells"].keys())
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.4))
    x = np.arange(len(cells))
    axes[0].bar(x, [fits["cells"][c]["s_na_fit"] for c in cells], color=C_RD1)
    axes[0].axhline(0.25, color=C_GREY, ls="--", lw=0.8)
    axes[0].set_ylabel("fitted s_Na")
    axes[0].set_title("fitted s_Na (grid lower edge 0.25 dashed)")
    axes[1].bar(x, [fits["cells"][c]["s_k_fit"] for c in cells], color=C_WT)
    axes[1].axhline(3.0, color=C_GREY, ls="--", lw=0.8)
    axes[1].set_ylabel("fitted s_K")
    axes[1].set_title("fitted s_K (grid upper edge 3.0 dashed)")
    ach_s = [fits["cells"][c]["achieved_sustained_ratio"] for c in cells]
    ach_t = [fits["cells"][c]["achieved_transient_ratio"] for c in cells]
    axes[2].plot(x, ach_s, "o", color=C_WT, label="sustained ratio (target 1.7)")
    axes[2].plot(x, ach_t, "s", color=C_RD1, label="Na transient ratio (target 0.25)")
    axes[2].axhline(TARGET_SUSTAINED_RATIO, color=C_WT, ls=":", lw=0.8)
    axes[2].axhline(TARGET_TRANSIENT_RATIO, color=C_RD1, ls=":", lw=0.8)
    axes[2].set_ylabel("achieved ratio (rd1-like / WT-like)")
    axes[2].legend(frameon=False, fontsize=8)
    for ax in axes:
        ax.set_xticks(x, [c.replace("_seed", "\nseed") for c in cells], fontsize=6, rotation=0)
        _clean(ax)
    fig.tight_layout()
    _save(fig=fig, name="fitted_scalings.png")


def chart_current_clamp(*, arm: str) -> None:
    ex = _example_cells()
    fig, axes = plt.subplots(2, len(ex), figsize=(4.4 * len(ex), 6.0), sharex=True, squeeze=False)
    for j, cid in enumerate(ex):
        for i, (amp, row_title) in enumerate(((60, "+60 pA, 500 ms step"), (0, "rest (0 pA)"))):
            ax = axes[i, j]
            for cond, col, lab in (("wt_like", C_WT, "WT-like"), ("rd1_like", C_RD1, "rd1-like")):
                key = f"cc|{arm}|{cid}|{cond}|{amp}"
                if trace_exists(key=key):
                    tr = load_trace(key=key)
                    ax.plot(tr["t_ms"], tr["v_mv"], color=col, lw=0.8, label=lab)
            if amp == 60:
                ax.axvspan(100, 600, color="#dfe9f3", alpha=0.5, zorder=0)
            ax.set_title(f"{cid}: {row_title}", fontsize=8)
            _clean(ax)
            ax.set_ylabel("soma Vm (mV)")
        axes[1, j].set_xlabel("time (ms; step 100-600 ms)")
    axes[0, 0].legend(frameon=False, fontsize=8)
    fig.suptitle("Panel B test (out of sample): +60 pA current step, WT-like vs rd1-like")
    fig.tight_layout()
    _save(fig=fig, name="current_clamp_traces.png")


def chart_fi(*, arm: str) -> None:
    df = pd.read_csv(with_arm_suffix(path=FI_CURVES_CSV, arm=arm))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    for cond, col, lab in (("wt_like", C_WT, "WT-like"), ("rd1_like", C_RD1, "rd1-like")):
        sub = df[df.condition == cond]
        g = sub.groupby("amp_pa").rate_hz.agg(["mean", "std"]).reset_index()
        for ax in axes:
            ax.errorbar(
                g.amp_pa + 1.0,
                g["mean"],
                yerr=g["std"],
                color=col,
                marker="o",
                ms=4,
                capsize=2,
                label=lab,
            )
            for cid in sub.cell_id.unique():
                s2 = sub[sub.cell_id == cid]
                ax.plot(s2.amp_pa + 1.0, s2.rate_hz, color=col, lw=0.5, alpha=0.35)
    axes[0].set_xscale("log")
    axes[0].set_xlabel("step amplitude + 1 (pA, log; 0 pA at left)")
    axes[1].set_xlabel("step amplitude (pA)")
    axes[1].set_xlim(-10, 850)
    for ax in axes:
        ax.set_ylabel("mean rate during 500 ms step (Hz)")
        ax.axvline(60, color=C_GREY, ls=":", lw=0.8)
        _clean(ax)
    axes[0].legend(frameon=False)
    axes[0].set_title("f-I curve, all amplitudes (mean +/- SD over cells; thin = cells)")
    axes[1].set_title("linear x axis, pre-declared amplitudes")
    fig.tight_layout()
    _save(fig=fig, name="fi_curves.png")


def chart_spontaneous(*, arm: str) -> None:
    summary = pd.read_csv(with_arm_suffix(path=SPONTANEOUS_SUMMARY_CSV, arm=arm))
    tuning = pd.read_csv(with_arm_suffix(path=BIAS_TUNING_CSV, arm=arm))
    chosen = json.loads(with_arm_suffix(path=CHOSEN_BIAS_JSON, arm=arm).read_text("utf-8"))
    ex = load_reference_cells()[:2]
    ch = chosen["selection"]["chosen"]
    fig = plt.figure(figsize=(14, 8.5))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1.2])
    from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
        SPONT_NOISE_SEEDS,
    )

    for j, c in enumerate(ex):
        for k, (tag, title) in enumerate((("nobias", "no bias"), ("chosen", "chosen bias"))):
            ax = fig.add_subplot(gs[k, j])
            for cond, col, lab in (("wt_like", C_WT, "WT-like"), ("rd1_like", C_RD1, "rd1-like")):
                if tag == "nobias":
                    key = f"spont|{arm}|nobias|{c.cell_id}|{cond}|none"
                else:
                    key = (
                        f"spont|{arm}|chosen|{c.cell_id}|{cond}|"
                        f"{ch['i_bias_pa']:.0f}_{ch['sigma_noise_pa']:.0f}_{SPONT_NOISE_SEEDS[0]}"
                    )
                if trace_exists(key=key):
                    tr = load_trace(key=key)
                    ax.plot(tr["t_ms"], tr["v_mv"], color=col, lw=0.5, label=lab)
            ax.set_title(
                f"{c.cell_id}: {title}"
                + (
                    f" ({ch['i_bias_pa']:.0f} pA DC, {ch['sigma_noise_pa']:.0f} pA noise)"
                    if tag == "chosen"
                    else ""
                ),
                fontsize=8,
            )
            ax.set_ylabel("Vm (mV)")
            _clean(ax)
            if k == 0 and j == 0:
                ax.legend(frameon=False, fontsize=7, loc="upper right")
        fig.axes[-1].set_xlabel("time (ms)")
    ax = fig.add_subplot(gs[2, :])
    for cond, col, lab in (("wt_like", C_WT, "WT-like"), ("rd1_like", C_RD1, "rd1-like")):
        sub = tuning[(tuning.condition == cond) & (tuning.sigma_noise_pa == ch["sigma_noise_pa"])]
        g = sub.groupby("i_bias_pa").rate_hz.agg(["mean", "std"]).reset_index()
        ax.errorbar(
            g.i_bias_pa + 1.0,
            g["mean"],
            yerr=g["std"],
            color=col,
            marker="o",
            ms=4,
            capsize=2,
            label=f"{lab} (tuning cells, noise {ch['sigma_noise_pa']:.0f} pA)",
        )
    ax.set_xscale("log")
    ax.axhline(7.0, color=C_GREY, ls="--", lw=0.8)
    ax.set_xlabel("DC bias + 1 (pA, log)")
    ax.set_ylabel("spontaneous rate (Hz)")
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Rate versus tonic bias (dashed: 7 Hz target)")
    _clean(ax)
    _ = summary
    fig.tight_layout()
    _save(fig=fig, name="spontaneous_traces.png")


def chart_dsi_by_condition(*, arm: str) -> None:
    df = pd.read_csv(with_arm_suffix(path=DSI_RESULTS_CSV, arm=arm))
    conds = [
        c
        for c in ("wt_like", "rd1_like", "wt_like_with_bias", "rd1_like_with_bias")
        if c in set(df.condition)
    ]
    labels = {
        "wt_like": "WT-like",
        "rd1_like": "rd1-like",
        "wt_like_with_bias": "WT-like\n+bias",
        "rd1_like_with_bias": "rd1-like\n+bias",
    }
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    for ax, (field, ylab) in zip(
        axes,
        (
            ("dsi_signed", "signed DSI (PD-ND)/(PD+ND)"),
            ("pd_rate_hz", "PD rate (Hz)"),
            ("nd_rate_hz", "ND rate (Hz)"),
        ),
        strict=True,
    ):
        for cid in df.cell_id.unique():
            sub = df[df.cell_id == cid].set_index("condition")
            ys = [sub.loc[c, field] if c in sub.index else np.nan for c in conds]
            ax.plot(range(len(conds)), ys, "-o", color=C_GREY, alpha=0.5, lw=0.8, ms=3)
        for xi, c in enumerate(conds):
            v = df[df.condition == c][field].dropna()
            if len(v) > 0:
                ax.plot(
                    [xi - 0.2, xi + 0.2],
                    [v.median(), v.median()],
                    color=C_RD1 if "rd1" in c else C_WT,
                    lw=3,
                )
            n_und = int(df[df.condition == c][field].isna().sum())
            if n_und > 0:
                ax.text(
                    xi,
                    ax.get_ylim()[0],
                    f"n undefined={n_und}",
                    ha="center",
                    va="bottom",
                    fontsize=7,
                    color="red",
                )
        ax.set_xticks(range(len(conds)), [labels[c] for c in conds], fontsize=8)
        ax.set_ylabel(ylab)
        _clean(ax)
    axes[0].set_title("signed DSI (undefined = fewer than 3 PD spikes; not plotted)")
    axes[1].set_title("PD rate (thick bar = median)")
    axes[2].set_title("ND rate")
    fig.tight_layout()
    _save(fig=fig, name="dsi_by_condition.png")


def chart_polar(*, arm: str) -> None:
    df = pd.read_csv(with_arm_suffix(path=DSI_RESULTS_CSV, arm=arm))
    ex = _example_cells()
    dir_cols = [c for c in df.columns if c.startswith("mean_spikes_dir_")]
    angles = sorted(int(c.rsplit("_", 1)[1]) for c in dir_cols)
    fig, axes = plt.subplots(
        1, len(ex), figsize=(4.4 * len(ex), 4.4), subplot_kw={"projection": "polar"}
    )
    for ax, cid in zip(np.atleast_1d(axes), ex, strict=True):
        for cond, col, lab in (("wt_like", C_WT, "WT-like"), ("rd1_like", C_RD1, "rd1-like")):
            row = df[(df.cell_id == cid) & (df.condition == cond)]
            if len(row) == 0:
                continue
            r = [float(row[f"mean_spikes_dir_{a}"].iloc[0]) for a in angles]
            th = np.deg2rad(angles + [angles[0]])
            ax.plot(th, r + [r[0]], color=col, marker="o", ms=3, label=lab)
        ax.set_title(cid, fontsize=8, pad=14)
    np.atleast_1d(axes)[0].legend(frameon=False, loc="upper right", bbox_to_anchor=(1.3, 1.15))
    fig.suptitle("Mean spikes per 1.4 s trial by bar direction (3 seeds)")
    fig.tight_layout()
    _save(fig=fig, name="polar_tuning.png")


def chart_dsi_heatmap(*, arm: str) -> None:
    df = pd.read_csv(with_arm_suffix(path=DSI_HEATMAP_CSV, arm=arm))
    fits = json.loads(with_arm_suffix(path=FITTED_SCALINGS_JSON, arm=arm).read_text("utf-8"))
    cells = df.cell_id.unique()
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
    specs: list[tuple[str, str, str]] = [
        ("dsi_signed", "median signed DSI (defined cells only)", "viridis"),
        ("pd_rate_hz", "median PD rate (Hz)", "magma"),
        ("n_def", f"number of cells with defined DSI (of {len(cells)})", "cividis"),
    ]
    d2 = df.copy()
    d2["n_def"] = d2.dsi_signed.notna().astype(float)
    for ax, (col, title, cmap) in zip(axes, specs, strict=True):
        arr = np.full((len(S_K_GRID), len(S_NA_GRID)), np.nan)
        for yi, sk in enumerate(S_K_GRID):
            for xi, sn in enumerate(S_NA_GRID):
                g = d2[(np.isclose(d2.s_k, sk)) & (np.isclose(d2.s_na, sn))][col]
                if col == "n_def":
                    arr[yi, xi] = float(g.sum())
                elif g.notna().any():
                    arr[yi, xi] = float(g.median())
        piv = pd.DataFrame(arr)
        im = ax.imshow(np.ma.masked_invalid(piv.values), origin="lower", aspect="auto", cmap=cmap)
        ax.set_xticks(range(len(S_NA_GRID)), [f"{v:.2f}" for v in S_NA_GRID], fontsize=7)
        ax.set_yticks(range(len(S_K_GRID)), [f"{v:.1f}" for v in S_K_GRID], fontsize=7)
        for yi in range(piv.shape[0]):
            for xi in range(piv.shape[1]):
                v = piv.values[yi, xi]
                if not np.isnan(v):
                    ax.text(
                        xi,
                        yi,
                        f"{v:.2f}" if col == "dsi_signed" else f"{v:.0f}",
                        ha="center",
                        va="center",
                        fontsize=6,
                        color="white",
                    )
        for cid in cells:
            f = fits["cells"].get(cid)
            if f is not None:
                ax.plot(
                    np.interp(f["s_na_fit"], S_NA_GRID, range(len(S_NA_GRID))),
                    np.interp(f["s_k_fit"], S_K_GRID, range(len(S_K_GRID))),
                    marker="*",
                    color="red",
                    ms=8,
                    mec="white",
                    mew=0.5,
                )
        ax.set_xlabel("s_Na (soma + AIS)")
        ax.set_ylabel("s_K (soma + AIS)")
        ax.set_title(title, fontsize=9)
        fig.colorbar(im, ax=ax, fraction=0.046)
    fig.suptitle("DSI versus (s_Na, s_K): red stars = per-cell fitted rd1-like scalings")
    fig.tight_layout()
    _save(fig=fig, name="dsi_heatmap.png")


def _toy_params(*, d: dict[str, Any]) -> ToyParams:
    return ToyParams(b=d["b"], r_max=d["r_max"], k=d["k"], n=d["n"], tau_ms=d["tau_ms"])


def chart_toy_model() -> None:
    toy = json.loads(TOY_PARAMS_JSON.read_text(encoding="utf-8"))
    wt, rd = _toy_params(d=toy["wt"]), _toy_params(d=toy["rd1"])
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    t = np.arange(0.0, 1000.0, 1.0)
    from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.panel_d_metrics import input_signal

    axes[0].plot(t, input_signal(t_ms=t), color=C_WT)
    axes[0].set_xlabel("time (ms)")
    axes[0].set_ylabel("input drive")
    axes[0].set_title("same input (three Gaussian pulses)")
    u = np.linspace(0, 100, 401)
    axes[1].plot(u, rate_static(u=u, params=wt), color=C_WT, label="WT-like")
    axes[1].plot(u, rate_static(u=u, params=rd), color=C_RD1, label="rd1-like")
    axes[1].set_xlabel("strength of restored retinal input")
    axes[1].set_ylabel("RGC spike output (toy units)")
    axes[1].legend(frameon=False)
    axes[1].set_title("toy input-output curves")
    tw = simulate_pulse_response(params=wt, u_ref=100.0, tstop_ms=1000.0, dt_ms=0.5)
    tr = simulate_pulse_response(params=rd, u_ref=100.0, tstop_ms=1000.0, dt_ms=0.5)
    axes[2].plot(t, input_signal(t_ms=t), color=C_GREY, lw=1, label="input")
    axes[2].plot(tw.t_ms, tw.relative, color=C_WT, label="WT-like output")
    axes[2].plot(tr.t_ms, tr.relative, color=C_RD1, label="rd1-like output")
    axes[2].set_xlabel("time (ms)")
    axes[2].set_ylabel("relative signal")
    axes[2].legend(frameon=False, fontsize=8)
    axes[2].set_title("toy responses to the pulses")
    for ax in axes:
        _clean(ax)
    fig.suptitle("Panel D toy model (Naka-Rushton plus leaky integrator), fitted to by-eye anchors")
    fig.tight_layout()
    _save(fig=fig, name="panel_d_toy_model.png")


def chart_panel_d_sweep() -> None:
    df = pd.read_csv(PANEL_D_SWEEP_CSV)
    conds = sorted(set(df.condition))
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4), sharey=True)
    for ax, suffix in zip(axes, ("", "_with_bias"), strict=True):
        for cond, col in ((f"wt_like{suffix}", C_WT), (f"rd1_like{suffix}", C_RD1)):
            if cond not in conds:
                continue
            sub = df[df.condition == cond]
            for cid in sub.cell_id.unique():
                s2 = sub[sub.cell_id == cid]
                ax.plot(s2.u, s2.rate_hz, color=col, lw=0.6, alpha=0.4)
            g = sub.groupby("u").rate_hz.mean().reset_index()
            ax.plot(g.u, g.rate_hz, color=col, marker="o", lw=2, label=cond.replace("_", " "))
        ax.set_xlabel("PD synaptic drive strength u (% of standard excitatory weight)")
        ax.set_title("no bias" if suffix == "" else "with tonic bias")
        ax.legend(frameon=False, fontsize=8)
        _clean(ax)
    axes[0].set_ylabel("mean PD-direction spike rate (Hz)")
    fig.suptitle("NEURON test of panel D prediction 1: input-output curve (3 cells, 3 seeds)")
    fig.tight_layout()
    _save(fig=fig, name="panel_d_neuron_sweep.png")


def chart_panel_d_pulses() -> None:
    z = np.load(PANEL_D_PSTH_NPZ)
    t = z["t_ms"]
    pulses = pd.read_csv(PANEL_D_PULSES_CSV)
    cells = list(pulses.cell_id.unique())
    from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.panel_d_metrics import input_signal

    fig, axes = plt.subplots(2, len(cells), figsize=(5 * len(cells), 7), squeeze=False)
    for j, cid in enumerate(cells):
        for i, suffix in enumerate(("", "_with_bias")):
            ax = axes[i, j]
            ax2 = ax.twinx()
            ax2.plot(t, input_signal(t_ms=t), color=C_GREY, lw=0.8, ls="--")
            ax2.set_yticks([])
            for cond, col in ((f"wt_like{suffix}", C_WT), (f"rd1_like{suffix}", C_RD1)):
                key = f"{cid}|{cond}"
                if key in z.files:
                    ax.plot(t, z[key], color=col, label=cond.replace("_", " "))
            ax.set_title(f"{cid}{' (with bias)' if suffix else ''}", fontsize=8)
            ax.set_ylabel("PSTH (Hz), smoothed")
            ax.set_xlabel("time (ms); dashed = input")
            ax.legend(frameon=False, fontsize=7)
            _clean(ax)
    fig.suptitle("NEURON test of panel D predictions 2-3: three-pulse response (10 repetitions)")
    fig.tight_layout()
    _save(fig=fig, name="panel_d_neuron_pulses.png")


def chart_arm_comparison() -> None:
    dec = json.loads(ARM_DECISION_JSON.read_text(encoding="utf-8"))
    if not dec.get("triggered", False):
        return
    base = json.loads(FITTED_SCALINGS_JSON.read_text(encoding="utf-8"))
    dend = json.loads(
        with_arm_suffix(path=FITTED_SCALINGS_JSON, arm="soma_ais_dendrite").read_text("utf-8")
    )
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.4))
    cells = list(base["cells"].keys())
    x = np.arange(len(cells))
    w = 0.38
    for ax, key, lab in (
        (axes[0], "s_na_fit", "fitted s_Na"),
        (axes[1], "s_k_fit", "fitted s_K"),
        (axes[2], "achieved_sustained_ratio", "achieved sustained ratio"),
    ):
        ax.bar(x - w / 2, [base["cells"][c][key] for c in cells], w, color=C_RD1, label="soma+AIS")
        ax.bar(
            x + w / 2,
            [dend["cells"][c][key] for c in cells],
            w,
            color=C_WT,
            label="soma+AIS+dendrite",
        )
        ax.set_ylabel(lab)
        ax.set_xticks(x, [c.replace("_seed", "\nseed") for c in cells], fontsize=6)
        _clean(ax)
    axes[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    _save(fig=fig, name="arm_comparison.png")


CHARTS: dict[str, Any] = {}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--arm", default="soma_ais")
    args = ap.parse_args()
    arm: str = args.arm
    todo: dict[str, Any] = {
        "panel_c": lambda: chart_panel_c(arm=arm),
        "calibration": lambda: chart_calibration_grid(arm=arm),
        "fitted": lambda: chart_fitted_scalings(arm=arm),
        "cc": lambda: chart_current_clamp(arm=arm),
        "fi": lambda: chart_fi(arm=arm),
        "spont": lambda: chart_spontaneous(arm=arm),
        "dsi": lambda: chart_dsi_by_condition(arm=arm),
        "polar": lambda: chart_polar(arm=arm),
        "heat": lambda: chart_dsi_heatmap(arm=arm),
        "toy": chart_toy_model,
        "sweep": chart_panel_d_sweep,
        "pulses": chart_panel_d_pulses,
        "arms": chart_arm_comparison,
    }
    names = list(todo.keys()) if args.only is None else args.only
    for n in names:
        todo[n]()
    _ = (Path, PANEL_D_VERDICTS_JSON)


if __name__ == "__main__":
    main()
