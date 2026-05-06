"""Phase C scorecard: score cluster centroids against biological priors.

For each (cluster, prior) pair compute deviation = (centroid_value - mean) / sigma
and assign verdict:
* plausible if |deviation| <= 2
* stretched if 2 < |deviation| <= 5
* exotic if |deviation| > 5

Per cluster, aggregate verdict = worst-case across priors.

Outputs:
* results/data/biological_scorecard.json (per cluster, per prior)
* results/images/biological_plausibility_heatmap.png
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import ParamIndex
from tasks.t0086_robustness_cluster_bio_comparison.code.paths import (
    BIOLOGICAL_PRIORS_JSON,
    BIOLOGICAL_SCORECARD_JSON,
    CLUSTER_CENTROIDS_JSON,
    RESULTS_IMAGES_DIR,
    ensure_directories,
)

PLAUSIBLE_THRESHOLD: float = 2.0
STRETCHED_THRESHOLD: float = 5.0
HEATMAP_PNG: Path = RESULTS_IMAGES_DIR / "biological_plausibility_heatmap.png"


def _verdict(*, deviation_abs: float) -> str:
    if deviation_abs <= PLAUSIBLE_THRESHOLD:
        return "plausible"
    if deviation_abs <= STRETCHED_THRESHOLD:
        return "stretched"
    return "exotic"


def _aggregate(*, verdicts: list[str]) -> str:
    """Worst-case aggregation."""
    if "exotic" in verdicts:
        return "exotic"
    if "stretched" in verdicts:
        return "stretched"
    if len(verdicts) == 0:
        return "no_data"
    return "plausible"


def _centroid_value(*, centroid_unnormalised: list[float], param_index: int) -> float:
    if param_index == -1:
        # Derived: AIS-to-soma Nav ratio.
        ais = centroid_unnormalised[int(ParamIndex.NAV16_AIS_GBAR)]
        soma = centroid_unnormalised[int(ParamIndex.NAV16_SOMA_GBAR)]
        if soma <= 0:
            return float("inf")
        return ais / soma
    return float(centroid_unnormalised[param_index])


def score_clusters() -> dict[str, object]:
    centroids_payload = json.loads(CLUSTER_CENTROIDS_JSON.read_text(encoding="utf-8"))
    priors_payload = json.loads(BIOLOGICAL_PRIORS_JSON.read_text(encoding="utf-8"))
    centroids = centroids_payload["centroids"]
    priors = priors_payload["priors"]

    cluster_scores: list[dict[str, object]] = []
    for centroid in centroids:
        cluster_id = int(centroid["cluster_id"])
        unnorm = list(centroid["centroid_unnormalised"])
        per_prior: list[dict[str, object]] = []
        verdicts: list[str] = []
        for prior in priors:
            value = _centroid_value(
                centroid_unnormalised=unnorm,
                param_index=int(prior["param_index"]),
            )
            mean = float(prior["published_mean"])
            sigma = float(prior["published_sigma"])
            deviation = (value - mean) / sigma if sigma > 0 else float("inf")
            verdict = _verdict(deviation_abs=abs(deviation))
            verdicts.append(verdict)
            per_prior.append(
                {
                    "parameter_name": prior["parameter_name"],
                    "param_index": int(prior["param_index"]),
                    "centroid_value": value,
                    "published_mean": mean,
                    "published_sigma": sigma,
                    "deviation_sigma": float(deviation),
                    "verdict": verdict,
                    "paper_id": prior["paper_id"],
                    "citation": prior["citation"],
                    "units": prior["units"],
                }
            )
        cluster_verdict = _aggregate(verdicts=verdicts)
        cluster_scores.append(
            {
                "cluster_id": cluster_id,
                "n_cells": int(centroid["n_cells"]),
                "cell_ids": list(centroid["cell_ids"]),
                "aggregate_verdict": cluster_verdict,
                "per_prior_scores": per_prior,
            }
        )

    return {
        "n_clusters": len(cluster_scores),
        "n_priors": len(priors),
        "thresholds": {
            "plausible_max_sigma": PLAUSIBLE_THRESHOLD,
            "stretched_max_sigma": STRETCHED_THRESHOLD,
        },
        "clusters": cluster_scores,
    }


def plot_heatmap(*, scorecard: dict[str, object]) -> None:
    clusters = scorecard["clusters"]
    if len(clusters) == 0:
        print("[biological_scorecard] no clusters; skipping heatmap")
        return
    prior_names: list[str] = [
        str(p["parameter_name"])
        for p in clusters[0]["per_prior_scores"]  # type: ignore[index]
    ]
    n_clusters = len(clusters)
    n_priors = len(prior_names)
    deviations = np.zeros((n_clusters, n_priors))
    for i, cluster in enumerate(clusters):
        for j, p in enumerate(cluster["per_prior_scores"]):  # type: ignore[index]
            deviations[i, j] = float(p["deviation_sigma"])

    fig, ax = plt.subplots(figsize=(max(8, n_priors * 1.0), max(4, n_clusters * 0.7)))
    # Cap absolute values at 10 sigma for color scaling.
    capped = np.clip(deviations, -10, 10)
    im = ax.imshow(capped, cmap="RdBu_r", aspect="auto", vmin=-10, vmax=10)
    ax.set_xticks(range(n_priors))
    ax.set_xticklabels(prior_names, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(n_clusters))
    ax.set_yticklabels(
        [
            f"Cluster {c['cluster_id']} (n={c['n_cells']}, {c['aggregate_verdict']})"
            for c in clusters
        ]
    )
    for i in range(n_clusters):
        for j in range(n_priors):
            verdict = str(
                clusters[i]["per_prior_scores"][j]["verdict"]  # type: ignore[index]
            )
            if verdict == "plausible":
                txt = "P"
            elif verdict == "stretched":
                txt = "S"
            else:
                txt = "X"
            ax.text(
                j,
                i,
                f"{txt}\n{deviations[i, j]:+.1f}",
                ha="center",
                va="center",
                fontsize=8,
                color="white" if abs(deviations[i, j]) > 5 else "black",
            )
    ax.set_title("Biological plausibility heatmap (deviation in sigma units)")
    fig.colorbar(im, ax=ax, label="Deviation (sigma)", fraction=0.04)
    fig.tight_layout()
    fig.savefig(HEATMAP_PNG, dpi=200)
    plt.close(fig)
    print(f"[biological_scorecard] wrote {HEATMAP_PNG}")


def main() -> None:
    ensure_directories()
    scorecard = score_clusters()
    BIOLOGICAL_SCORECARD_JSON.write_text(
        json.dumps(scorecard, indent=2),
        encoding="utf-8",
    )
    plot_heatmap(scorecard=scorecard)
    print(
        f"[biological_scorecard] wrote {BIOLOGICAL_SCORECARD_JSON}: "
        f"{scorecard['n_clusters']} clusters scored against {scorecard['n_priors']} priors"
    )


if __name__ == "__main__":
    main()
