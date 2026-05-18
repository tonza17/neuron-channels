"""Render polar tuning curves for the 10 t0107 cells.

Loads `results/data/per_cell_polar_eval.json`, draws a 2x5 grid of polar
subplots (one per cell), and writes `results/images/polar_tuning_curves_top10.png`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from tasks.t0107_t0106_polar_8dir_recheck.code.paths import (  # noqa: E402
    IMAGES_DIR,
    RESULTS_DATA_DIR,
    ensure_directories,
)

PER_CELL_POLAR_JSON: Path = RESULTS_DATA_DIR / "per_cell_polar_eval.json"
POLAR_PNG: Path = IMAGES_DIR / "polar_tuning_curves_top10.png"

N_ROWS: int = 2
N_COLS: int = 5
TITLE_FONTSIZE: int = 8
TICK_FONTSIZE: int = 7
FIG_DPI: int = 110
FIG_INCHES: tuple[float, float] = (14.0, 6.5)


@dataclass(frozen=True, slots=True)
class CellPolar:
    t0106_rank: int
    t0106_dsi: float
    t0106_pd_hz: float
    angles_deg: tuple[float, ...]
    rates_hz: tuple[float, ...]
    dsi_vsum: float


def _load_cells(*, path: Path) -> list[CellPolar]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records: list[dict[str, object]] = payload["evaluations"]  # type: ignore[index]
    out: list[CellPolar] = []
    for r in records:
        out.append(
            CellPolar(
                t0106_rank=int(r["t0106_rank"]),  # type: ignore[arg-type]
                t0106_dsi=float(r["t0106_dsi"]),  # type: ignore[arg-type]
                t0106_pd_hz=float(r["t0106_pd_hz"]),  # type: ignore[arg-type]
                angles_deg=tuple(
                    float(x)
                    for x in r["angles_deg"]  # type: ignore[arg-type]
                ),
                rates_hz=tuple(
                    float(x)
                    for x in r["per_direction_rates_hz"]  # type: ignore[arg-type]
                ),
                dsi_vsum=float(r["t0107_dsi_8dir_vsum"]),  # type: ignore[arg-type]
            )
        )
    return out


def _plot_one_cell(
    *,
    ax: plt.Axes,
    cell: CellPolar,
) -> None:
    if len(cell.angles_deg) == 0:
        ax.set_title(
            f"#{cell.t0106_rank} (no rates)\n"
            f"t0106: DSI={cell.t0106_dsi:.2f}, PD={cell.t0106_pd_hz:.1f}Hz",
            fontsize=TITLE_FONTSIZE,
        )
        return
    # Convert angles to radians.
    angles_rad: list[float] = [float(np.deg2rad(a)) for a in cell.angles_deg]
    rates: list[float] = list(cell.rates_hz)
    # Close the polygon by appending first point at the end.
    closed_angles: list[float] = [*angles_rad, angles_rad[0]]
    closed_rates: list[float] = [*rates, rates[0]]
    ax.plot(closed_angles, closed_rates, marker="o", color="#1f77b4", linewidth=1.6)
    ax.fill(closed_angles, closed_rates, alpha=0.25, color="#1f77b4")
    # Soma marker at origin.
    ax.plot([0.0], [0.0], marker="s", color="black", markersize=4)
    ax.set_theta_zero_location("E")  # 0 deg = east (PD).
    ax.set_theta_direction(1)  # CCW positive.
    ax.set_xticks(np.deg2rad([0, 45, 90, 135, 180, 225, 270, 315]).tolist())
    ax.set_xticklabels(
        ["0", "45", "90", "135", "180", "225", "270", "315"],
        fontsize=TICK_FONTSIZE,
    )
    ax.tick_params(axis="y", labelsize=TICK_FONTSIZE)
    ax.set_title(
        f"#{cell.t0106_rank}\n"
        f"t0106: DSI={cell.t0106_dsi:.2f}, PD={cell.t0106_pd_hz:.1f}Hz\n"
        f"t0107: vsum-DSI={cell.dsi_vsum:.3f}",
        fontsize=TITLE_FONTSIZE,
    )


def main() -> None:
    ensure_directories()
    src_path = (
        PER_CELL_POLAR_JSON
        if PER_CELL_POLAR_JSON.exists()
        else RESULTS_DATA_DIR / "per_cell_polar_eval.checkpoint.json"
    )
    cells = _load_cells(path=src_path)
    if len(cells) != N_ROWS * N_COLS:
        # Partial result mode (intervention path).
        print(
            f"WARNING: only {len(cells)} cells available "
            f"(expected {N_ROWS * N_COLS}); rendering partial grid"
        )
    fig, axes = plt.subplots(
        N_ROWS,
        N_COLS,
        figsize=FIG_INCHES,
        dpi=FIG_DPI,
        subplot_kw={"projection": "polar"},
    )
    cells_sorted = sorted(cells, key=lambda c: c.t0106_rank)
    for i, cell in enumerate(cells_sorted):
        if i >= N_ROWS * N_COLS:
            break
        ax = axes[i // N_COLS, i % N_COLS]
        _plot_one_cell(ax=ax, cell=cell)
    # Hide axes with no data.
    for j in range(len(cells_sorted), N_ROWS * N_COLS):
        ax = axes[j // N_COLS, j % N_COLS]
        ax.set_axis_off()
    fig.suptitle(
        f"t0107 polar tuning curves (8 directions, 3 noise seeds) — "
        f"{len(cells)}/{N_ROWS * N_COLS} cells rendered",
        fontsize=11,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
    fig.savefig(POLAR_PNG, dpi=FIG_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {POLAR_PNG}")


if __name__ == "__main__":
    main()
