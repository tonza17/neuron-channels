"""Generate t0112 result charts and CSV tables.

Reads:
* `tasks/t0112_t0106_seed77_replicate/results/data/all_evaluations_seed77.json.gz`
* `tasks/t0112_t0106_seed77_replicate/results/data/pareto_front_seed77.json`
* `tasks/t0112_t0106_seed77_replicate/results/data/hv_trajectory_seed77.json`
* `tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/.../files/all_evaluations_seed44.json.gz`

Writes:
* `results/images/pareto_front_seed44_vs_seed77.png`
* `results/images/hv_vs_gen_seed44_vs_seed77.png`
* `results/images/joint_pass_yield_per_gen.png`
* `results/images/top50_morphologies_seed77.png` (or a placeholder if morphology builder is absent)
* `results/images/asymmetry_distribution_seed44_vs_seed77.png`
* `results/data/joint_pass_summary.csv`
* `results/data/pareto_front_overlap.csv`
"""

from __future__ import annotations

import csv
import gzip
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

TASK_DIR: Path = Path(__file__).resolve().parent.parent
T0106_DIR: Path = TASK_DIR.parent / "t0106_long_pdnd_nsga2_300gen"

T0112_EVALS: Path = TASK_DIR / "results" / "data" / "all_evaluations_seed77.json.gz"
T0112_PARETO: Path = TASK_DIR / "results" / "data" / "pareto_front_seed77.json"
T0112_HV: Path = TASK_DIR / "results" / "data" / "hv_trajectory_seed77.json"

T0106_EVALS: Path = (
    T0106_DIR
    / "assets"
    / "predictions"
    / "nsga2-seed44-bedb-morph-2dir-300gen"
    / "files"
    / "all_evaluations_seed44.json.gz"
)
T0106_PARETO: Path = T0106_DIR / "results" / "data" / "pareto_front_seed44.json"
T0106_HV: Path = T0106_DIR / "results" / "data" / "hv_trajectory_seed44.json"

IMAGES_DIR: Path = TASK_DIR / "results" / "images"
DATA_DIR: Path = TASK_DIR / "results" / "data"


def _load_evals_gz(path: Path) -> list[dict]:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        data = json.load(f)
    return data["evaluations"] if isinstance(data, dict) else data


def _load_evals_json(path: Path) -> list[dict]:
    if path.suffix == ".gz":
        return _load_evals_gz(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["evaluations"] if isinstance(data, dict) else data


def _load_official_pareto(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["cells"]


def chart_pareto_front(t0112: list[dict], t0106: list[dict]) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))
    pf106 = _load_official_pareto(T0106_PARETO)
    pf112 = _load_official_pareto(T0112_PARETO)
    x106 = [c["dsi_vector_sum"] for c in pf106]
    y106 = [c["pd_rate_hz"] for c in pf106]
    x112 = [c["dsi_vector_sum"] for c in pf112]
    y112 = [c["pd_rate_hz"] for c in pf112]
    ax.scatter(x106, y106, s=40, alpha=0.7, label=f"t0106 seed 44 (n={len(pf106)})", color="C0")
    ax.scatter(
        x112,
        y112,
        s=40,
        alpha=0.7,
        label=f"t0112 seed 77 (n={len(pf112)})",
        color="C3",
        marker="D",
    )
    ax.axvline(0.5, color="grey", ls="--", lw=0.8, alpha=0.6)
    ax.axhline(30, color="grey", ls="--", lw=0.8, alpha=0.6)
    ax.set_xlabel("ratio DSI")
    ax.set_ylabel("PD-rate (Hz)")
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, max(max(y106), max(y112)) * 1.05)
    ax.set_title("Strict Pareto fronts: t0106 seed 44 vs t0112 seed 77")
    ax.legend()
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "pareto_front_seed44_vs_seed77.png", dpi=120)
    plt.close(fig)


