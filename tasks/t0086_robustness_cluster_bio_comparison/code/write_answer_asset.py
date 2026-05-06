"""Write the cluster-biological-plausibility-attribution answer asset.

Produces:
* assets/answer/cluster-biological-plausibility-attribution/details.json
* assets/answer/cluster-biological-plausibility-attribution/short_answer.md
* assets/answer/cluster-biological-plausibility-attribution/full_answer.md

Depends on results/data/biological_scorecard.json + cluster_centroids.json
+ cell_classification.json being already populated.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from tasks.t0086_robustness_cluster_bio_comparison.code.paths import (
    ANSWER_DIR,
    BIOLOGICAL_SCORECARD_JSON,
    CELL_CLASSIFICATION_JSON,
    CLUSTER_CENTROIDS_JSON,
    ensure_directories,
)

ANSWER_ID: str = "cluster-biological-plausibility-attribution"
TASK_ID: str = "t0086_robustness_cluster_bio_comparison"
DETAILS_JSON: Path = ANSWER_DIR / "details.json"
SHORT_ANSWER_MD: Path = ANSWER_DIR / "short_answer.md"
FULL_ANSWER_MD: Path = ANSWER_DIR / "full_answer.md"
QUESTION: str = (
    "Which clusters of joint-pass cells in t0083's expanded population are biologically "
    "plausible vs novel/unphysical, and which dendritic-spike machinery do the plausible "
    "clusters represent?"
)


def _load_data() -> dict[str, object]:
    return {
        "scorecard": json.loads(BIOLOGICAL_SCORECARD_JSON.read_text(encoding="utf-8")),
        "centroids": json.loads(CLUSTER_CENTROIDS_JSON.read_text(encoding="utf-8")),
        "classification": json.loads(CELL_CLASSIFICATION_JSON.read_text(encoding="utf-8")),
    }


def _write_details(*, confidence: str, today: str) -> None:
    payload = {
        "spec_version": "2",
        "answer_id": ANSWER_ID,
        "question": QUESTION,
        "short_title": "Cluster biological plausibility attribution",
        "short_answer_path": "short_answer.md",
        "full_answer_path": "full_answer.md",
        "categories": [],
        "answer_methods": ["code-experiment", "papers"],
        "source_paper_ids": [],
        "source_urls": [],
        "source_task_ids": [
            "t0024_port_de_rosenroll_2026_dsgc",
            "t0078_bedb_mobo_v2_ais_tiered_ahp",
            "t0080_bedb_mobo_v3_dendritic_spike_nsga2",
            "t0081_bedb_v3_warmstart_nsga2",
            "t0083_bedb_v3_extend_nsga2_gen8plus",
            "t0084_t0081_cell_767_vm_trace_deepdive",
            TASK_ID,
        ],
        "confidence": confidence,
        "created_by_task": TASK_ID,
        "date_created": today,
    }
    DETAILS_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _summarise_clusters(*, scorecard: dict[str, object]) -> str:
    clusters = scorecard["clusters"]  # type: ignore[index]
    if len(clusters) == 0:  # type: ignore[arg-type]
        return "no clusters were produced (insufficient Genuine cells)"
    parts: list[str] = []
    for c in clusters:  # type: ignore[union-attr]
        parts.append(f"Cluster {c['cluster_id']} (n={c['n_cells']}): {c['aggregate_verdict']}")
    return "; ".join(parts)


def _short_answer(*, data: dict[str, object], today: str) -> str:
    classification = data["classification"]
    summary = classification["summary"]  # type: ignore[index]
    n_genuine = int(summary["Genuine"])  # type: ignore[index]
    n_marginal = int(summary["Marginal"])  # type: ignore[index]
    n_stochastic = int(summary["Stochastic"])  # type: ignore[index]
    cluster_summary = _summarise_clusters(scorecard=data["scorecard"])  # type: ignore[arg-type]
    n_clusters = int(data["scorecard"]["n_clusters"])  # type: ignore[index]

    if n_genuine == 0:
        body_p1 = (
            "None of the 20 re-evaluated joint-pass cells passed the joint criterion "
            f"in all five replications. Robustness classification: 0 Genuine, "
            f"{n_marginal} Marginal, {n_stochastic} Stochastic. With zero Genuine "
            "cells the cluster analysis is not informative -- the t0081/t0083 "
            "joint-pass population is essentially stochastic at the chosen "
            "RNG-replication level."
        )
        body_p2 = (
            "The negative finding is itself meaningful: it indicates that t0083's "
            "joint-pass cells were artifacts of single-seed evaluation rather than "
            "stable biological mechanisms, and that the existing pass criterion "
            "(DSI >= 0.4 AND PD >= 10 Hz) is too tight relative to inter-replicate "
            "variance under the v3 substrate."
        )
    else:
        body_p1 = (
            f"Of 20 re-evaluated cells {n_genuine} are Genuine (5/5 reps pass joint "
            f"criterion), {n_marginal} Marginal (3-4/5), {n_stochastic} Stochastic "
            f"(<=2/5). The Genuine cells partition into {n_clusters} cluster(s) at "
            f"k-means best_k. {cluster_summary}."
        )
        body_p2 = (
            "Cluster centroids were scored against eight published priors (Kole 2008, "
            "Werginz 2024, Sivyer 2013, Branco-Hausser 2010, Oesch 2005, Stuart 1999, "
            "Goldfinger 2000, de Rosenroll 2026). See full_answer.md for per-cluster "
            "and per-prior breakdowns."
        )

    return f"""---
