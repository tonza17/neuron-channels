"""Generate Pareto front, hypervolume trajectory, all-cells scatter, and
per-generation parameter-distribution plots for t0083 (REQ-14, REQ-16).

The HV trajectory plot includes a vertical dashed line at gen=8 marking the
t0081 -> t0083 boundary so the continuation behaviour is visually distinct
from the warm-start trajectory.

The per-generation parameter-distribution plot tracks population mean +/- std
of a curated subset of high-importance parameters (AIS Nav1.6, AIS geometry,
dendritic-spike machinery, slow-AHP) across all 18 generations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import ParamIndex
from tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code import paths

GEN_BOUNDARY: int = 8

# Curated 12-dim subset of high-importance parameters for the
# per-generation distribution chart.
CURATED_PARAM_INDICES: tuple[tuple[ParamIndex, str], ...] = (
    (ParamIndex.NAV16_AIS_GBAR, "Nav1.6 AIS"),
    (ParamIndex.NAV16_SOMA_GBAR, "Nav1.6 soma"),
    (ParamIndex.KV3_AIS_GBAR, "Kv3 AIS"),
    (ParamIndex.AIS_LENGTH_UM, "AIS length"),
    (ParamIndex.AIS_DIAMETER_UM, "AIS diameter"),
    (ParamIndex.SKAHP_GBAR_SOMA_AIS, "SKAHP gbar"),
    (ParamIndex.SKAHP_TAU_CA_MULTIPLIER, "SKAHP tau_ca mult"),
    (ParamIndex.GNMDA_DEND, "gNMDA dend"),
    (ParamIndex.MG_CONC_MM, "Mg conc"),
    (ParamIndex.NAV16_DEND_DISTAL, "Nav1.6 dend distal"),
    (ParamIndex.NAP_DEND_DISTAL, "NaP dend distal"),
    (ParamIndex.W_ACH_US, "ACh weight"),
)


def _load_pareto() -> list[dict[str, Any]]:
    raw = json.loads(paths.PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    return raw.get("cells", raw) if isinstance(raw, dict) else raw


def _load_hv() -> dict[str, Any]:
    raw = json.loads(paths.HV_TRAJECTORY_JSON.read_text(encoding="utf-8"))
    return raw if isinstance(raw, dict) else {"trajectory": raw, "utopia_point": [0.7, 80.0]}


def _load_all_evals() -> list[dict[str, Any]]:
    raw = json.loads(paths.ALL_EVALUATIONS_JSON.read_text(encoding="utf-8"))
    return raw.get("evaluations", raw) if isinstance(raw, dict) else raw


def _plot_pareto_front(*, pareto: list[dict[str, Any]]) -> Path:
    p_dsi = [float(c["dsi"]) for c in pareto]
    p_pd = [float(c["pd_rate_hz"]) for c in pareto]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(p_pd, p_dsi, s=80, c="C0", edgecolor="black", zorder=3, label="Pareto front")
    if len(p_pd) > 0:
        ax.axvspan(10.0, max(p_pd) * 1.05 + 5, ymin=0.0, ymax=1.0, color="lightgreen", alpha=0.15)
    ax.axhspan(0.4, 1.0, xmin=0.0, xmax=1.0, color="lightgreen", alpha=0.15)
    ax.axvline(10.0, linestyle="--", color="green", alpha=0.5, label="PD=10 Hz threshold")
    ax.axhline(0.4, linestyle="--", color="green", alpha=0.5, label="DSI=0.4 threshold")
    n_joint = 0
    for c in pareto:
        if float(c["dsi"]) >= 0.4 and float(c["pd_rate_hz"]) >= 10.0:
            n_joint += 1
            ax.annotate(
                f"  cell {int(c['cell_index'])}\n  PASS",
                (float(c["pd_rate_hz"]), float(c["dsi"])),
                fontsize=9,
                color="darkgreen",
                fontweight="bold",
            )
    ax.set_xlabel("PD rate (Hz)")
    ax.set_ylabel("DSI")
    ax.set_title(
        f"t0083 Pareto front: {len(pareto)} non-dominated cells\n"
        f"Pass criterion (DSI >= 0.4 AND PD >= 10 Hz) achieved by {n_joint} cell(s)"
    )
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out_path: Path = paths.IMAGES_DIR / "pareto_front.png"
    fig.savefig(out_path, dpi=110)
    plt.close(fig)
    return out_path


def _plot_hv_trajectory(*, hv: dict[str, Any]) -> Path:
    traj = hv["trajectory"]
    gens = [int(t["generation"]) for t in traj]
    hvs = [float(t["hypervolume"]) for t in traj]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(gens, hvs, marker="o", linewidth=2, color="C2")
    ax.axvline(
        GEN_BOUNDARY,
        linestyle="--",
        color="red",
        alpha=0.6,
        label=f"t0081 -> t0083 boundary (gen {GEN_BOUNDARY})",
    )
    ax.set_xlabel("Generation")
    ax.set_ylabel("Hypervolume")
    ax.set_title(
        f"t0083 hypervolume trajectory (utopia point {hv['utopia_point']})\n"
        f"Final HV = {hvs[-1]:.3f} after {len(hvs)} generations"
    )
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out_path: Path = paths.IMAGES_DIR / "hypervolume_trajectory.png"
    fig.savefig(out_path, dpi=110)
    plt.close(fig)
    return out_path


def _plot_all_cells_scatter(
    *,
    all_evals: list[dict[str, Any]],
    pareto: list[dict[str, Any]],
) -> Path:
    feas_dsi = [
        float(c["dsi"]) for c in all_evals if c.get("is_feasible") and not c.get("is_unstable")
    ]
    feas_pd = [
        float(c["pd_rate_hz"])
        for c in all_evals
        if c.get("is_feasible") and not c.get("is_unstable")
    ]
    infeas_dsi = [float(c["dsi"]) for c in all_evals if not c.get("is_feasible")]
    infeas_pd = [float(c["pd_rate_hz"]) for c in all_evals if not c.get("is_feasible")]
    p_dsi = [float(c["dsi"]) for c in pareto]
    p_pd = [float(c["pd_rate_hz"]) for c in pareto]
    fig, ax = plt.subplots(figsize=(9, 6))
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
        p_pd,
        p_dsi,
        s=80,
        c="orange",
        edgecolor="black",
        zorder=3,
        label=f"Pareto front ({len(p_pd)})",
    )
    ax.axvline(10.0, linestyle="--", color="green", alpha=0.5)
    ax.axhline(0.4, linestyle="--", color="green", alpha=0.5)
    ax.set_xlabel("PD rate (Hz)")
    ax.set_ylabel("DSI")
    ax.set_title(f"t0083 all {len(all_evals)} cells: feasibility + Pareto front")
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out_path: Path = paths.IMAGES_DIR / "all_cells_scatter.png"
    fig.savefig(out_path, dpi=110)
    plt.close(fig)
    return out_path


def _plot_parameter_distribution_per_generation(
    *,
    all_evals: list[dict[str, Any]],
) -> Path:
    by_gen: dict[int, list[list[float]]] = {}
    for c in all_evals:
        gen = int(c["generation"])
        by_gen.setdefault(gen, []).append([float(v) for v in c["params"]])
    gens = sorted(by_gen)
    n_params_curated = len(CURATED_PARAM_INDICES)
    n_cols = 3
    n_rows = (n_params_curated + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(13, 2.5 * n_rows), squeeze=False)
    for i, (param_idx, label) in enumerate(CURATED_PARAM_INDICES):
        row, col = divmod(i, n_cols)
        ax = axes[row][col]
        means: list[float] = []
        stds: list[float] = []
        for gen in gens:
            vals = np.asarray(
                [params[int(param_idx)] for params in by_gen[gen]],
                dtype=np.float64,
            )
            means.append(float(np.mean(vals)))
            stds.append(float(np.std(vals)))
        means_arr = np.asarray(means, dtype=np.float64)
        stds_arr = np.asarray(stds, dtype=np.float64)
        ax.plot(gens, means_arr, marker="o", color="C0", label="mean")
        ax.fill_between(gens, means_arr - stds_arr, means_arr + stds_arr, color="C0", alpha=0.25)
        ax.axvline(GEN_BOUNDARY, linestyle="--", color="red", alpha=0.5)
        ax.set_title(f"{label} (idx {int(param_idx)})", fontsize=10)
        ax.set_xlabel("gen")
        ax.grid(alpha=0.3)
    # Hide unused axes.
    for j in range(n_params_curated, n_rows * n_cols):
        row, col = divmod(j, n_cols)
        axes[row][col].axis("off")
    fig.suptitle(
        "t0083 per-generation parameter distribution (mean +/- std)\n"
        f"Vertical line: t0081 -> t0083 boundary (gen {GEN_BOUNDARY})",
        fontsize=12,
    )
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
    out_path: Path = paths.IMAGES_DIR / "parameter_distribution_per_generation.png"
    fig.savefig(out_path, dpi=110)
    plt.close(fig)
    return out_path


def _save_parameter_distribution_json(*, all_evals: list[dict[str, Any]]) -> None:
    by_gen: dict[int, list[list[float]]] = {}
    for c in all_evals:
        gen = int(c["generation"])
        by_gen.setdefault(gen, []).append([float(v) for v in c["params"]])
    rows: list[dict[str, Any]] = []
    for gen in sorted(by_gen):
        params_arr = np.asarray(by_gen[gen], dtype=np.float64)
        per_dim_mean = params_arr.mean(axis=0).tolist()
        per_dim_std = params_arr.std(axis=0).tolist()
        rows.append(
            {
                "generation": gen,
                "n": int(params_arr.shape[0]),
                "mean": per_dim_mean,
                "std": per_dim_std,
            },
        )
    paths.PARAMETER_DISTRIBUTION_JSON.write_text(
        json.dumps(rows, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    paths.ensure_directories()
    pareto = _load_pareto()
    hv = _load_hv()
    all_evals = _load_all_evals()
    out_pareto = _plot_pareto_front(pareto=pareto)
    print(f"[plot] wrote {out_pareto}")
    out_hv = _plot_hv_trajectory(hv=hv)
    print(f"[plot] wrote {out_hv}")
    out_scatter = _plot_all_cells_scatter(all_evals=all_evals, pareto=pareto)
    print(f"[plot] wrote {out_scatter}")
    out_param = _plot_parameter_distribution_per_generation(all_evals=all_evals)
    print(f"[plot] wrote {out_param}")
    _save_parameter_distribution_json(all_evals=all_evals)
    print(f"[plot] wrote {paths.PARAMETER_DISTRIBUTION_JSON}")
    pareto_sorted = sorted(
        pareto,
        key=lambda c: (
            max(0.0, 0.4 - float(c["dsi"])) ** 2 + max(0.0, 10.0 - float(c["pd_rate_hz"])) ** 2
        ),
    )
    if len(pareto_sorted) > 0:
        cj = pareto_sorted[0]
        dist = (
            max(0.0, 0.4 - float(cj["dsi"])) ** 2 + max(0.0, 10.0 - float(cj["pd_rate_hz"])) ** 2
        ) ** 0.5
        print(
            f"[closest-to-joint] cell {int(cj['cell_index'])}: "
            f"dsi={float(cj['dsi']):.3f} pd={float(cj['pd_rate_hz']):.2f} "
            f"distance={dist:.3f}"
        )


if __name__ == "__main__":
    main()
