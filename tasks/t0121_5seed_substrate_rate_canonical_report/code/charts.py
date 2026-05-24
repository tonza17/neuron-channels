"""Three required charts for the canonical 5-seed substrate-rate report.

All charts call ``matplotlib.use("Agg")`` before importing pyplot to support
headless plotting on CI. The visual key (``SEED_COLORS`` / ``SEED_MARKERS`` /
``SEED_LABELS``) is imported from ``seed_metadata`` so the canonical report
stays visually consistent with the upstream per-seed reports.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

from pathlib import Path  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from tasks.t0121_5seed_substrate_rate_canonical_report.code.constants import (  # noqa: E402
    DRUCKMANN_2007_RATE_PCT,
    DSI_THRESHOLD,
    HAY_2011_RATE_PCT,
    LEGIT_DSI_CEILING,
    PD_RATE_THRESHOLD_HZ,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.paths import (  # noqa: E402
    CHART_ACCEPTANCE_BAR,
    CHART_DSI_PD_SCATTER,
    CHART_HV_OVERLAY,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.per_seed import (  # noqa: E402
    PerSeedSummary,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.seed_metadata import (  # noqa: E402
    ALL_SEED_KEYS,
    POOL_RESTART_CADENCE,
    SEED_COLORS,
    SEED_LABELS,
    SEED_MARKERS,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.stats import (  # noqa: E402
    SubstrateStats,
)

_MOHACSI_BAND_LO: int = 20
_MOHACSI_BAND_HI: int = 60


def chart_per_seed_acceptance_bar(
    *,
    summaries: dict[str, PerSeedSummary],
    stats: SubstrateStats,
) -> Path:
    """Per-seed bar chart with literature reference lines and both 95% CIs.

    Six bars: one per seed plus a 5-seed-mean bar with two error bars (the
    normal-approx 95% CI in black and the bootstrap 95% CI in slate-grey).
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    bar_labels: list[str] = []
    bar_values: list[float] = []
    bar_colors: list[str] = []
    for key in ALL_SEED_KEYS:
        bar_labels.append(SEED_LABELS[key])
        bar_values.append(summaries[key].acceptance_rate_pct)
        bar_colors.append(SEED_COLORS[key])
    bar_labels.append("5-seed mean")
    bar_values.append(stats.mean_pct)
    bar_colors.append("black")

    xs: np.ndarray = np.arange(len(bar_labels))
    bars = ax.bar(xs, bar_values, color=bar_colors, alpha=0.75, edgecolor="black")

    # Normal-approx 95% CI error bar (black).
    mean_x: float = float(xs[-1])
    normal_lo_off: float = max(0.0, stats.mean_pct - stats.normal_approx_ci_lo_pct)
    normal_hi_off: float = stats.normal_approx_ci_hi_pct - stats.mean_pct
    ax.errorbar(
        x=mean_x - 0.10,
        y=stats.mean_pct,
        yerr=np.asarray([[normal_lo_off], [normal_hi_off]]),
        fmt="none",
        ecolor="black",
        capsize=6,
        lw=1.8,
        label=(
            f"Normal-approx 95% CI = "
            f"({stats.normal_approx_ci_lo_pct:.2f}, "
            f"{stats.normal_approx_ci_hi_pct:.2f})"
        ),
    )

    # Bootstrap 95% CI error bar (slate-grey).
    boot_lo_off: float = max(0.0, stats.mean_pct - stats.bootstrap_ci_lo_pct)
    boot_hi_off: float = stats.bootstrap_ci_hi_pct - stats.mean_pct
    ax.errorbar(
        x=mean_x + 0.10,
        y=stats.mean_pct,
        yerr=np.asarray([[boot_lo_off], [boot_hi_off]]),
        fmt="none",
        ecolor="slategrey",
        capsize=6,
        lw=1.8,
        label=(
            f"Bootstrap 95% CI = ({stats.bootstrap_ci_lo_pct:.2f}, {stats.bootstrap_ci_hi_pct:.2f})"
        ),
    )

    ax.axhline(
        HAY_2011_RATE_PCT,
        color="crimson",
        ls="--",
        lw=1.6,
        label=f"Hay 2011 envelope ({HAY_2011_RATE_PCT:.2f}%)",
    )
    ax.axhline(
        DRUCKMANN_2007_RATE_PCT,
        color="darkorange",
        ls=":",
        lw=1.6,
        label=f"Druckmann 2007 ({DRUCKMANN_2007_RATE_PCT:.2f}%)",
    )

    label_offset: float = max(bar_values) * 0.01
    for b in bars:
        h: float = float(b.get_height())
        ax.text(
            b.get_x() + b.get_width() / 2,
            h + label_offset,
            f"{h:.2f}%",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    ax.set_xticks(xs)
    ax.set_xticklabels(bar_labels, rotation=20, ha="right")
    ax.set_ylabel("LEGIT joint-pass acceptance rate (%)")
    ax.set_title(
        "5-seed LEGIT joint-pass acceptance rate vs Hay 2011 and Druckmann 2007",
    )
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, ls=":", lw=0.5, alpha=0.5, axis="y")
    fig.tight_layout()
    CHART_ACCEPTANCE_BAR.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHART_ACCEPTANCE_BAR, dpi=120)
    plt.close(fig)
    return CHART_ACCEPTANCE_BAR


