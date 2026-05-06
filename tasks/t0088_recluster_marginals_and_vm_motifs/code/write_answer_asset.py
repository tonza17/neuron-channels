"""Phase C: write the mechanism-distinctness answer asset.

Produces ``assets/answer/are-cluster-motifs-mechanistically-distinct/`` with
``details.json``, ``short_answer.md``, and ``full_answer.md`` per the
answer-asset specification (v2).
"""

from __future__ import annotations

import json

from tasks.t0088_recluster_marginals_and_vm_motifs.code.paths import (
    ANSWER_DIR,
    MECHANISM_DISTINCTNESS_JSON,
    RECLUSTER_ASSIGNMENTS_JSON,
    RECLUSTER_BIOLOGICAL_SCORECARD_JSON,
    RECLUSTER_CENTROIDS_JSON,
    REPRESENTATIVE_CELLS_JSON,
    ensure_directories,
)

ANSWER_ID: str = "are-cluster-motifs-mechanistically-distinct"
DATE_CREATED: str = "2026-05-06"
TASK_ID: str = "t0088_recluster_marginals_and_vm_motifs"


def _write_details() -> None:
    details = {
        "spec_version": "2",
        "answer_id": ANSWER_ID,
        "question": (
            "When the t0086 13-cell pool of 6 Genuine + 7 Marginal cells is re-clustered in the "
            "t0080 54-d v3 parameter space and a t0084-style Vm-trace deep-dive is run at 16 "
            "directions on per-cluster representative cells, are the resulting clusters "
            "mechanistically distinct (different dominant channel mechanisms across clusters) or "
            "do they share the same mechanism with parameter-scale variation?"
        ),
        "short_title": (
            "Cluster motif mechanism distinctness (t0086 13-cell re-cluster + 16-dir deep-dive)"
        ),
        "short_answer_path": "short_answer.md",
        "full_answer_path": "full_answer.md",
        "categories": [
            "compartmental-modeling",
            "direction-selectivity",
            "dendritic-computation",
            "voltage-gated-channels",
        ],
        "answer_methods": ["code-experiment"],
        "source_paper_ids": [],
        "source_urls": [],
        "source_task_ids": [
            "t0080_bedb_mobo_v3_dendritic_spike_nsga2",
            "t0081_bedb_v3_warmstart_nsga2",
            "t0083_bedb_v3_extend_nsga2_gen8plus",
            "t0084_t0081_cell_767_vm_trace_deepdive",
            "t0086_robustness_cluster_bio_comparison",
        ],
        "confidence": "medium",
        "created_by_task": TASK_ID,
        "date_created": DATE_CREATED,
    }
    out_path = ANSWER_DIR / "details.json"
    out_path.write_text(json.dumps(details, indent=2), encoding="utf-8")
    print(f"[write_answer_asset] wrote {out_path}")