def chart_hv_vs_gen() -> None:
    hv112 = json.loads(T0112_HV.read_text(encoding="utf-8"))["trajectory"]
    hv106 = json.loads(T0106_HV.read_text(encoding="utf-8"))["trajectory"]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(
        [h["generation"] for h in hv106],
        [h["hypervolume"] for h in hv106],
        label="t0106 seed 44 (restart every 25)",
        color="C0",
        lw=1.5,
    )
    ax.plot(
        [h["generation"] for h in hv112],
        [h["hypervolume"] for h in hv112],
        label="t0112 seed 77 (restart every 10)",
        color="C3",
        lw=1.5,
        ls="-",
        marker="D",
        ms=4,
    )
    for g in [10, 20, 30, 40]:
        ax.axvline(g, color="lightgrey", ls=":", lw=0.6)
    ax.set_yscale("log")
    ax.set_xlabel("generation")
    ax.set_ylabel("hypervolume (log scale)")
    ax.set_title("HV trajectory: seed 44 vs seed 77 (pool-restart cadence annotated)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "hv_vs_gen_seed44_vs_seed77.png", dpi=120)
    plt.close(fig)


def _joint_pass_per_gen(cells: list[dict]) -> dict[int, int]:
    out: dict[int, int] = {}
    seen_params: set[tuple[float, ...]] = set()
    for gen in sorted({c["generation"] for c in cells}):
        for c in [c for c in cells if c["generation"] == gen]:
            if c["dsi_vector_sum"] >= 0.5 and c["pd_rate_hz"] >= 30:
                seen_params.add(tuple(c["vector_68d"]))
        out[gen] = len(seen_params)
    return out


def chart_joint_pass_yield(t0112: list[dict], t0106: list[dict]) -> None:
    yp112 = _joint_pass_per_gen(t0112)
    yp106 = _joint_pass_per_gen(t0106)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(
        list(yp106.keys()),
        list(yp106.values()),
        label="t0106 seed 44",
        color="C0",
        lw=1.5,
    )
    ax.plot(
        list(yp112.keys()),
        list(yp112.values()),
        label="t0112 seed 77",
        color="C3",
        lw=1.5,
        marker="D",
        ms=4,
    )
    ax.set_xlabel("generation")
    ax.set_ylabel("cumulative unique joint-pass cells")
    ax.set_title("Joint-pass cell discovery per generation")
    ax.legend()
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "joint_pass_yield_per_gen.png", dpi=120)
    plt.close(fig)


def chart_top50_placeholder() -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.text(
        0.5,
        0.5,
        "Top-50 morphology grid not rendered.\n"
        "t0112 has only 7 unique joint-pass cells (< 50);\n"
        "morphology archetype split mirrors t0106's analysis path.",
        ha="center",
        va="center",
        fontsize=12,
        transform=ax.transAxes,
    )
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "top50_morphologies_seed77.png", dpi=120)
    plt.close(fig)


def chart_asymmetry_distribution(t0112: list[dict], t0106: list[dict]) -> None:
    # Morphology indices in the 68-d vector are positions 54..67.
    # Picks: 54=soma_offset_y, 55=elongation, 60=branch_density_gradient,
    # 65=primary_branch_pd_concentration (best-effort indices per plan brief).
    morph_idx = {
        "soma_offset_y": 54,
        "elongation": 55,
        "branch_density_gradient": 60,
        "primary_branch_pd_concentration": 65,
    }
    by_dsi_t106 = sorted(t0106, key=lambda c: c["dsi_vector_sum"], reverse=True)[:50]
    by_dsi_t112 = sorted(t0112, key=lambda c: c["dsi_vector_sum"], reverse=True)[:50]
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    for ax, (name, idx) in zip(axes, morph_idx.items(), strict=False):
        v106 = [c["vector_68d"][idx] for c in by_dsi_t106]
        v112 = [c["vector_68d"][idx] for c in by_dsi_t112]
        ax.hist(v106, bins=15, alpha=0.5, label="t0106 seed 44", color="C0")
        ax.hist(v112, bins=15, alpha=0.5, label="t0112 seed 77", color="C3")
        ax.set_title(name.replace("_", " "))
        ax.set_xlabel("value")
        ax.set_ylabel("count")
        if name == "soma_offset_y":
            ax.legend()
    fig.suptitle("Morphology distributions: top-50-by-DSI cells, seed 44 vs seed 77")
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "asymmetry_distribution_seed44_vs_seed77.png", dpi=120)
    plt.close(fig)


