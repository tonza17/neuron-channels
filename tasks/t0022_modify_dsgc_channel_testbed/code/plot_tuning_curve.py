"""Plot the t0022 per-dendrite tuning curve as a polar + Cartesian pair.

Reads ``data/tuning_curves/curve_modeldb_189347_dendritic.csv`` and emits
``results/images/tuning_curve_dendritic.png``. Also overlays the t0004
target envelope if available for quick visual comparison.
"""

from __future__ import annotations

import csv
import statistics
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0022_modify_dsgc_channel_testbed.code.paths import (
    IMAGES_DIR,
    TUNING_CURVE_DENDRITIC_CSV,
    TUNING_CURVE_PNG,
)


def _load_per_angle_means() -> tuple[list[float], list[float], list[float]]:
    """Return (angles_deg, mean_hz, std_hz) sorted by angle."""
    rows: list[tuple[int, int, float]] = []
    with TUNING_CURVE_DENDRITIC_CSV.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            rows.append(
                (
                    int(r["angle_deg"]),
                    int(r["trial_seed"]),
                    float(r["firing_rate_hz"]),
                ),
            )
    angles: list[int] = sorted({r[0] for r in rows})
    means: list[float] = []
    stds: list[float] = []
    for a in angles:
        vals: list[float] = [r[2] for r in rows if r[0] == a]
        means.append(statistics.mean(vals))
        stds.append(statistics.stdev(vals) if len(vals) > 1 else 0.0)
    return ([float(a) for a in angles], means, stds)


def main() -> int:
    if not TUNING_CURVE_DENDRITIC_CSV.exists():
        print(f"ERROR: {TUNING_CURVE_DENDRITIC_CSV} not found")
        return 1

    angles_deg, means, stds = _load_per_angle_means()
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    fig, (ax_polar, ax_cart) = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(12, 5),
        subplot_kw={"polar": False},
    )
    # Replace the left subplot with a polar one.
    fig.delaxes(ax_polar)
    ax_polar = fig.add_subplot(1, 2, 1, projection="polar")

    theta = np.radians(angles_deg + [angles_deg[0]])
    r = means + [means[0]]
    ax_polar.plot(theta, r, marker="o", linewidth=2, color="#1f77b4")
    ax_polar.fill(theta, r, alpha=0.2, color="#1f77b4")
    ax_polar.set_theta_zero_location("E")
    ax_polar.set_theta_direction(1)
    ax_polar.set_title(
        "t0022 per-dendrite E-I tuning curve (polar)",
        fontsize=11,
    )

    ax_cart.errorbar(
        angles_deg,
        means,
        yerr=stds,
        marker="o",
        color="#1f77b4",
        linewidth=2,
        capsize=3,
    )
    ax_cart.set_xlabel("Bar direction (deg)")
    ax_cart.set_ylabel("Firing rate (Hz)")
    ax_cart.set_title("t0022 per-dendrite E-I tuning curve (Cartesian)")
    ax_cart.grid(True, alpha=0.4)
    ax_cart.set_xticks([0, 60, 120, 180, 240, 300, 360])
    ax_cart.axhline(y=10.0, linestyle="--", color="gray", alpha=0.5, label="peak gate (10 Hz)")
    ax_cart.legend(loc="upper right")

    fig.tight_layout()
    fig.savefig(TUNING_CURVE_PNG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {TUNING_CURVE_PNG}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