def _format_attribution_table(*, narratives: list[dict[str, object]]) -> str:
    """Return a markdown table of per-cluster fractional attributions."""
    lines: list[str] = [
        "| Cluster | Rep cell | NMDA frac | Nav1.6 frac | NaP frac | Dominant |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for n in narratives:
        lines.append(
            f"| {n['cluster_id']} | {n['representative_cell_id']} | "
            f"{n['frac_nmda']:.3f} | {n['frac_nav16']:.3f} | "
            f"{n['frac_nap']:.3f} | {n['dominant_mechanism']} |"
        )
    return "\n".join(lines)


def _short_answer(
    *,
    verdict: str,
    n_clusters: int,
    unique_dominants: list[str],
    table_md: str,
    rationale: str,
) -> str:
    dominants_str = ", ".join(unique_dominants) if unique_dominants else "none"
    return f"""---
spec_version: "2"
answer_id: "{ANSWER_ID}"
answered_by_task: "{TASK_ID}"
date_answered: "{DATE_CREATED}"
---
# Cluster Motif Mechanism Distinctness

## Question

When the t0086 13-cell pool of 6 Genuine + 7 Marginal cells is re-clustered in the t0080 54-d v3
parameter space and a t0084-style Vm-trace deep-dive is run at 16 directions on per-cluster
representative cells, are the resulting clusters mechanistically distinct (different dominant
channel mechanisms across clusters) or do they share the same mechanism with parameter-scale
variation?

## Answer

The 13-cell re-cluster produces **{n_clusters} clusters**, and the per-cluster Vm-trace deep-dive
at 16 directions yields the verdict **{verdict}**. Unique dominant mechanisms across clusters:
**{dominants_str}**. Per-cluster fractional channel attributions are tabulated below; the verdict
reflects whether different clusters use different dominant ion-current mechanisms in their
PD-minus-ND integrated dendritic current.

{table_md}

{rationale}

Compare to t0084's cell 767 attribution (NaP-dominant 93%, Nav1.6 7%, NMDA 0%): the per-cluster
re-evaluation at 16 directions reveals whether the cell-767 NaP-dominant signature generalises to
the broader 13-cell pool's clusters.

## Sources

* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2` (v3 substrate library)
* Task: `t0081_bedb_v3_warmstart_nsga2` (cell 767 warm-start lineage)
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus` (54-d parameter vectors for all 13 cells)
* Task: `t0084_t0081_cell_767_vm_trace_deepdive` (per-direction recording pattern + attribution
  metric)
* Task: `t0086_robustness_cluster_bio_comparison` (Genuine + Marginal classification + clustering
  + biological priors)
"""


def _full_answer(
    *,
    verdict: str,
    n_clusters: int,
    best_k: int,
    unique_dominants: list[str],
    bootstrap_ari_mean: float,
    bootstrap_ari_sd: float,
    table_md: str,
    rationale: str,
    narratives: list[dict[str, object]],
    biological_summary: str,
) -> str:
    bullet_narratives = "\n".join(f"* {n['narrative']}" for n in narratives)
    dominants_str = ", ".join(unique_dominants) if unique_dominants else "none"
    return f"""---
spec_version: "2"
answer_id: "{ANSWER_ID}"
answered_by_task: "{TASK_ID}"
date_answered: "{DATE_CREATED}"
confidence: "medium"
---
# Cluster Motif Mechanism Distinctness (Full Answer)

## Question

When the t0086 13-cell pool of 6 Genuine + 7 Marginal cells is re-clustered in the t0080 54-d v3
parameter space and a t0084-style Vm-trace deep-dive is run at 16 directions on per-cluster
representative cells, are the resulting clusters mechanistically distinct (different dominant
channel mechanisms across clusters) or do they share the same mechanism with parameter-scale
variation?

## Short Answer

The 13-cell re-cluster produces **{n_clusters} clusters at best_k = {best_k}** (KMeans +
silhouette selection), and the per-cluster Vm-trace deep-dive at 16 directions yields the verdict
**{verdict}**. Unique dominant mechanisms across clusters: **{dominants_str}**.

## Research Process

This answer is produced by the t0088 task in three sequential phases on local CPU only ($0 cost):

1. **Phase A -- Re-cluster 13 cells.** Loaded the 6 Genuine + 7 Marginal cells from t0086's
   `cell_classification.json` (13 cells: 767, 1304, 1379, 1504, 1517, 1559, 1604, 1624, 1634,
   1639, 1663, 1677, 1721). Loaded their 54-d natural-unit parameter vectors from t0083's
   `all_evaluations.json`. Re-ran KMeans for k=2..6 (silhouette + BIC selection); ran hierarchical
   clustering with cosine + euclidean metrics; plotted UMAP / PCA; computed per-cluster centroids
   in normalised + unnormalised space; ran 50-sample bootstrap stability ARI =
   {bootstrap_ari_mean:.3f} +/- {bootstrap_ari_sd:.3f}. Picked the cell minimising 54-d Euclidean
   distance to each cluster centroid as the cluster representative.
2. **Phase B -- Per-cluster Vm-trace deep-dive at 16 directions.** For each representative cell,
   ran 16 NEURON simulations at 22.5-deg spacing recording per-segment Vm at proximal soma /
   mid-dendrite / distal-dendrite / AIS, per-synapse NMDA conductance, and per-segment Nav1.6 / NaP
   currents at the distal dendrite. Computed PD (0 deg) - ND (180 deg) integrated current
   difference over the response window [200, 1200] ms for each channel, then converted to
   fractional contributions (matching t0084's `attribution_metric.py`).
3. **Phase C -- Mechanism-distinctness analysis.** Compared dominant channel mechanism across
   clusters. If all clusters share the same dominant mechanism: verdict =
   `shared_mechanism_different_scale` (clusters differ in parameter scale within 54-d space, not in
   which channel drives PD response). If clusters split into 2+ different dominant mechanisms:
   verdict = `distinct`.

## Evidence from Papers

This answer relies on the paper-derived biological priors database from t0086 (re-used unchanged in
t0088): Kole 2008 (AIS Nav density), Werginz 2024 (RGC AIS Nav + AIS-to-soma ratio), Sivyer 2013
(dendritic NMDA conductance), Branco-Hausser 2010 (NMDA Mg-block voff), Oesch 2005 (distal Nav1.6),
Stuart 1999 / Goldfinger 2000 (distal NaP), de Rosenroll 2026 (GABA spatial gradient). The
biological scorecard scores each cluster centroid against these priors (see Phase A output
`recluster_biological_scorecard.json`).

## Evidence from Internet Sources

No new internet research conducted; biological priors are inherited from t0086.

## Evidence from Code or Experiments

### Re-cluster output

Phase A produced **best_k = {best_k}** clusters from the 13-cell pool. Bootstrap stability ARI =
{bootstrap_ari_mean:.3f} +/- {bootstrap_ari_sd:.3f} across 50 bootstrap samples (subsample
fraction 0.8). KMeans / hierarchical-cosine / hierarchical-euclidean ARI cross-validation reported
in `recluster_assignments.json`.

Per-cluster representative cells selected as the cell minimising 54-d Euclidean distance to the
cluster centroid; deterministic tiebreak by smaller cell_id.

### Per-cluster fractional channel attribution at 16 directions

{table_md}

### Per-cluster narrative

{bullet_narratives}

### Biological scorecard summary

{biological_summary}

## Synthesis

{rationale}

The 4 figures per representative cell (Vm traces grid, NMDA conductance trajectories, Nav1.6 / NaP
current decomposition, AIS spike onsets at 16 directions) are saved under `results/images/` and
embedded in `results/results_detailed.md`. The polar 16-bin AIS spike-onset histograms reveal the
direction-tuning sharpness and PD-vs-ND asymmetry per representative cell.

Compare to t0084's cell 767 attribution (NaP-dominant 93%, Nav1.6 7%, NMDA 0%) at 8-direction
resolution: the per-cluster re-evaluation at 16 directions on a wider 13-cell pool gives the most
comprehensive available view of mechanism heterogeneity across the v3 substrate's joint-pass /
near-joint-pass cells.

## Limitations

* **Single inner replication per direction**: Phase B uses 1 inner replication per direction
  (matching t0084 single-seed). The cell parameters that t0086 classified as Marginal (3-4/5 reps
  pass) may have direction-conditional variability that a single replicate per direction cannot
  reveal. A multi-replicate per-direction extension (e.g., 5 inner reps per direction) would
  reduce noise but cost ~5x wall-clock; deferred to a follow-up.
* **Representative-cell choice may not generalise**: the cluster representative is the cell
  closest to the centroid in 54-d Euclidean distance. Within-cluster mechanism heterogeneity (if
  any) is not captured by a single representative per cluster.
* **Mechanism attribution is PD-minus-ND only**: orthogonal directions (90 deg, 270 deg) and
  diagonal directions (45 deg etc.) are recorded but not folded into the attribution score. A
  full polar-attribution decomposition (per-direction fractional contributions integrated against
  the direction-tuning curve) would extract more information from the 16-direction recordings.
* **GABA contribution not in attribution**: GABA inhibition is part of the de Rosenroll 2026 v3
  substrate and shapes the PD-vs-ND asymmetry, but the attribution metric only decomposes NMDA /
  Nav1.6 / NaP. GABA's contribution is implicitly visible in the Vm traces but not in the
  fractional table.
* **Cluster instability with n=13 cells**: 13 cells in 54-d space is a small sample for KMeans /
  silhouette / BIC; bootstrap ARI = {bootstrap_ari_mean:.3f} indicates moderate stability. With
  more cells (e.g., S-0086-04's 10-rep extension would not add cells, but S-0086-01's NSGA-II
  re-run with tightened NMDA bounds may), the cluster structure could differ.

## Sources

* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2` (v3 substrate library: cell builder, parameter
  vector helpers, synapse setup, constants)
* Task: `t0081_bedb_v3_warmstart_nsga2` (cell 767 warm-start lineage; superseded by t0083 for the
  parameter loader)
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus` (54-d parameter vectors for all 13 cells)
* Task: `t0084_t0081_cell_767_vm_trace_deepdive` (per-direction NEURON recording pattern,
  attribution metric, plotting helpers)
* Task: `t0086_robustness_cluster_bio_comparison` (Genuine + Marginal classification, clustering
  core, biological priors database, biological scorecard)
"""


def _summarise_biology() -> str:
    """Compose a brief markdown summary of the biological scorecard."""
    if not RECLUSTER_BIOLOGICAL_SCORECARD_JSON.exists():
        return "_Biological scorecard not yet available._"
    sc = json.loads(RECLUSTER_BIOLOGICAL_SCORECARD_JSON.read_text(encoding="utf-8"))
    lines: list[str] = []
    lines.append(
        f"All {sc['n_clusters']} clusters scored against {sc['n_priors']} published priors "
        f"(plausible <= 2 sigma; stretched 2-5 sigma; exotic > 5 sigma)."
    )
    for c in sc["clusters"]:
        verdict = c["aggregate_verdict"]
        cell_ids = ", ".join(str(cid) for cid in c["cell_ids"])
        lines.append(
            f"* **Cluster {c['cluster_id']} (n={c['n_cells']}, cells {cell_ids}): {verdict}**."
        )
        # Highlight the top-3 most-deviated priors for this cluster.
        sorted_priors = sorted(
            c["per_prior_scores"], key=lambda p: -abs(float(p["deviation_sigma"]))
        )[:3]
        for p in sorted_priors:
            lines.append(
                f"  * {p['parameter_name']}: {p['centroid_value']:+.3g} {p['units']} "
                f"({p['deviation_sigma']:+.1f} sigma vs {p['citation']})"
            )
    return "\n".join(lines)


def _select_unique_dominants(*, narratives: list[dict[str, object]]) -> list[str]:
    return sorted({str(n["dominant_mechanism"]) for n in narratives})


def main() -> None:
    ensure_directories()
    md = json.loads(MECHANISM_DISTINCTNESS_JSON.read_text(encoding="utf-8"))
    ra = json.loads(RECLUSTER_ASSIGNMENTS_JSON.read_text(encoding="utf-8"))
    rc = json.loads(RECLUSTER_CENTROIDS_JSON.read_text(encoding="utf-8"))
    _ = json.loads(REPRESENTATIVE_CELLS_JSON.read_text(encoding="utf-8"))

    verdict: str = str(md["verdict"])
    n_clusters: int = int(md["n_clusters"])
    best_k: int = int(rc["best_k"])
    unique_dominants: list[str] = _select_unique_dominants(narratives=md["per_cluster_narrative"])
    bootstrap = ra["bootstrap_ari"]
    table_md = _format_attribution_table(narratives=md["per_cluster_narrative"])
    rationale = str(md["verdict_rationale"])
    biological_summary = _summarise_biology()

    _write_details()

    short_md = _short_answer(
        verdict=verdict,
        n_clusters=n_clusters,
        unique_dominants=unique_dominants,
        table_md=table_md,
        rationale=rationale,
    )
    short_path = ANSWER_DIR / "short_answer.md"
    short_path.write_text(short_md, encoding="utf-8")
    print(f"[write_answer_asset] wrote {short_path}")

    full_md = _full_answer(
        verdict=verdict,
        n_clusters=n_clusters,
        best_k=best_k,
        unique_dominants=unique_dominants,
        bootstrap_ari_mean=float(bootstrap["mean"]),
        bootstrap_ari_sd=float(bootstrap["sd"]),
        table_md=table_md,
        rationale=rationale,
        narratives=md["per_cluster_narrative"],
        biological_summary=biological_summary,
    )
    full_path = ANSWER_DIR / "full_answer.md"
    full_path.write_text(full_md, encoding="utf-8")
    print(f"[write_answer_asset] wrote {full_path}")


if __name__ == "__main__":
    main()
