"""Build the four required charts for t0129's results step.

REQ-8 from ``plan/plan.md``. Inputs:

* ``results/cell_params.jsonl`` -- 5,760 evaluated cells (Phase A + 59 NSGA-II
  generations) with signed DSI, ATP per spike, PD/ND firing rates, silence flag.
* ``results/data/pareto_front_seed3517.json`` -- final 9-cell Pareto front.
* ``tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/pareto_front_seed8929.json``
  -- t0126 Pareto front under vector-sum DSI for the overlay chart.

Outputs (all written to ``tasks/t0129_*/results/images/``):

1. ``pareto_front_dsi_signed_vs_atp.png`` -- 9-cell Pareto front with full DSI
   range visible.
2. ``dsi_signed_distribution.png`` -- 40-bin histogram of signed DSI over all
   5,760 evaluated cells, with the 264 silence-failed cells separated.
3. ``pd_vs_nd_rate_scatter.png`` -- PD vs ND firing rate scatter coloured by
   signed DSI for all 5,496 viable cells, with the Pareto front highlighted.
4. ``pareto_t0126_vs_t0129_overlay.png`` -- overlay of t0126's vector-sum
   Pareto front and t0129's signed-DSI Pareto front in DSI vs ATP space.

All charts are embedded into ``results_detailed.md`` per the spec.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.figure import Figure
from numpy.typing import NDArray

from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.paths import (
    CELL_PARAMS_JSONL,
    IMAGES_DIR,
    REPO_ROOT,
    RESULTS_DATA_DIR,
    pareto_front_json,
)

# Output PNG paths.
PARETO_FRONT_PNG: Path = IMAGES_DIR / "pareto_front_dsi_signed_vs_atp.png"
DSI_DISTRIBUTION_PNG: Path = IMAGES_DIR / "dsi_signed_distribution.png"
PD_VS_ND_SCATTER_PNG: Path = IMAGES_DIR / "pd_vs_nd_rate_scatter.png"
T0126_VS_T0129_OVERLAY_PNG: Path = IMAGES_DIR / "pareto_t0126_vs_t0129_overlay.png"

# Sidecar JSON for the metrics builder.
T0126_VS_T0129_SIGN_FLIP_JSON: Path = RESULTS_DATA_DIR / "t0126_vs_t0129_sign_flip_count.json"

# Read-only input from t0126 (dependency task).
T0126_PARETO_FRONT_JSON: Path = (
    REPO_ROOT
    / "tasks"
    / "t0126_bedb_dsi_atp_per_spike_nsga2_60gen"
    / "results"
    / "data"
    / "pareto_front_seed8929.json"
)

# Constants used in chart rendering.
DPI: int = 150
T0129_SEED: int = 3517
T0126_SEED: int = 8929
N_HIST_BINS: int = 40
ATP_M_DIVISOR: float = 1.0e6  # render ATP in millions of molecules per spike.


@dataclass(frozen=True, slots=True)
class CellRow:
    """One row from ``cell_params.jsonl``."""

    gen: int
    cell_idx: int
    dsi_signed: float
    atp_per_spike_molecules: float
    pd_rate_hz: float
    nd_rate_hz: float
    silence_failed: bool
    n_errors: int


@dataclass(frozen=True, slots=True)
class ParetoCell:
    """One cell from the final Pareto front JSON."""

    cell_id: int
    dsi_signed: float
    atp_per_spike_molecules: float


@dataclass(frozen=True, slots=True)
class CellParamsSummary:
    rows: list[CellRow]
    pareto_cells: list[ParetoCell]


def _load_cell_params(*, path: Path) -> list[CellRow]:
    """Load ``cell_params.jsonl`` into typed dataclass rows."""
    rows: list[CellRow] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if len(line) == 0:
                continue
            d = json.loads(line)
            rows.append(
                CellRow(
                    gen=int(d["gen"]),
                    cell_idx=int(d["cell_idx"]),
                    dsi_signed=float(d["dsi_signed"]),
                    atp_per_spike_molecules=float(d["atp_per_spike_molecules"]),
                    pd_rate_hz=float(d["pd_rate_hz"]),
                    nd_rate_hz=float(d["nd_rate_hz"]),
                    silence_failed=bool(d["silence_failed"]),
                    n_errors=int(d["n_errors"]),
                )
            )
    return rows


def _load_t0129_pareto(*, path: Path) -> list[ParetoCell]:
    """Load t0129's final Pareto front from JSON."""
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    cells: list[ParetoCell] = []
    for c in data["cells"]:
        cells.append(
            ParetoCell(
                cell_id=int(c["cell_id"]),
                dsi_signed=float(c["dsi_signed"]),
                atp_per_spike_molecules=float(c["atp_per_spike_molecules"]),
            )
        )
    return cells