spec_version: "2"
answer_id: "{ANSWER_ID}"
answered_by_task: "{TASK_ID}"
date_answered: "{today}"
---
# Cluster Biological Plausibility Attribution

## Question

{QUESTION}

## Answer

{body_p1} {body_p2}

## Sources

* Task: `t0086_robustness_cluster_bio_comparison` (this task; 100-evaluation
  replication study, k-means/hierarchical/UMAP cluster analysis, biological
  scorecard).
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus` (source of the 18-cell Pareto
  front and 14 of the 15 joint-pass cells).
* Task: `t0081_bedb_v3_warmstart_nsga2` (source of cell 767, the original
  joint-pass cell).
* Task: `t0084_t0081_cell_767_vm_trace_deepdive` (cell 767 mechanism
  attribution informing cluster-67 narrative).
"""


def _full_answer(*, data: dict[str, object], today: str, confidence: str) -> str:
    classification = data["classification"]
    summary = classification["summary"]  # type: ignore[index]
    n_genuine = int(summary["Genuine"])  # type: ignore[index]
    n_marginal = int(summary["Marginal"])  # type: ignore[index]
    n_stochastic = int(summary["Stochastic"])  # type: ignore[index]
    scorecard = data["scorecard"]
    n_clusters = int(scorecard["n_clusters"])  # type: ignore[index]

    cluster_block_lines: list[str] = []
    for cluster in scorecard["clusters"]:  # type: ignore[union-attr]
        cluster_block_lines.append(
            f"### Cluster {cluster['cluster_id']} -- {cluster['aggregate_verdict']}"
        )
        cluster_block_lines.append("")
        cluster_block_lines.append(f"Members ({cluster['n_cells']}): {cluster['cell_ids']}.")
        cluster_block_lines.append("")
        cluster_block_lines.append(
            "| Prior | Citation | Centroid | Mean | Sigma | Dev. | Verdict |"
        )
        cluster_block_lines.append(
            "|-------|----------|----------|------|-------|------|---------|"
        )
        for prior in cluster["per_prior_scores"]:  # type: ignore[index]
            cluster_block_lines.append(
                f"| `{prior['parameter_name']}` | {prior['citation']} | "
                f"{prior['centroid_value']:.4g} | {prior['published_mean']:.4g} | "
                f"{prior['published_sigma']:.4g} | {prior['deviation_sigma']:+.2f} | "
                f"{prior['verdict']} |"
            )
        cluster_block_lines.append("")
    cluster_block = (
        "\n".join(cluster_block_lines)
        if n_clusters > 0
        else ("No clusters were produced because there are insufficient Genuine cells.")
    )

    short_answer_block = _short_answer(data=data, today=today)
    short_answer_body = short_answer_block.split("## Answer\n\n", 1)[1].split("\n\n## Sources", 1)[
        0
    ]

    return f"""---
spec_version: "2"
answer_id: "{ANSWER_ID}"
answered_by_task: "{TASK_ID}"
date_answered: "{today}"
confidence: "{confidence}"
---
# Cluster Biological Plausibility Attribution -- Full Answer

## Question

{QUESTION}

## Short Answer

{short_answer_body}

## Research Process

The investigation proceeded in three phases on top of t0083's 18-cell Pareto
front. Phase A re-evaluated 20 cells (15 joint-pass: cell 767 + 14 t0083
joint-pass cells; 5 closest near-pass cells from the t0083 Pareto front
ranked by Euclidean distance to the (DSI=0.4, PD=10 Hz) joint corner) at 24
directions x 30 inner seeds x 5 outer-seed replications using the t0080
`evaluate_parameter_vector` entry point. Each replication monkey-patches the
t0080 module-level `SEED_BASE` constant to one of 5 deterministic seeds drawn
from `np.random.SeedSequence(42).spawn(5)` so that DSI and PD variance across
replications reflect inter-RNG variability rather than parameter changes
(REQ-3, REQ-4, REQ-16). Each cell was classified Genuine (5/5 reps pass),
Marginal (3-4/5), or Stochastic (<=2/5) (REQ-5).

Phase B applied k-means clustering with k=2..6 to the 54-d parameter vectors
of the Genuine cells in min-max normalised space, selecting best_k by
silhouette score. Hierarchical clustering with cosine and euclidean metrics
provided cross-validation; 50-sample bootstrap stability ARI quantified
robustness of the k-means partition (REQ-6, REQ-7, REQ-9, REQ-10). UMAP
(falling back to PCA if umap-learn unavailable) produced a 2-D embedding for
visualisation (REQ-8).

Phase C scored each cluster centroid in unnormalised parameter space against
eight published biological priors (Kole 2008, Werginz 2024, Sivyer 2013,
Branco-Hausser 2010, Oesch 2005, Stuart 1999, Goldfinger 2000, de Rosenroll
2026; REQ-11). Per (cluster, prior) pair, deviation = (centroid - mean)/sigma
with verdict plausible (|deviation| <= 2), stretched (2-5), or exotic (> 5).
Cluster aggregate verdict = worst-case (REQ-12).

## Evidence from Papers

The biological priors database (`code/biological_priors.py`) hard-codes published
measurements with paper_id references so the audit trail back to the corpus
is explicit. Kole 2008 (`10.1038_nn.2153`) and Werginz 2024 supply the AIS
Nav density priors; Oesch 2005 supplies distal Nav1.6; Stuart 1999 and
Goldfinger 2000 supply distal NaP; Sivyer 2013 supplies dendritic NMDA;
Branco-Hausser 2010 supplies the NMDA Mg-block voff; de Rosenroll 2026
supplies the GABA spatial gradient.

## Evidence from Internet Sources

No new internet research was conducted in this task; published values were
sourced from the existing paper corpus inherited from t0024, t0078, and
t0080.

## Evidence from Code or Experiments

The 100-cell-evaluation replication run (Phase A) generated
`results/data/replication_results.json` (one record per cell-eval pair),
classified at `results/data/cell_classification.json`. Phase B clustering
results live in `results/data/clustering_results.json` and centroids in
`results/data/cluster_centroids.json`. Phase C scorecard lives in
`results/data/biological_scorecard.json` with the heatmap at
`results/images/biological_plausibility_heatmap.png`. The cost watchdog
(REQ-X, `code/cost_watchdog.py`) read the actual hourly rate
(\\$0.3474/hr) from `logs/steps/008_setup-machines/machine_log.json`
`selected_offer.price_per_hour` -- this fixes the t0083 \\$0.83 budget overrun
caused by a hard-coded \\$0.2382/hr default.

## Synthesis

Robustness summary: {n_genuine} Genuine, {n_marginal} Marginal, {n_stochastic}
Stochastic of 20 re-evaluated cells. Cluster summary at best_k:

{cluster_block}

## Limitations

* Only 5 outer-seed replications per cell. A 10-replication study would
  distinguish 10/10 from 8-9/10 from <=7/10 with finer granularity but
  would double the wall-clock and \\$ cost.
* Bootstrap subsample size = 80 percent of Genuine cells. With small N this
  produces wide ARI confidence intervals.
* Biological sigma values are conservative best-effort estimates where the
  source paper does not report formal uncertainty. Stretched / exotic
  verdicts may shift if a future task tightens the priors.

## Sources

* Task: `t0024_port_de_rosenroll_2026_dsgc` (de Rosenroll 2026 substrate).
* Task: `t0078_bedb_mobo_v2_ais_tiered_ahp` (AIS-tiered AHP recovery).
* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2` (v3 substrate; 54-d
  parameter space; AIS-to-soma constraint; cost-watchdog pattern).
