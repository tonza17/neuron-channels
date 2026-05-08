"""t0091 biological scorecard: score per-Pareto-cell 68-d vectors against priors.

Adapted from
``tasks/t0088_recluster_marginals_and_vm_motifs/code/biological_scorecard.py``
to score per-cell rather than per-cluster, treating each Pareto cell's 68-d
parameter vector as a pseudo-centroid (n_cells=1).

For each (cell, prior) pair compute deviation = (cell_value - mean) / sigma
and assign verdict:
* plausible if |deviation| <= 2
* stretched if 2 < |deviation| <= 5
* exotic if |deviation| > 5

Per-cell aggregate verdict is the worst-case across the priors.
"""

from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0091_morphology_extended_nsga2_v1.code.constants import ParamIndex
from tasks.t0091_morphology_extended_nsga2_v1.code.paths import (
    BIOLOGICAL_HEATMAP_PNG,
    BIOLOGICAL_PRIORS_68D_JSON,
    BIOLOGICAL_SCORECARD_68D_JSON,
    PARETO_FRONT_JSON,
    ensure_directories,
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
        # Derived: AIS-to-soma Nav ratio.
        ais = vector_68d[int(ParamIndex.NAV16_AIS_GBAR)]
        soma = vector_68d[int(ParamIndex.NAV16_SOMA_GBAR)]
        if soma <= 0:
            return float("inf")
        return ais / soma
    if param_index < 0 or param_index >= len(vector_68d):
        return float("nan")
    return float(vector_68d[param_index])


def score_pareto_cells() -> dict[str, object]:
    pareto_payload = json.loads(PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    priors_payload = json.loads(BIOLOGICAL_PRIORS_68D_JSON.read_text(encoding="utf-8"))
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
                "verdict": cell_verdict,
                "per_prior_scores": per_prior,
            }
        )

    return {
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
            "glycinergic extraclassical pathway). Per REQ-22."
        ),
        "cells": cell_scores,
    }


def plot_heatmap(*, scorecard: dict[str, object]) -> None:
    cells = scorecard["cells"]
    if not isinstance(cells, list) or len(cells) == 0:
        print("[biological_scorecard] no cells; skipping heatmap")
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
    ax.set_title("Per-cell biological plausibility (deviation in sigma)")
    fig.colorbar(im, ax=ax, label="Deviation (sigma)", fraction=0.04)
    fig.tight_layout()
    fig.savefig(BIOLOGICAL_HEATMAP_PNG, dpi=200)
    plt.close(fig)
    print(f"[biological_scorecard] wrote {BIOLOGICAL_HEATMAP_PNG}")


def main() -> None:
    ensure_directories()
    scorecard = score_pareto_cells()
    BIOLOGICAL_SCORECARD_68D_JSON.write_text(
        json.dumps(scorecard, indent=2),
        encoding="utf-8",
    )
    plot_heatmap(scorecard=scorecard)
    print(
        f"[biological_scorecard] wrote {BIOLOGICAL_SCORECARD_68D_JSON}: "
        f"{scorecard['n_cells']} cells x {scorecard['n_priors']} priors"
    )


if __name__ == "__main__":
    main()