def _load_t0126_pareto_vector_sum(*, path: Path) -> list[ParetoCell]:
    """Load t0126's final Pareto front under vector-sum DSI."""
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    cells: list[ParetoCell] = []
    for c in data["cells"]:
        # t0126 stored the vector-sum magnitude under ``dsi_best_legit``. For
        # the antipodal pair this is identically ``|dsi_signed|``.
        dsi_mag: float = float(c["dsi_best_legit"])
        cells.append(
            ParetoCell(
                cell_id=int(c["cell_id"]),
                dsi_signed=dsi_mag,  # treated as magnitude; sign unknown
                atp_per_spike_molecules=float(c["atp_per_spike_molecules"]),
            )
        )
    return cells


def _save_figure(*, fig: Figure, path: Path) -> None:
    """Save a matplotlib figure to disk and close it."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def build_pareto_front_chart(
    *,
    pareto_cells: list[ParetoCell],
    output_path: Path,
) -> None:
    """Chart (a): 9-cell Pareto front, DSI on x-axis from -1 to 1, ATP on y.

    Highlights cell 0 (rank-1 cheapest) and cell with the largest dsi_signed
    (rank-9 selectivity champion). x-axis is the full signed-DSI range so the
    negative tail is visible even though the t0129 Pareto front does not
    contain negative-DSI cells (silent and 0-DSI dominate the energy minimum
    corner; negative DSI is dominated in F-space by 0-DSI silent cells).
    """
    dsi: NDArray[np.float64] = np.array([c.dsi_signed for c in pareto_cells])
    atp_m: NDArray[np.float64] = np.array(
        [c.atp_per_spike_molecules / ATP_M_DIVISOR for c in pareto_cells]
    )

    rank1_idx: int = int(np.argmin(atp_m))
    rank9_idx: int = int(np.argmax(dsi))

    fig, ax = plt.subplots(figsize=(8.0, 5.5))
    ax.scatter(
        dsi,
        atp_m,
        s=110,
        c="#1f77b4",
        edgecolors="black",
        linewidths=1.0,
        zorder=3,
        label=f"t0129 Pareto cells (n={len(pareto_cells)})",
    )
    ax.axvline(
        x=0.0,
        color="grey",
        linestyle="--",
        linewidth=1.0,
        zorder=1,
        label="DSI = 0 (no selectivity)",
    )
    # Annotate rank-1 and rank-9.
    rank1 = pareto_cells[rank1_idx]
    rank9 = pareto_cells[rank9_idx]
    ax.annotate(
        f"rank-1 (min ATP)\ncell {rank1.cell_id}\n"
        f"DSI={rank1.dsi_signed:.3f}, ATP={atp_m[rank1_idx]:.2f} M/spike",
        xy=(rank1.dsi_signed, atp_m[rank1_idx]),
        xytext=(0.05, 0.18),
        textcoords="axes fraction",
        fontsize=9,
        arrowprops={"arrowstyle": "->", "color": "black", "lw": 0.8},
    )
    ax.annotate(
        f"rank-9 (max DSI)\ncell {rank9.cell_id}\n"
        f"DSI={rank9.dsi_signed:.3f}, ATP={atp_m[rank9_idx]:.2f} M/spike",
        xy=(rank9.dsi_signed, atp_m[rank9_idx]),
        xytext=(0.55, 0.85),
        textcoords="axes fraction",
        fontsize=9,
        arrowprops={"arrowstyle": "->", "color": "black", "lw": 0.8},
    )
    ax.set_xlim(-1.05, 1.05)
    ax.set_xlabel("Signed antipodal DSI = (R_PD - R_ND) / (R_PD + R_ND)")
    ax.set_ylabel("ATP per spike (millions of molecules)")
    ax.set_title(
        f"t0129 final Pareto front (seed {T0129_SEED}, n={len(pareto_cells)} cells)\n"
        "Signed antipodal DSI vs ATP per spike"
    )
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=9)
    _save_figure(fig=fig, path=output_path)


def build_dsi_distribution_chart(
    *,
    rows: list[CellRow],
    output_path: Path,
) -> None:
    """Chart (b): histogram of dsi_signed across all 5,760 evaluated cells.

    The 264 silence-failed cells (all at dsi_signed=-1.0 by the silence
    sentinel) are rendered as a separate red bar at x=-1 so they are not
    confused with the 95 "real" viable cells in the negative tail.
    """
    silenced: list[CellRow] = [r for r in rows if r.silence_failed]
    viable: list[CellRow] = [r for r in rows if not r.silence_failed]
    dsi_viable: NDArray[np.float64] = np.array([r.dsi_signed for r in viable])

    fig, ax = plt.subplots(figsize=(9.0, 5.5))

    # Histogram of viable cells.
    bin_edges: list[float] = list(np.linspace(-1.0, 1.0, N_HIST_BINS + 1))
    counts, _, _ = ax.hist(
        dsi_viable,
        bins=bin_edges,
        color="#1f77b4",
        edgecolor="white",
        alpha=0.85,
        label=f"viable cells (n={len(viable)})",
        zorder=2,
    )

    # Separate bar for silence-failed cells (all at exactly -1.0).
    silence_bar_x: float = -1.025  # left of the histogram so it is visually separated.
    silence_bar_w: float = 0.04
    ax.bar(
        x=silence_bar_x,
        height=len(silenced),
        width=silence_bar_w,
        color="#d62728",
        edgecolor="black",
        linewidth=0.8,
        label=f"silence-failed cells (n={len(silenced)}, sentinel DSI=-1)",
        zorder=3,
    )

    # Annotate the 95 viable cells with negative DSI.
    n_viable_neg: int = int(np.sum(dsi_viable < 0.0))
    ax.text(
        0.02,
        0.85,
        (
            f"Viable cells with DSI < 0 (reversed preference,\n"
            f"invisible to vector-sum DSI): n = {n_viable_neg}\n"
            f"min DSI (viable): {float(dsi_viable.min()):.3f}\n"
            f"max DSI: {float(dsi_viable.max()):.3f}\n"
            f"mean DSI (viable): {float(dsi_viable.mean()):.3f}"
        ),
        transform=ax.transAxes,
        fontsize=9,
        bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "grey"},
        verticalalignment="top",
    )

    ax.axvline(x=0.0, color="grey", linestyle="--", linewidth=1.0, zorder=1)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(0, max(float(np.max(counts)), float(len(silenced))) * 1.10)
    ax.set_xlabel("Signed antipodal DSI = (R_PD - R_ND) / (R_PD + R_ND)")
    ax.set_ylabel("Count of evaluated cells")
    ax.set_title(
        f"t0129 signed-DSI distribution across all {len(rows)} evaluated cells "
        f"(seed {T0129_SEED}, 96 Phase A + 5,664 NSGA-II)\n"
        "Silence-failed cells (sentinel DSI=-1) shown as separate red bar"
    )
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=9)
    _save_figure(fig=fig, path=output_path)


def build_pd_vs_nd_scatter(
    *,
    rows: list[CellRow],
    pareto_cells: list[ParetoCell],
    output_path: Path,
) -> None:
    """Chart (c): PD vs ND firing rate scatter coloured by signed DSI.

    All 5,496 viable cells, diverging colormap (RdBu_r) centred at 0,
    diagonal y=x line shows the DSI=0 locus. Pareto cells highlighted with
    larger markers and a black edge.
    """
    viable: list[CellRow] = [r for r in rows if not r.silence_failed]
    pd_rate: NDArray[np.float64] = np.array([r.pd_rate_hz for r in viable])
    nd_rate: NDArray[np.float64] = np.array([r.nd_rate_hz for r in viable])
    dsi_viable: NDArray[np.float64] = np.array([r.dsi_signed for r in viable])

    # Pareto cells -- look up their pd/nd_rate from cell_params via cell_id
    # match. ``cell_id`` in pareto_front_seed3517.json is the row index in the
    # final population (gen 60), but we just reproduce the Pareto rate values
    # from the matching cell_params rows when available. Since the Pareto JSON
    # does not include pd/nd_rate (those are None), compute them by matching on
    # vector_68d to the closest cell_params row. Simpler approach: query the
    # rows where dsi_signed and atp match the Pareto values.
    pareto_pd: list[float] = []
    pareto_nd: list[float] = []
    pareto_dsi: list[float] = []
    for c in pareto_cells:
        # find a viable row with the matching dsi+atp pair
        match: CellRow | None = None
        for r in viable:
            if (
                abs(r.dsi_signed - c.dsi_signed) < 1e-9
                and abs(r.atp_per_spike_molecules - c.atp_per_spike_molecules) < 1.0
            ):
                match = r
                break
        if match is None:
            continue
        pareto_pd.append(match.pd_rate_hz)
        pareto_nd.append(match.nd_rate_hz)
        pareto_dsi.append(match.dsi_signed)

    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    norm: Normalize = Normalize(vmin=-1.0, vmax=1.0)
    sc = ax.scatter(
        pd_rate,
        nd_rate,
        c=dsi_viable,
        cmap="RdBu_r",
        norm=norm,
        s=14,
        alpha=0.55,
        edgecolors="none",
        zorder=2,
    )
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label("Signed DSI")

    # Diagonal y=x line (DSI=0 locus).
    max_rate: float = float(max(np.max(pd_rate), np.max(nd_rate))) * 1.02
    ax.plot(
        [0, max_rate],
        [0, max_rate],
        color="black",
        linestyle="--",
        linewidth=1.2,
        zorder=3,
        label="PD rate = ND rate (DSI = 0)",
    )

    # Pareto cells -- larger markers with black edge.
    if pareto_pd:
        ax.scatter(
            pareto_pd,
            pareto_nd,
            c=pareto_dsi,
            cmap="RdBu_r",
            norm=norm,
            s=160,
            alpha=1.0,
            edgecolors="black",
            linewidths=1.4,
            zorder=4,
            label=f"Pareto cells (n={len(pareto_pd)})",
        )

    ax.set_xlim(left=-1.0, right=max_rate)
    ax.set_ylim(bottom=-1.0, top=max_rate)
    ax.set_xlabel("PD firing rate (Hz) at 0 deg")
    ax.set_ylabel("ND firing rate (Hz) at 180 deg")
    ax.set_title(
        f"t0129: PD vs ND firing rate, coloured by signed DSI "
        f"(seed {T0129_SEED}, n={len(viable)} viable cells)\n"
        "Cells above the diagonal: ND > PD (reversed preference, negative DSI)"
    )
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=9)
    _save_figure(fig=fig, path=output_path)


def _compute_sign_flip_estimate(
    *,
    t0126_pareto: list[ParetoCell],
) -> dict[str, int | None]:
    """Estimate the count of t0126-Pareto cells with sign-flip vs t0129 signed DSI.

    For the antipodal pair, vector-sum DSI = |signed DSI|, so the magnitudes
    are arithmetically identical. Determining the sign requires the per-direction
    spike counts that t0126 never persisted (``pd_rate_hz=40`` is the
    synthesised placeholder per memory ``project_t0126_cell_trace_synthesised``;
    ``nd_rate_hz`` is null in the t0126 predictions). Therefore the true
    sign-flip count for t0126 is UNKNOWABLE from the persisted artefacts. We
    report this as null and provide the count of t0126-Pareto cells whose
    ``dsi_vector_sum > 0.5`` (the upper bound on the potential sign-flip
    population) as a diagnostic.
    """
    upper_bound: int = sum(1 for c in t0126_pareto if c.dsi_signed > 0.5)
    return {
        "t0126_pareto_size": len(t0126_pareto),
        "t0126_pareto_cells_with_dsi_vector_sum_gt_0p5": upper_bound,
        "t0126_pareto_cells_with_dsi_vector_sum_gt_0p5_and_dsi_signed_lt_0": None,
    }


def build_t0126_vs_t0129_overlay(
    *,
    t0126_pareto: list[ParetoCell],
    t0129_pareto: list[ParetoCell],
    output_path: Path,
) -> None:
    """Chart (d): overlay of t0126 (vector-sum) and t0129 (signed) Pareto fronts.

    t0126's cells are plotted at ``+dsi_vector_sum`` (the magnitude); the true
    signed DSI for those cells is unknowable because t0126 did not persist
    per-direction spike counts (and its ``pd_rate_hz=40`` is the synthesised
    placeholder, per memory ``project_t0126_cell_trace_synthesised``). This is
    annotated on the chart.
    """
    t0126_dsi: NDArray[np.float64] = np.array([c.dsi_signed for c in t0126_pareto])
    t0126_atp_m: NDArray[np.float64] = np.array(
        [c.atp_per_spike_molecules / ATP_M_DIVISOR for c in t0126_pareto]
    )
    t0129_dsi: NDArray[np.float64] = np.array([c.dsi_signed for c in t0129_pareto])
    t0129_atp_m: NDArray[np.float64] = np.array(
        [c.atp_per_spike_molecules / ATP_M_DIVISOR for c in t0129_pareto]
    )

    fig, ax = plt.subplots(figsize=(9.0, 6.0))
    ax.scatter(
        t0126_dsi,
        t0126_atp_m,
        s=140,
        marker="s",
        c="#ff7f0e",
        edgecolors="black",
        linewidths=1.0,
        alpha=0.85,
        label=(f"t0126 Pareto (n={len(t0126_pareto)}, vector-sum DSI, seed {T0126_SEED})"),
        zorder=3,
    )
    ax.scatter(
        t0129_dsi,
        t0129_atp_m,
        s=140,
        marker="o",
        c="#1f77b4",
        edgecolors="black",
        linewidths=1.0,
        alpha=0.85,
        label=(f"t0129 Pareto (n={len(t0129_pareto)}, signed DSI, seed {T0129_SEED})"),
        zorder=4,
    )
    ax.axvline(x=0.0, color="grey", linestyle="--", linewidth=1.0, zorder=1)

    # Note about reprojection limitation (placed in lower-right where data is empty).
    ax.text(
        0.40,
        0.36,
        (
            "Note: t0126 stored only |DSI| (vector-sum magnitude),\n"
            "and its pd_rate_hz=40 is a synthesised placeholder per\n"
            "memory project_t0126_cell_trace_synthesised. The true\n"
            "signed DSI for t0126 cells cannot be recovered, so t0126\n"
            "cells are plotted at +|DSI|. See results_detailed.md."
        ),
        transform=ax.transAxes,
        fontsize=8,
        bbox={"facecolor": "lightyellow", "alpha": 0.95, "edgecolor": "grey"},
        verticalalignment="top",
    )

    ax.set_xlim(-1.05, 1.05)
    ax.set_xlabel("DSI (t0126: vector-sum = |signed|; t0129: signed antipodal)")
    ax.set_ylabel("ATP per spike (millions of molecules)")
    ax.set_title(
        "t0126 vs t0129 Pareto front overlay\n"
        "t0126 = vector-sum DSI (magnitude only, sign discarded), "
        "t0129 = signed antipodal DSI"
    )
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=9)
    _save_figure(fig=fig, path=output_path)


def _write_sign_flip_sidecar(
    *,
    t0126_pareto: list[ParetoCell],
    path: Path,
) -> None:
    """Write the sign-flip sidecar JSON consumed by the metrics builder."""
    estimate = _compute_sign_flip_estimate(t0126_pareto=t0126_pareto)
    estimate_with_provenance: dict[str, object] = dict(estimate)
    estimate_with_provenance["t0126_pareto_seed"] = T0126_SEED
    estimate_with_provenance["note"] = (
        "Sign-flip count is null because t0126 did not persist "
        "per-direction spike counts and its pd_rate_hz=40 is a synthesised "
        "placeholder (per memory project_t0126_cell_trace_synthesised). "
        "The dsi_vector_sum>0.5 count is the upper bound on the potential "
        "sign-flip population."
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(estimate_with_provenance, fh, indent=2)


def main() -> None:
    rows: list[CellRow] = _load_cell_params(path=CELL_PARAMS_JSONL)
    t0129_pareto: list[ParetoCell] = _load_t0129_pareto(
        path=pareto_front_json(seed=T0129_SEED),
    )
    t0126_pareto: list[ParetoCell] = _load_t0126_pareto_vector_sum(
        path=T0126_PARETO_FRONT_JSON,
    )

    print(
        f"[t0129 charts] loaded {len(rows)} cell_params rows, "
        f"{len(t0129_pareto)} t0129 Pareto cells, "
        f"{len(t0126_pareto)} t0126 Pareto cells"
    )

    build_pareto_front_chart(
        pareto_cells=t0129_pareto,
        output_path=PARETO_FRONT_PNG,
    )
    print(f"[t0129 charts] wrote {PARETO_FRONT_PNG}")

    build_dsi_distribution_chart(
        rows=rows,
        output_path=DSI_DISTRIBUTION_PNG,
    )
    print(f"[t0129 charts] wrote {DSI_DISTRIBUTION_PNG}")

    build_pd_vs_nd_scatter(
        rows=rows,
        pareto_cells=t0129_pareto,
        output_path=PD_VS_ND_SCATTER_PNG,
    )
    print(f"[t0129 charts] wrote {PD_VS_ND_SCATTER_PNG}")

    build_t0126_vs_t0129_overlay(
        t0126_pareto=t0126_pareto,
        t0129_pareto=t0129_pareto,
        output_path=T0126_VS_T0129_OVERLAY_PNG,
    )
    print(f"[t0129 charts] wrote {T0126_VS_T0129_OVERLAY_PNG}")

    _write_sign_flip_sidecar(
        t0126_pareto=t0126_pareto,
        path=T0126_VS_T0129_SIGN_FLIP_JSON,
    )
    print(f"[t0129 charts] wrote {T0126_VS_T0129_SIGN_FLIP_JSON}")


if __name__ == "__main__":
    main()