* Task: `t0081_bedb_v3_warmstart_nsga2` (8-gen warmstart; cell 767).
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus` (gen 8-17 extension; 14 t0083
  joint-pass cells; 18-cell Pareto front; \\$0.83 cost overrun motivating
  REQ-X).
* Task: `t0084_t0081_cell_767_vm_trace_deepdive` (cell 767 mechanism
  attribution).
* Paper: `10.1038_nn.2153` (Kole 2008 AIS Nav density).
* Paper: `werginz_2024` (Werginz 2024 AIS-to-soma ratio).
* Paper: `sivyer_2013` (Sivyer 2013 dendritic NMDA).
* Paper: `branco_hausser_2010` (NMDA Mg-block voff).
* Paper: `oesch_2005` (distal Nav1.6).
* Paper: `stuart_1999` (distal NaP).
* Paper: `goldfinger_2000` (distal NaP cross-reference).
* Paper: `de_rosenroll_2026` (GABA spatial gradient).
"""


def _decide_confidence(*, n_genuine: int, n_clusters: int) -> str:
    if n_genuine == 0:
        return "high"  # negative result is well-supported
    if n_genuine < 5 or n_clusters < 2:
        return "low"
    return "medium"


def main() -> None:
    ensure_directories()
    data = _load_data()
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    classification = data["classification"]
    summary = classification["summary"]  # type: ignore[index]
    n_genuine = int(summary["Genuine"])  # type: ignore[index]
    n_clusters = int(data["scorecard"]["n_clusters"])  # type: ignore[index]
    confidence = _decide_confidence(n_genuine=n_genuine, n_clusters=n_clusters)
    _write_details(confidence=confidence, today=today)
    SHORT_ANSWER_MD.write_text(_short_answer(data=data, today=today), encoding="utf-8")
    FULL_ANSWER_MD.write_text(
        _full_answer(data=data, today=today, confidence=confidence), encoding="utf-8"
    )
    print(
        f"[write_answer_asset] wrote {ANSWER_DIR} (confidence={confidence}, "
        f"n_genuine={n_genuine}, n_clusters={n_clusters})"
    )


if __name__ == "__main__":
    main()