def chart_hv_trajectory_overlay(
    *,
    hv_traces: dict[str, list[dict[str, object]]],
) -> Path:
    """5-seed HV-trajectory overlay with pool-restart and convergence-band annotations."""
    fig, ax = plt.subplots(figsize=(11, 6.5))

    max_gen_seen: int = 0
    for key in ALL_SEED_KEYS:
        traj = hv_traces[key]
        gens: list[int] = [int(h["generation"]) for h in traj]
        hvs: list[float] = [float(h["hypervolume"]) for h in traj]
        cadence: int = POOL_RESTART_CADENCE[key]
        final_hv: float = hvs[-1] if len(hvs) > 0 else float("nan")
        ax.plot(
            gens,
            hvs,
            label=(
                f"{SEED_LABELS[key]} (cadence {cadence}, {len(gens)} gens, final HV={final_hv:.2f})"
            ),
            color=SEED_COLORS[key],
            marker=SEED_MARKERS[key],
            ms=3.0,
            lw=1.4,
        )
        last_gen: int = gens[-1] if len(gens) > 0 else 0
        if last_gen > max_gen_seen:
            max_gen_seen = last_gen
        # Faint dotted vertical lines at pool-restart generations.
        for g in range(cadence, last_gen + 1, cadence):
            ax.axvline(
                g,
                color=SEED_COLORS[key],
                ls=":",
                lw=0.4,
                alpha=0.30,
            )
        # X marker at the operator-stop / auto-stop point.
        ax.plot(
            last_gen,
            final_hv,
            marker="x",
            ms=10,
            mew=2.0,
            color=SEED_COLORS[key],
        )

    # Mohacsi 2024 convergence band shaded between gens 20 and 60.
    ax.axvspan(
        _MOHACSI_BAND_LO,
        _MOHACSI_BAND_HI,
        color="lightyellow",
        alpha=0.40,
        label=f"Mohacsi 2024 convergence band ({_MOHACSI_BAND_LO}-{_MOHACSI_BAND_HI} gens)",
    )

    ax.set_yscale("log")
    ax.set_xlabel("generation")
    ax.set_ylabel("hypervolume (log scale)")
    ax.set_title(
        "5-seed HV trajectory overlay (t0106 / t0112 / t0113 / t0114 / t0115) "
        "with pool-restart events",
    )
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(True, ls=":", lw=0.5, alpha=0.5)
    fig.tight_layout()
    CHART_HV_OVERLAY.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHART_HV_OVERLAY, dpi=120)
    plt.close(fig)
    return CHART_HV_OVERLAY


def chart_dsi_pd_scatter(*, pooled_df: pd.DataFrame) -> Path:
    """Pooled LEGIT joint-pass DSI-vs-PD scatter, coloured by seed."""
    fig, ax = plt.subplots(figsize=(10, 6.5))

    for key in ALL_SEED_KEYS:
        subset = pooled_df[pooled_df["seed"] == key]
        ax.scatter(
            subset["pd_rate_hz"],
            subset["dsi"],
            s=35,
            alpha=0.7,
            color=SEED_COLORS[key],
            marker=SEED_MARKERS[key],
            label=f"{SEED_LABELS[key]} (n={len(subset)})",
            edgecolors="black",
            linewidths=0.25,
        )

    ax.axhline(
        DSI_THRESHOLD,
        color="black",
        ls="--",
        lw=1.0,
        alpha=0.7,
        label=f"DSI threshold ({DSI_THRESHOLD:.1f})",
    )
    ax.axvline(
        PD_RATE_THRESHOLD_HZ,
        color="black",
        ls="--",
        lw=1.0,
        alpha=0.7,
        label=f"PD-rate threshold ({PD_RATE_THRESHOLD_HZ:.0f} Hz)",
    )
    ax.axhline(
        LEGIT_DSI_CEILING,
        color="grey",
        ls=":",
        lw=1.0,
        alpha=0.7,
        label=f"LEGIT ceiling ({LEGIT_DSI_CEILING})",
    )

    ax.set_xlabel("PD-rate (Hz)")
    ax.set_ylabel("ratio DSI")
    ax.set_title("Pooled LEGIT joint-pass cells (DSI vs PD-rate), 5-seed canonical batch")
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(True, ls=":", lw=0.5, alpha=0.5)
    fig.tight_layout()
    CHART_DSI_PD_SCATTER.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHART_DSI_PD_SCATTER, dpi=120)
    plt.close(fig)
    return CHART_DSI_PD_SCATTER
