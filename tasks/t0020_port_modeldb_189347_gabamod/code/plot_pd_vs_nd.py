"""Plot the PD vs ND mean firing-rate bar chart with per-trial scatter overlay.

Reads ``data/tuning_curves.csv`` and writes
``results/images/pd_vs_nd_firing_rate.png`` at 200 DPI, 5x4 inches.

Shows:
  * Two bars: mean PD firing rate and mean ND firing rate.
  * Error bars: per-condition standard deviation (population ``ddof=0``).
  * Per-trial scatter overlay: jittered points for every trial.

This chart is the implementation deliverable for the image half of
REQ-7. The narrative comparison table and the markdown embed in
``results_detailed.md`` are written by the orchestrator's results step
and are out of scope here.
"""

from __future__ import annotations

import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from pandas import DataFrame  # noqa: E402

from tasks.t0020_port_modeldb_189347_gabamod.code.constants import (  # noqa: E402
    CONDITION_COLUMN,
    FIRING_RATE_COLUMN,
    TRIAL_SEED_COLUMN,
    Condition,
)
from tasks.t0020_port_modeldb_189347_gabamod.code.paths import (  # noqa: E402
    IMAGES_DIR,
    PD_VS_ND_PNG,
    TUNING_CURVES_CSV,
)

TUNING_CURVES_DTYPE: dict[str, object] = {
    CONDITION_COLUMN: pd.StringDtype(),
    TRIAL_SEED_COLUMN: pd.UInt32Dtype(),
    FIRING_RATE_COLUMN: "float64",
}

BAR_COLORS: dict[str, str] = {
    Condition.PD.value: "#1f77b4",
    Condition.ND.value: "#d62728",
}

FIGURE_WIDTH_IN: float = 5.0
FIGURE_HEIGHT_IN: float = 4.0
FIGURE_DPI: int = 200
SCATTER_JITTER: float = 0.12
SCATTER_RNG_SEED: int = 42


def _load_tuning_curves() -> DataFrame:
    df = pd.read_csv(
        filepath_or_buffer=TUNING_CURVES_CSV,
        dtype=TUNING_CURVES_DTYPE,
    )
    assert CONDITION_COLUMN in df.columns, (
        f"missing column '{CONDITION_COLUMN}' in {TUNING_CURVES_CSV}"
    )
    assert FIRING_RATE_COLUMN in df.columns, (
        f"missing column '{FIRING_RATE_COLUMN}' in {TUNING_CURVES_CSV}"
    )
    return df


def _plot(*, df: DataFrame) -> None:
    labels = [Condition.PD.value, Condition.ND.value]
    x_positions = np.arange(len(labels))
    means: list[float] = []
    stds: list[float] = []
    per_trial: dict[str, list[float]] = {}
    for label in labels:
        rates = df.loc[
            df[CONDITION_COLUMN] == label,
            FIRING_RATE_COLUMN,
        ].to_numpy(dtype="float64")
        assert len(rates) > 0, f"no trials found for condition {label}"
        means.append(float(np.mean(rates)))
        stds.append(float(np.std(rates, ddof=0)))
        per_trial[label] = rates.tolist()

    fig, ax = plt.subplots(
        figsize=(FIGURE_WIDTH_IN, FIGURE_HEIGHT_IN),
        dpi=FIGURE_DPI,
    )
    ax.bar(
        x=x_positions,
        height=means,
        yerr=stds,
        capsize=6,
        color=[BAR_COLORS[label] for label in labels],
        alpha=0.7,
        edgecolor="black",
        linewidth=1.0,
        label=None,
    )

    rng = np.random.default_rng(seed=SCATTER_RNG_SEED)
    for idx, label in enumerate(labels):
        rates = per_trial[label]
        jitter = rng.uniform(
            low=-SCATTER_JITTER,
            high=SCATTER_JITTER,
            size=len(rates),
        )
        ax.scatter(
            x=x_positions[idx] + jitter,
            y=rates,
            s=22,
            color="black",
            alpha=0.6,
            zorder=3,
        )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Firing rate (Hz)")
    ax.set_xlabel("Condition")
    ax.set_title("DSGC PD vs ND firing rate (gabaMOD swap)")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    fig.tight_layout()
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(PD_VS_ND_PNG)
    plt.close(fig=fig)


def main() -> int:
    if not TUNING_CURVES_CSV.exists():
        print(
            f"ERROR: tuning curve CSV missing at {TUNING_CURVES_CSV}",
            flush=True,
        )
        return 1

    print(f"Plotting {TUNING_CURVES_CSV}...", flush=True)
    df = _load_tuning_curves()
    _plot(df=df)
    print(f"Wrote {PD_VS_ND_PNG}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
