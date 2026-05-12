"""t0099 biological scorecard: per-seed scoring of NSGA-II Pareto cells.

Adapted from the t0091 scorecard. Reads a per-seed Pareto front and the shared
priors file, then writes per-seed verdicts. Worst-case aggregation across the
13 priors (9 electrophys + 4 morphology) is identical to t0091.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code.constants_electrophys import ParamIndex
from tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code.paths import (
    IMAGES_DIR,
    biological_priors_json,
    biological_scorecard_json,
    ensure_directories,
    pareto_front_json,
)

PLAUSIBLE_THRESHOLD_SIGMA: float = 2.0
STRETCHED_THRESHOLD_SIGMA: float = 5.0


def _verdict(*, deviation_abs: float) -> str:
    if deviation_abs <= PLAUSIBLE_THRESHOLD_SIGMA:
        return "plausible"
    if deviation_abs <= STRETCHED_THRESHOLD_SIGMA:
        return "stretched"
    return "exotic"


def _aggregate(*, verdicts: list[str]) -> str:
    """Worst-case aggregation across priors."""
    if "exotic" in verdicts:
        return "exotic"
    if "stretched" in verdicts:
        return "stretched"
    if len(verdicts) == 0:
        return "no_data"
    return "plausible"


def _cell_value(*, vector_68d: list[float], param_index: int) -> float:
    if param_index == -1:
        ais = vector_68d[int(ParamIndex.NAV16_AIS_GBAR)]
        soma = vector_68d[int(ParamIndex.NAV16_SOMA_GBAR)]
        if soma <= 0:
            return float("inf")
        return ais / soma
    if param_index < 0 or param_index >= len(vector_68d):
        return float("nan")
    return float(vector_68d[param_index])


def score_pareto_cells_for_seed(*, seed: int) -> dict[str, object]:
    pareto_payload = json.loads(pareto_front_json(seed=seed).read_text(encoding="utf-8"))
    priors_payload = json.loads(biological_priors_json().read_text(encoding="utf-8"))
    cells_in = pareto_payload["cells"]
    priors = priors_payload["priors"]

    cell_scores: list[dict[str, object]] = []
    for cell_in in cells_in:
        cell_id = cell_in.get("cell_id", cell_in.get("cell_index", -1))
        vector = list(cell_in.get("vector_68d") or cell_in.get("params"))
        per_prior: list[dict[str, object]] = []
        verdicts: list[str] = []
        for prior in priors:
            value = _cell_value(vector_68d=vector, param_index=int(prior["param_index"]))
            mean = float(prior["published_mean"])
            sigma = float(prior["published_sigma"])
            deviation = (value - mean) / sigma if sigma > 0 else float("inf")
            verdict = _verdict(deviation_abs=abs(deviation))
            verdicts.append(verdict)
            per_prior.append(
                {
                    "parameter_name": prior["parameter_name"],
                    "param_index": int(prior["param_index"]),
                    "cell_value": value,
                    "published_mean": mean,
                    "published_sigma": sigma,
                    "deviation_sigma": float(deviation),
                    "verdict": verdict,
                    "paper_id": prior["paper_id"],
                    "citation": prior["citation"],
                    "units": prior["units"],
                }
            )
        cell_verdict = _aggregate(verdicts=verdicts)
        cell_scores.append(
            {
                "cell_id": cell_id,
                "dsi_vector_sum": float(cell_in.get("dsi_vector_sum", 0.0)),
                "pd_rate_hz": float(cell_in.get("pd_rate_hz", 0.0)),
                "robustness": float(cell_in.get("robustness", 0.0)),
                "verdict": cell_verdict,
                "per_prior_scores": per_prior,
            }
        )

    return {
        "seed": seed,
        "n_cells": len(cell_scores),
        "n_priors": len(priors),
        "thresholds": {
            "plausible_max_sigma": PLAUSIBLE_THRESHOLD_SIGMA,
            "stretched_max_sigma": STRETCHED_THRESHOLD_SIGMA,
        },
        "notes": (
            "Per-cell biological plausibility; aggregate verdict is the worst-case "
            "across the 9 electrophys + 4 morphology priors. GABA spatial-gradient "
            "priors apply to classical-RF SAC-mediated DS only (not Riccitelli 2025 "
            "glycinergic extraclassical pathway)."
        ),
        "cells": cell_scores,
    }


def plot_heatmap(*, scorecard: dict[str, object], output_png: Path) -> None:
    cells = scorecard["cells"]
    if not isinstance(cells, list) or len(cells) == 0:
        print(f"[biological_scorecard] no cells for seed {scorecard.get('seed')}; skipping heatmap")
        return
    first_cell = cells[0]
    assert isinstance(first_cell, dict)
    prior_names: list[str] = [str(p["parameter_name"]) for p in first_cell["per_prior_scores"]]
    n_cells = len(cells)
    n_priors = len(prior_names)
    deviations = np.zeros((n_cells, n_priors))
    for i, cell in enumerate(cells):
        assert isinstance(cell, dict)
        for j, p in enumerate(cell["per_prior_scores"]):
            deviations[i, j] = float(p["deviation_sigma"])

    fig, ax = plt.subplots(figsize=(max(8, n_priors * 0.9), max(4, n_cells * 0.4)))
    capped = np.clip(deviations, -10, 10)
    im = ax.imshow(capped, cmap="RdBu_r", aspect="auto", vmin=-10, vmax=10)
    ax.set_xticks(range(n_priors))
    ax.set_xticklabels(prior_names, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(n_cells))
    ax.set_yticklabels(
        [f"Cell {c['cell_id']} ({c['verdict']})" for c in cells],
        fontsize=8,
    )
    seed = scorecard.get("seed")
    ax.set_title(f"Seed {seed} per-cell biological plausibility (deviation in sigma)")
    fig.colorbar(im, ax=ax, label="Deviation (sigma)", fraction=0.04)
    fig.tight_layout()
    fig.savefig(output_png, dpi=200)
    plt.close(fig)
    print(f"[biological_scorecard] wrote {output_png}")


def main_for_seed(*, seed: int) -> dict[str, object]:
    ensure_directories()
    scorecard = score_pareto_cells_for_seed(seed=seed)
    biological_scorecard_json(seed=seed).write_text(
        json.dumps(scorecard, indent=2),
        encoding="utf-8",
    )
    heatmap_png = IMAGES_DIR / f"biological_heatmap_seed{seed}.png"
    plot_heatmap(scorecard=scorecard, output_png=heatmap_png)
    print(
        f"[biological_scorecard] seed={seed} wrote {biological_scorecard_json(seed=seed)}: "
        f"{scorecard['n_cells']} cells x {scorecard['n_priors']} priors"
    )
    return scorecard


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Score per-seed Pareto cells against priors")
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    main_for_seed(seed=int(args.seed))
