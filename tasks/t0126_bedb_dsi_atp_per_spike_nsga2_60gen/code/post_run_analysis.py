"""Top-level orchestrator for t0126 post-run analysis steps 10-15.

Runs after the NSGA-II results have been synced back from remote. Produces:
* The cross-comparison chart and comparator report (Step 10).
* The five core charts (Step 11).
* The top-50 morphology grid (Step 12).
* metrics.json (Step 13).
* The predictions asset (Step 14).
* The answer asset (Step 15).

Each sub-step is idempotent. The script does not call any verificator; the
caller invokes those after the build steps complete.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code import t0124_vs_t0126_comparator
from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.paths import (
    IMAGES_DIR,
    RESULTS_DATA_DIR,
    TASK_ROOT,
)

COMPARATOR_CHART_PATH: Path = IMAGES_DIR / "pareto_front_t0124_vs_t0126.png"
COMPARATOR_JSON_PATH: Path = RESULTS_DATA_DIR / "comparator_report.json"


def run_comparator(*, seed: int, repo_root: Path) -> dict[str, Any]:
    """Step 10: cross-comparison module."""
    pareto_path = RESULTS_DATA_DIR / f"pareto_front_seed{seed}.json"
    if not pareto_path.exists():
        raise FileNotFoundError(f"t0126 Pareto front file not found at {pareto_path}")

    report = t0124_vs_t0126_comparator.run_t0124_vs_t0126_comparison(
        t0126_pareto_path=pareto_path,
        output_chart_path=COMPARATOR_CHART_PATH,
        repo_root=repo_root,
        n_bootstrap=2000,
    )

    report_dict: dict[str, Any] = {
        "t0124_front_n": report.t0124_front.n,
        "t0124_front_seed": report.t0124_front.seed,
        "t0126_front_n": report.t0126_front.n,
        "t0126_front_seed": report.t0126_front.seed,
        "t0124_bootstrap_r": {
            "r": report.t0124_r.r,
            "ci_low": report.t0124_r.ci_low,
            "ci_high": report.t0124_r.ci_high,
            "n": report.t0124_r.n,
            "n_resamples": report.t0124_r.n_resamples,
        },
        "t0126_bootstrap_r": {
            "r": report.t0126_r.r,
            "ci_low": report.t0126_r.ci_low,
            "ci_high": report.t0126_r.ci_high,
            "n": report.t0126_r.n,
            "n_resamples": report.t0126_r.n_resamples,
        },
        "n_t0124_dominated_by_t0126": report.n_t0124_dominated_by_t0126,
        "dominance_mask_t0124": list(report.dominance_mask_t0124),
        "verdict": report.verdict,
        "verdict_rationale": report.verdict_rationale,
        "decision_rule": {
            "carter_bean_min_r": t0124_vs_t0126_comparator.CARTER_BEAN_MIN_R,
            "artefact_max_r": t0124_vs_t0126_comparator.ARTEFACT_MAX_R,
            "min_n_for_verdict": t0124_vs_t0126_comparator.MIN_N_FOR_VERDICT,
        },
    }
    COMPARATOR_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    COMPARATOR_JSON_PATH.write_text(json.dumps(report_dict, indent=2), encoding="utf-8")
    print(f"[post_run] wrote {COMPARATOR_JSON_PATH}")
    return report_dict


def _load_hv_trace(*, seed: int) -> list[dict[str, Any]]:
    """Load hv_trace.jsonl rows."""
    hv_trace_path = TASK_ROOT / "logs" / "steps" / "009_implementation" / "hv_trace.jsonl"
    rows: list[dict[str, Any]] = []
    if not hv_trace_path.exists():
        return rows
    for line in hv_trace_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def render_hv_trajectory(*, seed: int) -> Path:
    """Step 11 sub-step: hypervolume trajectory chart."""
    import matplotlib.pyplot as plt

    rows = _load_hv_trace(seed=seed)
    if len(rows) == 0:
        print(f"[post_run] warning: no hv_trace.jsonl rows for seed {seed}")
        return IMAGES_DIR / f"hv_trajectory_seed{seed}.png"

    gens = [int(r["gen"]) for r in rows]
    hvs = [float(r["hv"]) for r in rows]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(gens, hvs, marker="o", color="tab:blue", linewidth=1.5)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Hypervolume (HV)")
    ax.set_title(f"NSGA-II Hypervolume Trajectory (seed {seed}, gen 1 - gen {gens[-1]})")
    ax.grid(True, alpha=0.3)
    ax.axvline(60, color="red", linestyle="--", alpha=0.6, label="N_GEN_MAX = 60")
    ax.legend()
    output_path = IMAGES_DIR / f"hv_trajectory_seed{seed}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=140)
    plt.close(fig)
    print(f"[post_run] wrote {output_path}")
    return output_path


def render_pareto_front_dsi_vs_atp(*, seed: int) -> Path:
    """Step 11 sub-step: Pareto front chart with joint-pass highlight."""
    import matplotlib.pyplot as plt

    pareto_path = RESULTS_DATA_DIR / f"pareto_front_seed{seed}.json"
    raw = json.loads(pareto_path.read_text(encoding="utf-8"))
    cells = raw.get("cells", [])

    dsi_list: list[float] = []
    atp_list: list[float] = []
    pd_rate_list: list[float | None] = []
    for c in cells:
        dsi = c.get("dsi_best_legit")
        if dsi is None:
            dsi = c.get("dsi_vector_sum")
        if dsi is None:
            continue
        atp = c.get("atp_per_spike_molecules")
        if atp is None:
            continue
        dsi_list.append(float(dsi))
        atp_list.append(float(atp))
        pd_rate_list.append(c.get("pd_rate_hz"))

    median_atp = float(np.median(atp_list)) if len(atp_list) > 0 else float("nan")
    joint_pass: list[bool] = []
    for dsi, atp, pd_rate in zip(dsi_list, atp_list, pd_rate_list, strict=True):
        if pd_rate is None:
            joint_pass.append(False)
            continue
        joint_pass.append(
            dsi >= 0.5 and float(pd_rate) >= 30.0 and atp <= median_atp,
        )

    fig, ax = plt.subplots(figsize=(10, 7))
    not_joint = [not j for j in joint_pass]
    ax.scatter(
        [a for a, m in zip(atp_list, not_joint, strict=True) if m],
        [d for d, m in zip(dsi_list, not_joint, strict=True) if m],
        c="tab:blue",
        s=60,
        marker="s",
        label="Pareto cell",
        edgecolors="black",
        linewidths=0.4,
        alpha=0.7,
    )
    if any(joint_pass):
        ax.scatter(
            [a for a, m in zip(atp_list, joint_pass, strict=True) if m],
            [d for d, m in zip(dsi_list, joint_pass, strict=True) if m],
            c="tab:green",
            s=120,
            marker="*",
            label="joint-pass (DSI >= 0.5, PD >= 30 Hz, ATP <= median)",
            edgecolors="black",
            linewidths=0.6,
        )
    ax.set_xscale("log")
    ax.set_xlabel("ATP per spike (molecules), log scale, lower is better")
    ax.set_ylabel("DSI (best legit), higher is better")
    ax.set_title(
        f"Pareto Front: DSI vs ATP-per-Spike (t0126 60-gen, seed {seed}, n={len(cells)})",
    )
    ax.grid(True, alpha=0.3, which="both")
    ax.legend(loc="best")
    ax.set_ylim(-0.05, 1.05)
    output_path = IMAGES_DIR / "pareto_front_dsi_vs_atp.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=140)
    plt.close(fig)
    print(f"[post_run] wrote {output_path}")
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--skip-comparator",
        action="store_true",
        help="Skip running the t0124-vs-t0126 comparator.",
    )
    parser.add_argument(
        "--skip-charts",
        action="store_true",
        help="Skip generating the post-run charts.",
    )
    args = parser.parse_args(argv)

    if not args.skip_comparator:
        report = run_comparator(seed=int(args.seed), repo_root=args.repo_root)
        print(f"[post_run] verdict: {report['verdict']}")
        print(f"[post_run] rationale: {report['verdict_rationale']}")

    if not args.skip_charts:
        render_hv_trajectory(seed=int(args.seed))
        render_pareto_front_dsi_vs_atp(seed=int(args.seed))

    return 0


if __name__ == "__main__":
    sys.exit(main())
