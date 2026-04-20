"""Generate result charts for t0008 results_detailed.md.

Produces three PNGs under results/images/:

* polar_tuning_curve_vs_envelope.png - Reproduced mean tuning curve on polar axes with
  shaded envelope band (target curve + peak target 40-80 Hz, null <10 Hz).
* envelope_metrics_bars.png - Bar chart of reproduced DSI / peak / null / HWHM vs
  envelope target bands, coloured by pass/fail.
* per_angle_firing_rate.png - Cartesian plot of reproduced per-trial firing rates with
  mean ± std and the t0004 target curve overlay (same axes for direct comparison).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tasks.t0008_port_modeldb_189347.code.paths import (
    IMAGES_DIR,
    REPO_ROOT,
    SCORE_REPORT_JSON,
    TUNING_CURVE_MODELDB_CSV,
)

TARGET_CURVE_CSV: Path = (
    REPO_ROOT
    / "tasks"
    / "t0004_generate_target_tuning_curve"
    / "assets"
    / "dataset"
    / "target-tuning-curve"
    / "files"
    / "curve_mean.csv"
)

# Envelope targets from the task description (project goal).
ENV_DSI_LO: float = 0.70
ENV_DSI_HI: float = 0.85
ENV_PEAK_LO_HZ: float = 40.0
ENV_PEAK_HI_HZ: float = 80.0
ENV_NULL_MAX_HZ: float = 10.0
ENV_HWHM_LO_DEG: float = 60.0
ENV_HWHM_HI_DEG: float = 90.0


@dataclass(frozen=True, slots=True)
class CandidateMetrics:
    dsi: float
    peak_hz: float
    null_hz: float
    hwhm_deg: float


@dataclass(frozen=True, slots=True)
class AxisSpec:
    name: str
    reproduced: float
    target_lo: float
    target_hi: float
    unit: str
    passed: bool


def _load_score_report() -> tuple[CandidateMetrics, dict[str, bool]]:
    payload: dict[str, object] = json.loads(SCORE_REPORT_JSON.read_text(encoding="utf-8"))
    candidate: dict[str, float] = payload["candidate_metrics"]  # type: ignore[assignment]
    per_target_pass: dict[str, bool] = payload["per_target_pass"]  # type: ignore[assignment]
    metrics: CandidateMetrics = CandidateMetrics(
        dsi=float(candidate["dsi"]),
        peak_hz=float(candidate["peak_hz"]),
        null_hz=float(candidate["null_hz"]),
        hwhm_deg=float(candidate["hwhm_deg"]),
    )
    return metrics, per_target_pass


def _compute_per_angle_stats(df: pd.DataFrame) -> pd.DataFrame:
    grouped: pd.DataFrame = df.groupby("angle_deg")["firing_rate_hz"].agg(["mean", "std"])
    return grouped.reset_index()


def _plot_polar(
    *,
    stats: pd.DataFrame,
    target: pd.DataFrame,
    out_path: Path,
) -> None:
    fig: plt.Figure = plt.figure(figsize=(7.5, 7.5))
    ax: plt.PolarAxes = fig.add_subplot(111, projection="polar")

    angles_rad: np.ndarray = np.deg2rad(stats["angle_deg"].to_numpy())
    means: np.ndarray = stats["mean"].to_numpy()
    stds: np.ndarray = stats["std"].to_numpy()
    target_rad: np.ndarray = np.deg2rad(target["angle_deg"].to_numpy())
    target_rates: np.ndarray = target["mean_rate_hz"].to_numpy()

    # Close the loop for a smooth polygon.
    angles_closed: np.ndarray = np.concatenate([angles_rad, angles_rad[:1]])
    means_closed: np.ndarray = np.concatenate([means, means[:1]])
    stds_closed: np.ndarray = np.concatenate([stds, stds[:1]])
    target_rad_closed: np.ndarray = np.concatenate([target_rad, target_rad[:1]])
    target_rates_closed: np.ndarray = np.concatenate([target_rates, target_rates[:1]])

    # Shaded 40-80 Hz peak envelope band (full circle at that radius range).
    theta_fill: np.ndarray = np.linspace(0, 2 * np.pi, 361)
    ax.fill_between(
        theta_fill,
        np.full_like(theta_fill, ENV_PEAK_LO_HZ),
        np.full_like(theta_fill, ENV_PEAK_HI_HZ),
        color="tab:green",
        alpha=0.15,
        label=f"Envelope peak target ({int(ENV_PEAK_LO_HZ)}-{int(ENV_PEAK_HI_HZ)} Hz)",
    )
    # Null region: 0 to NULL_MAX.
    ax.fill_between(
        theta_fill,
        np.zeros_like(theta_fill),
        np.full_like(theta_fill, ENV_NULL_MAX_HZ),
        color="tab:red",
        alpha=0.08,
        label=f"Envelope null ceiling (<{int(ENV_NULL_MAX_HZ)} Hz)",
    )

    # Target curve (t0004 canonical).
    ax.plot(
        target_rad_closed,
        target_rates_closed,
        color="tab:blue",
        linewidth=2.0,
        linestyle="--",
        label="Target curve (t0004 mean)",
    )

    # Reproduced mean with std band.
    ax.plot(
        angles_closed,
        means_closed,
        color="tab:orange",
        linewidth=2.5,
        marker="o",
        markersize=6,
        label="Reproduced (mean of 20 trials)",
    )
    ax.fill_between(
        angles_closed,
        means_closed - stds_closed,
        means_closed + stds_closed,
        color="tab:orange",
        alpha=0.25,
        label="Reproduced mean +/- std",
    )

    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)  # counter-clockwise
    ax.set_rlabel_position(135)
    ax.set_ylim(0, max(float(ENV_PEAK_HI_HZ) + 5.0, float(means.max() + stds.max() + 5.0)))
    ax.set_title(
        "Polar tuning curve: reproduced vs target + envelope band",
        pad=25,
        fontsize=12,
    )
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.10), fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def _plot_envelope_bars(
    *,
    metrics: CandidateMetrics,
    per_target_pass: dict[str, bool],
    out_path: Path,
) -> None:
    specs: list[AxisSpec] = [
        AxisSpec(
            name="DSI",
            reproduced=metrics.dsi,
            target_lo=ENV_DSI_LO,
            target_hi=ENV_DSI_HI,
            unit="",
            passed=per_target_pass["dsi"],
        ),
        AxisSpec(
            name="Peak",
            reproduced=metrics.peak_hz,
            target_lo=ENV_PEAK_LO_HZ,
            target_hi=ENV_PEAK_HI_HZ,
            unit="Hz",
            passed=per_target_pass["peak"],
        ),
        AxisSpec(
            name="Null",
            reproduced=metrics.null_hz,
            target_lo=0.0,
            target_hi=ENV_NULL_MAX_HZ,
            unit="Hz",
            passed=per_target_pass["null"],
        ),
        AxisSpec(
            name="HWHM",
            reproduced=metrics.hwhm_deg,
            target_lo=ENV_HWHM_LO_DEG,
            target_hi=ENV_HWHM_HI_DEG,
            unit="deg",
            passed=per_target_pass["hwhm"],
        ),
    ]

    fig, axes = plt.subplots(1, 4, figsize=(15, 4.5))
    for ax, spec in zip(axes, specs, strict=True):
        bar_color: str = "tab:green" if spec.passed else "tab:red"
        ax.axhspan(
            spec.target_lo,
            spec.target_hi,
            color="tab:green",
            alpha=0.15,
            label="Envelope band",
        )
        ax.bar(
            [spec.name],
            [spec.reproduced],
            color=bar_color,
            width=0.55,
            edgecolor="black",
        )
        ax.text(
            0,
            spec.reproduced + (spec.target_hi - spec.target_lo) * 0.05 + 0.01,
            f"{spec.reproduced:.3g}{spec.unit}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )
        ax.set_title(
            f"{spec.name} ({spec.unit if spec.unit else '-'})\n"
            f"{'PASS' if spec.passed else 'FAIL'}: "
            f"target {spec.target_lo:g}-{spec.target_hi:g}",
            fontsize=10,
        )
        top: float = max(spec.target_hi * 1.3, spec.reproduced * 1.2)
        ax.set_ylim(0, top)
        ax.set_xticks([])
        ax.grid(axis="y", alpha=0.3)
        ax.legend(loc="upper right", fontsize=8)

    fig.suptitle(
        "Envelope axes: reproduced value vs target band",
        fontsize=13,
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def _plot_per_angle(
    *,
    df: pd.DataFrame,
    stats: pd.DataFrame,
    target: pd.DataFrame,
    out_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 5.5))

    # Envelope bands.
    ax.axhspan(
        ENV_PEAK_LO_HZ,
        ENV_PEAK_HI_HZ,
        color="tab:green",
        alpha=0.12,
        label=f"Peak envelope ({int(ENV_PEAK_LO_HZ)}-{int(ENV_PEAK_HI_HZ)} Hz)",
    )
    ax.axhspan(
        0.0,
        ENV_NULL_MAX_HZ,
        color="tab:red",
        alpha=0.08,
        label=f"Null envelope (<{int(ENV_NULL_MAX_HZ)} Hz)",
    )

    # Per-trial scatter (jittered for visibility).
    rng: np.random.Generator = np.random.default_rng(seed=2026)
    jitter: np.ndarray = rng.uniform(-3.0, 3.0, size=len(df))
    ax.scatter(
        df["angle_deg"].to_numpy() + jitter,
        df["firing_rate_hz"].to_numpy(),
        s=12,
        color="tab:orange",
        alpha=0.35,
        label="Per-trial rate (n=20 per angle)",
    )

    # Reproduced mean +/- std.
    ax.errorbar(
        stats["angle_deg"].to_numpy(),
        stats["mean"].to_numpy(),
        yerr=stats["std"].to_numpy(),
        color="tab:orange",
        linewidth=2.0,
        capsize=4,
        marker="o",
        markersize=7,
        label="Reproduced mean +/- std",
    )

    # Target curve.
    ax.plot(
        target["angle_deg"].to_numpy(),
        target["mean_rate_hz"].to_numpy(),
        color="tab:blue",
        linewidth=2.0,
        linestyle="--",
        marker="s",
        markersize=6,
        label="Target curve (t0004 mean)",
    )

    ax.set_xlabel("Bar angle (deg)")
    ax.set_ylabel("Firing rate (Hz)")
    ax.set_title(
        "Reproduced vs target tuning curve (per-angle, 20 trials each)",
        fontsize=12,
    )
    ax.set_xticks(list(range(0, 361, 30)))
    ax.set_xlim(-15, 345)
    ax.set_ylim(0, max(float(ENV_PEAK_HI_HZ) + 5.0, float(df["firing_rate_hz"].max()) + 2.0))
    ax.grid(alpha=0.3)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=TUNING_CURVE_MODELDB_CSV)
    assert list(df.columns) == ["angle_deg", "trial_seed", "firing_rate_hz"], (
        "tuning curve columns match canonical schema"
    )
    assert len(df) == 240, "tuning curve has 240 rows (12 angles x 20 trials)"

    target: pd.DataFrame = pd.read_csv(filepath_or_buffer=TARGET_CURVE_CSV)
    assert list(target.columns) == ["angle_deg", "mean_rate_hz"], (
        "target curve columns match canonical schema"
    )

    metrics, per_target_pass = _load_score_report()
    stats: pd.DataFrame = _compute_per_angle_stats(df=df)

    _plot_polar(
        stats=stats,
        target=target,
        out_path=IMAGES_DIR / "polar_tuning_curve_vs_envelope.png",
    )
    _plot_envelope_bars(
        metrics=metrics,
        per_target_pass=per_target_pass,
        out_path=IMAGES_DIR / "envelope_metrics_bars.png",
    )
    _plot_per_angle(
        df=df,
        stats=stats,
        target=target,
        out_path=IMAGES_DIR / "per_angle_firing_rate.png",
    )

    print(f"Wrote charts to {IMAGES_DIR}")


if __name__ == "__main__":
    main()
