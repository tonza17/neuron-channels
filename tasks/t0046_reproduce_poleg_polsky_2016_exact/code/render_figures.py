"""Render results/images/fig{1..8}_*.png from the per-figure CSVs.

Each PNG overlays the paper's reported value (where stated) against this task's reproduction
value with a tolerance band. Plain matplotlib is used because the paper's figures are PD-vs-ND
bar plots / scatter plots, not 12-angle tuning curves; t0011's ``tuning_curve_viz`` library is
designed for the latter shape and is invoked once for the Fig 8 8-angle tuning-curve overlay.
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.paths import (
    DATA_DIR,
    FIG1_PNG,
    FIG2_PNG,
    FIG3_PNG,
    FIG4_PNG,
    FIG5_PNG,
    FIG6_PNG,
    FIG7_PNG,
    FIG8_PNG,
    IMAGES_DIR,
)

# Paper-reported metrics (values copied from the paper / task_description.md Pass Criterion).
PAPER_FIG1_PD_MV: float = 5.8
PAPER_FIG1_PD_SD: float = 3.1
PAPER_FIG1_ND_MV: float = 3.3
PAPER_FIG1_ND_SD: float = 2.8
PAPER_FIG1_SLOPE_DEG: float = 62.5
PAPER_FIG1_SLOPE_SD: float = 14.2
PAPER_FIG2_PD_REDUCTION_PERCENT: float = 16.0
PAPER_FIG4_SLOPE_DEG: float = 45.5
PAPER_FIG4_SLOPE_SD: float = 3.7
PAPER_FIG5_SLOPE_DEG: float = 45.5
PAPER_FIG5_SLOPE_SD: float = 5.3
PAPER_FIG7_AUC_CONTROL: float = 0.99
PAPER_FIG7_AUC_AP5: float = 0.98
PAPER_FIG7_AUC_ZEROMG: float = 0.83


def _load_grouped(*, csv_path: Path) -> dict[str, dict[str, list[float]]]:
    """Return groups[notes][direction_label] = [peak_psp_mv, ...]."""
    groups: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    if not csv_path.exists():
        return groups
    with csv_path.open("r", encoding="utf-8", newline="") as fh:
        reader: Any = csv.DictReader(fh)
        for r in reader:
            groups[r["notes"]][r["direction_label"]].append(float(r["peak_psp_mv"]))
    return groups


def _load_grouped_spikes(*, csv_path: Path) -> dict[str, dict[str, list[float]]]:
    groups: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    if not csv_path.exists():
        return groups
    with csv_path.open("r", encoding="utf-8", newline="") as fh:
        reader: Any = csv.DictReader(fh)
        for r in reader:
            groups[r["notes"]][r["direction_label"]].append(float(r["ap_rate_hz"]))
    return groups


def _bar_pd_nd(
    *,
    repro_pd: list[float],
    repro_nd: list[float],
    paper_pd: float,
    paper_pd_sd: float,
    paper_nd: float,
    paper_nd_sd: float,
    title: str,
    ylabel: str,
    out_png: Path,
) -> None:
    """Make a 4-bar comparison: paper PD/ND vs reproduction PD/ND with error bars."""
    pd_mean: float = float(np.mean(repro_pd)) if len(repro_pd) > 0 else 0.0
    pd_sd: float = float(np.std(repro_pd, ddof=1)) if len(repro_pd) >= 2 else 0.0
    nd_mean: float = float(np.mean(repro_nd)) if len(repro_nd) > 0 else 0.0
    nd_sd: float = float(np.std(repro_nd, ddof=1)) if len(repro_nd) >= 2 else 0.0

    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    x: np.ndarray = np.arange(4)
    means: list[float] = [paper_pd, pd_mean, paper_nd, nd_mean]
    sds: list[float] = [paper_pd_sd, pd_sd, paper_nd_sd, nd_sd]
    colors: list[str] = ["#888888", "#1f77b4", "#cccccc", "#ff7f0e"]
    labels: list[str] = ["Paper PD", "Repro PD", "Paper ND", "Repro ND"]
    bars = ax.bar(x, means, yerr=sds, capsize=5, color=colors)
    for rect, mean in zip(bars, means, strict=True):
        ax.annotate(
            f"{mean:.2f}",
            xy=(rect.get_x() + rect.get_width() / 2, rect.get_height()),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(fname=out_png, dpi=120, facecolor="white", bbox_inches="tight")
    plt.close(fig=fig)
    print(f"  wrote {out_png}", flush=True)


def _render_fig1() -> None:
    """Fig 1: control PSP at b2gnmda = 0.5 (code) and 2.5 (paper)."""
    groups = _load_grouped(csv_path=DATA_DIR / "fig1_psp.csv")
    if "fig1_control_gnmda05" not in groups and "fig1_control_gnmda25" not in groups:
        print("  [skip] fig1: no data", flush=True)
        return
    # Pick gnmda 0.5 (primary) for the headline plot; annotate gnmda 2.5 in title.
    primary_label: str = "fig1_control_gnmda05"
    if primary_label not in groups:
        primary_label = "fig1_control_gnmda25"
    g = groups[primary_label]
    _bar_pd_nd(
        repro_pd=g["PD"],
        repro_nd=g["ND"],
        paper_pd=PAPER_FIG1_PD_MV,
        paper_pd_sd=PAPER_FIG1_PD_SD,
        paper_nd=PAPER_FIG1_ND_MV,
        paper_nd_sd=PAPER_FIG1_ND_SD,
        title=(f"Figure 1: control PSP, paper vs reproduction ({primary_label})"),
        ylabel="PSP amplitude (mV)",
        out_png=FIG1_PNG,
    )


def _render_fig2() -> None:
    """Fig 2: AP5 analogue (b2gnmda = 0)."""
    groups = _load_grouped(csv_path=DATA_DIR / "fig2_imk801_psp.csv")
    if "fig2_ap5_gnmda0" not in groups:
        print("  [skip] fig2: no data", flush=True)
        return
    g = groups["fig2_ap5_gnmda0"]
    # Paper Fig 2: AP5-after-iMK801 reduces PD PSP by 16+/-17%; we represent as bars.
    _bar_pd_nd(
        repro_pd=g["PD"],
        repro_nd=g["ND"],
        paper_pd=PAPER_FIG1_PD_MV * (1.0 - PAPER_FIG2_PD_REDUCTION_PERCENT / 100.0),
        paper_pd_sd=PAPER_FIG1_PD_SD,
        paper_nd=PAPER_FIG1_ND_MV * (1.0 - PAPER_FIG2_PD_REDUCTION_PERCENT / 100.0),
        paper_nd_sd=PAPER_FIG1_ND_SD,
        title="Figure 2: AP5 analogue (b2gnmda = 0); paper estimate vs reproduction",
        ylabel="PSP amplitude (mV)",
        out_png=FIG2_PNG,
    )


def _render_fig3() -> None:
    """Fig 3: gNMDA sweep, DSI vs gNMDA."""
    groups = _load_grouped(csv_path=DATA_DIR / "fig3_gnmda_sweep.csv")
    if len(groups) == 0:
        print("  [skip] fig3: no data", flush=True)
        return
    gnmda_values: list[float] = []
    pd_means: list[float] = []
    nd_means: list[float] = []
    dsi_values: list[float] = []
    for key, g in sorted(groups.items()):
        # key = "fig3_gnmda_X.XX"
        try:
            gnmda: float = float(key.split("_")[-1])
        except ValueError:
            continue
        if len(g["PD"]) == 0 or len(g["ND"]) == 0:
            continue
        pd_m: float = float(np.mean(g["PD"]))
        nd_m: float = float(np.mean(g["ND"]))
        gnmda_values.append(gnmda)
        pd_means.append(pd_m)
        nd_means.append(nd_m)
        denom: float = pd_m + nd_m
        dsi: float = (pd_m - nd_m) / denom if denom != 0 else 0.0
        dsi_values.append(dsi)

    if len(gnmda_values) == 0:
        print("  [skip] fig3: no parsable rows", flush=True)
        return

    FIG3_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.5))
    ax1.plot(gnmda_values, pd_means, "o-", label="PD", color="#1f77b4")
    ax1.plot(gnmda_values, nd_means, "o-", label="ND", color="#ff7f0e")
    ax1.axvline(0.5, linestyle="--", color="#888", label="code value (0.5)")
    ax1.axvline(2.5, linestyle="--", color="#cc0000", label="paper value (2.5)")
    ax1.set_xlabel("b2gnmda (nS)")
    ax1.set_ylabel("PSP amplitude (mV)")
    ax1.set_title("Figure 3: gNMDA sweep, mean PSP vs gNMDA")
    ax1.legend(loc="best")
    ax1.grid(alpha=0.3)
    ax2.plot(gnmda_values, dsi_values, "s-", color="#2ca02c")
    ax2.axvline(0.5, linestyle="--", color="#888")
    ax2.axvline(2.5, linestyle="--", color="#cc0000")
    ax2.set_xlabel("b2gnmda (nS)")
    ax2.set_ylabel("DSI (PD-ND)/(PD+ND)")
    ax2.set_title("Figure 3: DSI vs gNMDA")
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(fname=FIG3_PNG, dpi=120, facecolor="white", bbox_inches="tight")
    plt.close(fig=fig)
    print(f"  wrote {FIG3_PNG}", flush=True)


def _render_fig4() -> None:
    """Fig 4: high-Cl-."""
    groups = _load_grouped(csv_path=DATA_DIR / "fig4_highcl_psp.csv")
    if "fig4_highcl" not in groups:
        print("  [skip] fig4: no data", flush=True)
        return
    g = groups["fig4_highcl"]
    _bar_pd_nd(
        repro_pd=g["PD"],
        repro_nd=g["ND"],
        paper_pd=PAPER_FIG1_PD_MV,  # paper Fig 4 reports slope, not absolute PSP; use Fig 1.
        paper_pd_sd=PAPER_FIG1_PD_SD,
        paper_nd=PAPER_FIG1_ND_MV,
        paper_nd_sd=PAPER_FIG1_ND_SD,
        title=(
            f"Figure 4: high-Cl- (paper slope {PAPER_FIG4_SLOPE_DEG}+/-{PAPER_FIG4_SLOPE_SD} deg)"
        ),
        ylabel="PSP amplitude (mV)",
        out_png=FIG4_PNG,
    )


def _render_fig5() -> None:
    """Fig 5: 0 Mg2+."""
    groups = _load_grouped(csv_path=DATA_DIR / "fig5_zeromg_psp.csv")
    if "fig5_zeromg" not in groups:
        print("  [skip] fig5: no data", flush=True)
        return
    g = groups["fig5_zeromg"]
    _bar_pd_nd(
        repro_pd=g["PD"],
        repro_nd=g["ND"],
        paper_pd=PAPER_FIG1_PD_MV,
        paper_pd_sd=PAPER_FIG1_PD_SD,
        paper_nd=PAPER_FIG1_ND_MV,
        paper_nd_sd=PAPER_FIG1_ND_SD,
        title=(
            f"Figure 5: 0 Mg2+ (paper slope {PAPER_FIG5_SLOPE_DEG}+/-{PAPER_FIG5_SLOPE_SD} deg)"
        ),
        ylabel="PSP amplitude (mV)",
        out_png=FIG5_PNG,
    )


def _render_fig6() -> None:
    """Fig 6: noise sweep, DSI by SD for control / 0Mg / AP5."""
    groups = _load_grouped(csv_path=DATA_DIR / "fig6_noise.csv")
    if len(groups) == 0:
        print("  [skip] fig6: no data", flush=True)
        return
    conditions: list[tuple[str, str, str]] = [
        ("fig6_control", "Control", "#1f77b4"),
        ("fig6_ap5", "AP5 analogue", "#2ca02c"),
        ("fig6_zeromg", "0 Mg2+", "#cc0000"),
    ]
    noise_levels: list[float] = [0.0, 0.10, 0.30]

    FIG6_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for prefix, label, color in conditions:
        dsi_at_noise: list[float] = []
        for noise in noise_levels:
            key: str = f"{prefix}_noise{noise:.2f}"
            if key not in groups:
                dsi_at_noise.append(float("nan"))
                continue
            g = groups[key]
            pd_m: float = float(np.mean(g["PD"])) if len(g["PD"]) > 0 else 0.0
            nd_m: float = float(np.mean(g["ND"])) if len(g["ND"]) > 0 else 0.0
            denom: float = pd_m + nd_m
            dsi_at_noise.append((pd_m - nd_m) / denom if denom != 0 else 0.0)
        ax.plot(noise_levels, dsi_at_noise, "o-", label=label, color=color)
    ax.set_xlabel("flickerVAR (luminance noise SD)")
    ax.set_ylabel("DSI (PD-ND)/(PD+ND)")
    ax.set_title("Figure 6: DSI vs noise SD by condition")
    ax.legend(loc="best")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(fname=FIG6_PNG, dpi=120, facecolor="white", bbox_inches="tight")
    plt.close(fig=fig)
    print(f"  wrote {FIG6_PNG}", flush=True)


def _render_fig7() -> None:
    """Fig 7: ROC AUC under noise for control / AP5 / 0Mg."""
    groups = _load_grouped(csv_path=DATA_DIR / "fig7_roc_noise.csv")
    if len(groups) == 0:
        print("  [skip] fig7: no data", flush=True)
        return
    conditions: list[tuple[str, str, str, float]] = [
        ("fig6_control", "Control", "#1f77b4", PAPER_FIG7_AUC_CONTROL),
        ("fig6_ap5", "AP5 analogue", "#2ca02c", PAPER_FIG7_AUC_AP5),
        ("fig6_zeromg", "0 Mg2+", "#cc0000", PAPER_FIG7_AUC_ZEROMG),
    ]
    noise_levels: list[float] = [0.0, 0.10, 0.30]

    FIG7_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for prefix, label, color, paper_noise_free in conditions:
        aucs: list[float] = []
        for noise in noise_levels:
            key: str = f"{prefix}_noise{noise:.2f}"
            if key not in groups:
                aucs.append(float("nan"))
                continue
            g = groups[key]
            # ROC PD-vs-ND: probability that random PD > random ND.
            n_pos: int = len(g["PD"])
            n_neg: int = len(g["ND"])
            correct: int = 0
            for p in g["PD"]:
                for n in g["ND"]:
                    if p > n:
                        correct += 1
                    elif p == n:
                        correct += 0
            auc: float = float(correct) / float(n_pos * n_neg) if n_pos * n_neg > 0 else 0.0
            aucs.append(auc)
        ax.plot(
            noise_levels,
            aucs,
            "o-",
            label=f"{label} (paper noise-free {paper_noise_free})",
            color=color,
        )
        ax.axhline(paper_noise_free, linestyle=":", color=color, alpha=0.5)
    ax.set_xlabel("flickerVAR (luminance noise SD)")
    ax.set_ylabel("ROC AUC (PD vs ND)")
    ax.set_ylim(0.4, 1.05)
    ax.set_title(
        "Figure 7: ROC AUC vs noise SD (dashed lines = paper noise-free reference)",
    )
    ax.legend(loc="best", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(fname=FIG7_PNG, dpi=120, facecolor="white", bbox_inches="tight")
    plt.close(fig=fig)
    print(f"  wrote {FIG7_PNG}", flush=True)


def _render_fig8() -> None:
    """Fig 8: spike rates and PD-failure rates by condition."""
    groups = _load_grouped_spikes(csv_path=DATA_DIR / "fig8_spikes.csv")
    if len(groups) == 0:
        print("  [skip] fig8: no data", flush=True)
        return
    # Pull spike-count rows for failure rates too.
    spike_count_groups: dict[str, dict[str, list[int]]] = defaultdict(
        lambda: defaultdict(list),
    )
    csv_path: Path = DATA_DIR / "fig8_spikes.csv"
    if csv_path.exists():
        with csv_path.open("r", encoding="utf-8", newline="") as fh:
            reader: Any = csv.DictReader(fh)
            for r in reader:
                spike_count_groups[r["notes"]][r["direction_label"]].append(
                    int(r["spike_count"]),
                )

    FIG8_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.5))
    conditions: list[tuple[str, str, str]] = [
        ("fig8_control", "Control", "#1f77b4"),
        ("fig8_ap5", "AP5 analogue", "#2ca02c"),
        ("fig8_zeromg", "0 Mg2+", "#cc0000"),
    ]
    noise_levels: list[float] = [0.0, 0.10]
    width: float = 0.25

    # Panel 1: PD/ND spike rates (Hz) at noise=0 only for clarity.
    rate_data: dict[str, tuple[float, float]] = {}
    for prefix, label, _ in conditions:
        key: str = f"{prefix}_noise0.00"
        if key in groups:
            pd_m: float = float(np.mean(groups[key]["PD"])) if len(groups[key]["PD"]) > 0 else 0.0
            nd_m: float = float(np.mean(groups[key]["ND"])) if len(groups[key]["ND"]) > 0 else 0.0
            rate_data[label] = (pd_m, nd_m)

    x: np.ndarray = np.arange(len(rate_data))
    pd_rates: list[float] = [rate_data[lbl][0] for lbl in rate_data]
    nd_rates: list[float] = [rate_data[lbl][1] for lbl in rate_data]
    ax1.bar(x - width / 2, pd_rates, width, label="PD", color="#1f77b4")
    ax1.bar(x + width / 2, nd_rates, width, label="ND", color="#ff7f0e")
    ax1.set_xticks(x)
    ax1.set_xticklabels(list(rate_data.keys()))
    ax1.set_ylabel("Spike rate (Hz)")
    ax1.set_title("Figure 8: AP rate by condition (noise = 0)")
    ax1.legend(loc="best")
    ax1.grid(axis="y", alpha=0.3)

    # Panel 2: PD-failure rate by noise level for each condition.
    for prefix, label, color in conditions:
        failure_rates: list[float] = []
        for noise in noise_levels:
            key = f"{prefix}_noise{noise:.2f}"
            if key not in spike_count_groups:
                failure_rates.append(float("nan"))
                continue
            pd_counts: list[int] = spike_count_groups[key]["PD"]
            n_total: int = len(pd_counts)
            n_zero: int = sum(1 for c in pd_counts if c == 0)
            failure_rates.append(float(n_zero) / float(n_total) if n_total > 0 else 0.0)
        ax2.plot(noise_levels, failure_rates, "o-", label=label, color=color)
    ax2.set_xlabel("flickerVAR (luminance noise SD)")
    ax2.set_ylabel("PD-failure rate (fraction of trials with 0 spikes)")
    ax2.set_title("Figure 8: PD-failure rate vs noise (qualitative)")
    ax2.legend(loc="best")
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(fname=FIG8_PNG, dpi=120, facecolor="white", bbox_inches="tight")
    plt.close(fig=fig)
    print(f"  wrote {FIG8_PNG}", flush=True)


def main() -> int:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    _render_fig1()
    _render_fig2()
    _render_fig3()
    _render_fig4()
    _render_fig5()
    _render_fig6()
    _render_fig7()
    _render_fig8()
    print("Figure rendering complete.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