def csv_joint_pass_summary(t0112: list[dict], t0106: list[dict], hv112: dict, hv106: dict) -> None:
    rows: list[dict] = []
    for label, cells, hv in (("t0106_seed44", t0106, hv106), ("t0112_seed77", t0112, hv112)):
        jp = [c for c in cells if c["dsi_vector_sum"] >= 0.5 and c["pd_rate_hz"] >= 30]
        unique = {tuple(c["vector_68d"]) for c in jp}
        rows.append(
            {
                "task_seed_label": label,
                "n_total_evals": len(cells),
                "n_generations_completed": max(c["generation"] for c in cells),
                "n_joint_pass_unique": len(unique),
                "n_joint_pass_evaluations": len(jp),
                "best_dsi": round(max(c["dsi_vector_sum"] for c in cells), 4),
                "best_pd_rate_hz": round(max(c["pd_rate_hz"] for c in cells), 2),
                "final_hypervolume": round(hv["trajectory"][-1]["hypervolume"], 4),
                "n_generations_to_plateau": max(c["generation"] for c in cells),
            }
        )
    with (DATA_DIR / "joint_pass_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_pareto_overlap(t0112: list[dict], t0106: list[dict]) -> None:
    pf112 = _load_official_pareto(T0112_PARETO)
    pf106 = _load_official_pareto(T0106_PARETO)
    v112 = np.array([c["vector_68d"] for c in pf112])
    v106 = np.array([c["vector_68d"] for c in pf106])
    rows: list[dict] = []
    for i, p in enumerate(v112):
        dists = np.linalg.norm(v106 - p, axis=1)
        nn = int(np.argmin(dists))
        rows.append(
            {
                "t0112_pareto_idx": i,
                "t0112_dsi": round(pf112[i]["dsi_vector_sum"], 4),
                "t0112_pd_rate_hz": round(pf112[i]["pd_rate_hz"], 2),
                "t0112_generation": pf112[i].get("generation", -1),
                "nn_t0106_pareto_idx": nn,
                "nn_t0106_dsi": round(pf106[nn]["dsi_vector_sum"], 4),
                "nn_t0106_pd_rate_hz": round(pf106[nn]["pd_rate_hz"], 2),
                "nn_t0106_generation": pf106[nn].get("generation", -1),
                "param_space_l2_distance": round(float(np.min(dists)), 4),
            }
        )
    with (DATA_DIR / "pareto_front_overlap.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("Loading t0112 evaluations...")
    t0112 = _load_evals_json(T0112_EVALS)
    print(f"  {len(t0112)} cells")
    print("Loading t0106 evaluations...")
    t0106 = _load_evals_json(T0106_EVALS)
    print(f"  {len(t0106)} cells")
    hv112 = json.loads(T0112_HV.read_text(encoding="utf-8"))
    hv106 = json.loads(T0106_HV.read_text(encoding="utf-8"))

    print("Chart 1: pareto front overlay")
    chart_pareto_front(t0112, t0106)
    print("Chart 2: HV vs gen")
    chart_hv_vs_gen()
    print("Chart 3: joint-pass yield per gen")
    chart_joint_pass_yield(t0112, t0106)
    print("Chart 4: top-50 morphologies placeholder")
    chart_top50_placeholder()
    print("Chart 5: asymmetry distribution")
    chart_asymmetry_distribution(t0112, t0106)
    print("CSV 1: joint_pass_summary")
    csv_joint_pass_summary(t0112, t0106, hv112, hv106)
    print("CSV 2: pareto_front_overlap")
    csv_pareto_overlap(t0112, t0106)
    print("Done.")


if __name__ == "__main__":
    main()
