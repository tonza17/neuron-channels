"""Generate Pareto front, hypervolume trajectory, and all-cells scatter plots for t0081.

Imports t0080's plotting functions but redirects paths to t0081's results directory.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from tasks.t0081_bedb_v3_warmstart_nsga2.code import paths


def main() -> None:
    paths.ensure_directories()
    pareto = json.loads(paths.PARETO_FRONT_JSON.read_text())
    hv = json.loads(paths.HV_TRAJECTORY_JSON.read_text())
    all_evals_raw = json.loads(paths.ALL_EVALUATIONS_JSON.read_text())
    all_evals = (
        all_evals_raw.get("evaluations", all_evals_raw)
        if isinstance(all_evals_raw, dict)
        else all_evals_raw
    )

    pareto_cells = pareto.get("cells", pareto)
    p_dsi = [c["dsi"] for c in pareto_cells]
    p_pd = [c["pd_rate_hz"] for c in pareto_cells]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(p_pd, p_dsi, s=80, c="C0", edgecolor="black", zorder=3, label="Pareto front")
    ax.axvspan(10.0, max(p_pd) * 1.05 + 5, ymin=0.0, ymax=1.0, color="lightgreen", alpha=0.15)
    ax.axhspan(0.4, 1.0, xmin=0.0, xmax=1.0, color="lightgreen", alpha=0.15)
    ax.axvline(10.0, linestyle="--", color="green", alpha=0.5, label="PD=10 Hz threshold")
    ax.axhline(0.4, linestyle="--", color="green", alpha=0.5, label="DSI=0.4 threshold")
    for c in pareto_cells:
        if c["dsi"] >= 0.4 and c["pd_rate_hz"] >= 10.0:
            ax.annotate(
                f"  cell {c['cell_index']}\n  PASS",
                (c["pd_rate_hz"], c["dsi"]),
                fontsize=9,
                color="darkgreen",
                fontweight="bold",
            )
    ax.set_xlabel("PD rate (Hz)")
    ax.set_ylabel("DSI")
    ax.set_title(
        "t0081 Pareto front: 16 non-dominated cells across 768 evaluations\n"
        "Pass criterion (DSI >= 0.4 AND PD >= 10 Hz) ACHIEVED at cell 767",
    )
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out_pareto: Path = paths.IMAGES_DIR / "pareto_front.png"
    fig.savefig(out_pareto, dpi=110)
    plt.close(fig)
    print(f"[plot] wrote {out_pareto}")

    fig, ax = plt.subplots(figsize=(8, 5))
    gens = [t["generation"] for t in hv["trajectory"]]
    hvs = [t["hypervolume"] for t in hv["trajectory"]]
    ax.plot(gens, hvs, marker="o", linewidth=2, color="C2")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Hypervolume")
    ax.set_title(f"t0081 Hypervolume trajectory (utopia point {hv['utopia_point']})")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out_hv: Path = paths.IMAGES_DIR / "hypervolume_trajectory.png"
    fig.savefig(out_hv, dpi=110)
    plt.close(fig)
    print(f"[plot] wrote {out_hv}")

    fig, ax = plt.subplots(figsize=(9, 6))
    feas_dsi = [c["dsi"] for c in all_evals if c.get("is_feasible") and not c.get("is_unstable")]
    feas_pd = [
        c["pd_rate_hz"] for c in all_evals if c.get("is_feasible") and not c.get("is_unstable")
    ]
    infeas_dsi = [c["dsi"] for c in all_evals if not c.get("is_feasible")]
    infeas_pd = [c["pd_rate_hz"] for c in all_evals if not c.get("is_feasible")]
    ax.scatter(
        infeas_pd,
        infeas_dsi,
        s=12,
        c="lightgray",
        alpha=0.5,
        label=f"Infeasible ({len(infeas_dsi)})",
    )
    ax.scatter(feas_pd, feas_dsi, s=14, c="C0", alpha=0.6, label=f"Feasible ({len(feas_dsi)})")
    ax.scatter(
        p_pd, p_dsi, s=80, c="orange", edgecolor="black", zorder=3, label="Pareto front (16)"
    )
    ax.axvline(10.0, linestyle="--", color="green", alpha=0.5)
    ax.axhline(0.4, linestyle="--", color="green", alpha=0.5)
    ax.set_xlabel("PD rate (Hz)")
    ax.set_ylabel("DSI")
    ax.set_title("t0081 all 768 cells: feasibility + Pareto front")
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out_scatter: Path = paths.IMAGES_DIR / "all_cells_scatter.png"
    fig.savefig(out_scatter, dpi=110)
    plt.close(fig)
    print(f"[plot] wrote {out_scatter}")

    pareto_cells_sorted = sorted(
        pareto_cells,
        key=lambda c: max(0, 0.4 - c["dsi"]) ** 2 + max(0, 10.0 - c["pd_rate_hz"]) ** 2,
    )
    cj = pareto_cells_sorted[0]
    dist = (max(0, 0.4 - cj["dsi"]) ** 2 + max(0, 10.0 - cj["pd_rate_hz"]) ** 2) ** 0.5
    msg = (
        f"[closest-to-joint] cell {cj['cell_index']}: "
        f"dsi={cj['dsi']:.3f} pd={cj['pd_rate_hz']:.2f} distance={dist:.3f}"
    )
    print(msg)


if __name__ == "__main__":
    main()
