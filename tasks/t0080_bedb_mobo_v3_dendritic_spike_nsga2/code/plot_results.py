"""Generate Pareto-front and HV-trajectory PNGs from the NSGA-II loop output.

Reads ``results/data/pareto_front.json``, ``results/data/all_evaluations.json``,
and ``results/data/hv_trajectory.json`` and emits:

* ``results/images/pareto_front.png`` — DSI vs PD-rate scatter with t0076 +
  t0078 fronts overlaid as comparisons.
* ``results/images/hypervolume_trajectory.png`` — per-generation HV vs the
  t0076 / t0078 baselines.
* ``results/images/scatter_all_cells.png`` — every evaluated cell coloured
  by feasibility (debugging deep-dive aid).
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.paths import (
    HYPERVOLUME_PNG,
    IMAGES_DIR,
    PARETO_FRONT_JSON,
    PARETO_FRONT_PNG,
    RESULTS_DATA_DIR,
)

T0076_HV_BASELINE: float = 8.41
T0078_HV_BASELINE: float = 11.41
T0080_PASS_DSI: float = 0.4
T0080_PASS_PD_HZ: float = 10.0


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def plot_pareto_front() -> None:
    if not PARETO_FRONT_JSON.exists():
        print(f"[plot] missing {PARETO_FRONT_JSON}; skipping pareto plot")
        return
    data = _load_json(PARETO_FRONT_JSON)
    cells = data.get("cells", [])
    if len(cells) == 0:
        print("[plot] empty pareto front; skipping")
        return
    dsi = [c["dsi"] for c in cells]
    pd = [c["pd_rate_hz"] for c in cells]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(dsi, pd, c="C0", s=60, label=f"t0080 v3 Pareto (n={len(cells)})")
    ax.axvline(
        T0080_PASS_DSI,
        color="red",
        linestyle="--",
        alpha=0.5,
        label=f"DSI threshold = {T0080_PASS_DSI}",
    )
    ax.axhline(
        T0080_PASS_PD_HZ,
        color="red",
        linestyle="--",
        alpha=0.5,
        label=f"PD threshold = {T0080_PASS_PD_HZ} Hz",
    )
    ax.set_xlabel("DSI")
    ax.set_ylabel("PD firing rate (Hz)")
    ax.set_title("t0080 v3 Pareto front (NSGA-II, 54-d)")
    ax.legend(loc="best")
    ax.grid(alpha=0.3)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(PARETO_FRONT_PNG, dpi=150)
    plt.close(fig)
    print(f"[plot] wrote {PARETO_FRONT_PNG}")


def plot_hv_trajectory() -> None:
    hv_path: Path = RESULTS_DATA_DIR / "hv_trajectory.json"
    if not hv_path.exists():
        print(f"[plot] missing {hv_path}; skipping")
        return
    data = _load_json(hv_path)
    traj = data.get("trajectory", [])
    if len(traj) == 0:
        return
    gens = [t["generation"] for t in traj]
    hvs = [t["hypervolume"] for t in traj]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(gens, hvs, "o-", c="C0", label="t0080 v3 NSGA-II")
    ax.axhline(
        T0076_HV_BASELINE,
        color="C1",
        linestyle="--",
        alpha=0.7,
        label=f"t0076 BoTorch (HV={T0076_HV_BASELINE})",
    )
    ax.axhline(
        T0078_HV_BASELINE,
        color="C2",
        linestyle="--",
        alpha=0.7,
        label=f"t0078 BoTorch+AIS (HV={T0078_HV_BASELINE})",
    )
    ax.set_xlabel("Generation")
    ax.set_ylabel("Hypervolume (DSI x PD-rate Hz)")
    ax.set_title("t0080 hypervolume trajectory")
    ax.legend(loc="best")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(HYPERVOLUME_PNG, dpi=150)
    plt.close(fig)
    print(f"[plot] wrote {HYPERVOLUME_PNG}")


def plot_all_cells_scatter() -> None:
    all_path: Path = RESULTS_DATA_DIR / "all_evaluations.json"
    if not all_path.exists():
        return
    cells = _load_json(all_path)
    if not isinstance(cells, list) or len(cells) == 0:
        return
    feas_dsi = [c["dsi"] for c in cells if c["is_feasible"] and not c["is_unstable"]]
    feas_pd = [c["pd_rate_hz"] for c in cells if c["is_feasible"] and not c["is_unstable"]]
    inf_dsi = [c["dsi"] for c in cells if not c["is_feasible"] or c["is_unstable"]]
    inf_pd = [c["pd_rate_hz"] for c in cells if not c["is_feasible"] or c["is_unstable"]]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(
        inf_dsi,
        inf_pd,
        c="lightgray",
        s=20,
        alpha=0.5,
        label=f"infeasible/unstable (n={len(inf_dsi)})",
    )
    ax.scatter(
        feas_dsi, feas_pd, c="C0", s=30, alpha=0.7, label=f"feasible stable (n={len(feas_dsi)})"
    )
    ax.axvline(T0080_PASS_DSI, color="red", linestyle="--", alpha=0.5)
    ax.axhline(T0080_PASS_PD_HZ, color="red", linestyle="--", alpha=0.5)
    ax.set_xlabel("DSI")
    ax.set_ylabel("PD firing rate (Hz)")
    ax.set_title(f"t0080 all evaluated cells (n={len(cells)})")
    ax.legend(loc="best")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out_path: Path = IMAGES_DIR / "all_cells_scatter.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"[plot] wrote {out_path}")


def find_closest_to_joint() -> dict:
    """Return the Pareto cell with smallest distance to (DSI=0.4, PD=10)."""
    if not PARETO_FRONT_JSON.exists():
        return {}
    data = _load_json(PARETO_FRONT_JSON)
    cells = data.get("cells", [])
    if len(cells) == 0:
        return {}
    target = np.array([T0080_PASS_DSI, T0080_PASS_PD_HZ], dtype=np.float64)
    best = None
    best_dist = float("inf")
    for c in cells:
        dist = float(np.linalg.norm(np.array([c["dsi"], c["pd_rate_hz"]]) - target))
        if dist < best_dist:
            best_dist = dist
            best = c
    if best is not None:
        best = dict(best)
        best["_distance_to_joint"] = best_dist
    return best or {}


def main() -> int:
    plot_pareto_front()
    plot_hv_trajectory()
    plot_all_cells_scatter()
    closest = find_closest_to_joint()
    if closest:
        print(
            f"[closest-to-joint] cell {closest.get('cell_index', '?')}: "
            f"dsi={closest['dsi']:.3f} pd={closest['pd_rate_hz']:.2f} "
            f"distance={closest.get('_distance_to_joint', float('nan')):.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
