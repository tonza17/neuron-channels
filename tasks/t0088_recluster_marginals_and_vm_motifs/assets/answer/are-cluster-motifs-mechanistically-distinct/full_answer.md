---
spec_version: "2"
answer_id: "are-cluster-motifs-mechanistically-distinct"
answered_by_task: "t0088_recluster_marginals_and_vm_motifs"
date_answered: "2026-05-06"
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

The 13-cell re-cluster produces **4 clusters at best_k = 4** (KMeans + silhouette selection), and
the per-cluster Vm-trace deep-dive at 16 directions yields the verdict
**shared_mechanism_different_scale**. Unique dominant mechanisms across clusters: **nap**.

## Research Process

This answer is produced by the t0088 task in three sequential phases on local CPU only ($0 cost):

1. **Phase A -- Re-cluster 13 cells.** Loaded the 6 Genuine + 7 Marginal cells from t0086's
   `cell_classification.json` (13 cells: 767, 1304, 1379, 1504, 1517, 1559, 1604, 1624, 1634, 1639,
   1663, 1677, 1721). Loaded their 54-d natural-unit parameter vectors from t0083's
   `all_evaluations.json`. Re-ran KMeans for k=2..6 (silhouette + BIC selection); ran hierarchical
   clustering with cosine + euclidean metrics; plotted UMAP / PCA; computed per-cluster centroids in
   normalised + unnormalised space; ran 50-sample bootstrap stability ARI = 0.583 +/- 0.226. Picked
   the cell minimising 54-d Euclidean distance to each cluster centroid as the cluster
   representative.
2. **Phase B -- Per-cluster Vm-trace deep-dive at 16 directions.** For each representative cell, ran
   16 NEURON simulations at 22.5-deg spacing recording per-segment Vm at proximal soma /
   mid-dendrite / distal-dendrite / AIS, per-synapse NMDA conductance, and per-segment Nav1.6 / NaP
   currents at the distal dendrite. Computed PD (0 deg) - ND (180 deg) integrated current difference
   over the response window [200, 1200] ms for each channel, then converted to fractional
   contributions (matching t0084's `attribution_metric.py`).
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

Phase A produced **best_k = 4** clusters from the 13-cell pool. Bootstrap stability ARI = 0.583 +/-
0.226 across 50 bootstrap samples (subsample fraction 0.8). KMeans / hierarchical-cosine /
hierarchical-euclidean ARI cross-validation reported in `recluster_assignments.json`.

Per-cluster representative cells selected as the cell minimising 54-d Euclidean distance to the
cluster centroid; deterministic tiebreak by smaller cell_id.

### Per-cluster fractional channel attribution at 16 directions

| Cluster | Rep cell | NMDA frac | Nav1.6 frac | NaP frac | Dominant |
| --- | --- | --- | --- | --- | --- |
| 0 | 1604 | 0.000 | 0.012 | 0.988 | nap |
| 1 | 1634 | 0.000 | 0.126 | 0.874 | nap |
| 2 | 767 | 0.000 | 0.125 | 0.875 | nap |
| 3 | 1639 | 0.000 | 0.003 | 0.997 | nap |

### Per-cluster narrative

* Cluster 0 (representative cell 1604): frac NMDA = 0.000, frac Nav1.6 = 0.012, frac NaP = 0.988;
  dominant = nap.
* Cluster 1 (representative cell 1634): frac NMDA = 0.000, frac Nav1.6 = 0.126, frac NaP = 0.874;
  dominant = nap.
* Cluster 2 (representative cell 767): frac NMDA = 0.000, frac Nav1.6 = 0.125, frac NaP = 0.875;
  dominant = nap.
* Cluster 3 (representative cell 1639): frac NMDA = 0.000, frac Nav1.6 = 0.003, frac NaP = 0.997;
  dominant = nap.

### Biological scorecard summary

All 4 clusters scored against 9 published priors (plausible <= 2 sigma; stretched 2-5 sigma; exotic
\> 5 sigma).
* **Cluster 0 (n=5, cells 1379, 1517, 1559, 1604, 1721): exotic**.
  * gnmda_dend_sivyer2013: +0.00487 uS (+95.4 sigma vs Sivyer 2013)
  * nap_dend_distal_stuart1999: +0.00242 S/cm^2 (+9.6 sigma vs Stuart 1999 / Goldfinger 2000)
  * rho0_gaba_de_rosenroll_2026: +3.7 dimensionless (+5.4 sigma vs de Rosenroll 2026)
* **Cluster 1 (n=4, cells 1304, 1504, 1624, 1634): exotic**.
  * gnmda_dend_sivyer2013: +0.00442 uS (+86.4 sigma vs Sivyer 2013)
  * nap_dend_distal_stuart1999: +0.00723 S/cm^2 (+33.6 sigma vs Stuart 1999 / Goldfinger 2000)
  * ais_to_soma_nav_ratio_werginz2024: +116 dimensionless (+32.9 sigma vs Werginz 2024)
* **Cluster 2 (n=2, cells 767, 1677): exotic**.
  * gnmda_dend_sivyer2013: +0.00454 uS (+88.8 sigma vs Sivyer 2013)
  * lambda_gaba_um_de_rosenroll_2026: +348 micrometers (+8.9 sigma vs de Rosenroll 2026)
  * nap_dend_distal_stuart1999: +0.00222 S/cm^2 (+8.6 sigma vs Stuart 1999 / Goldfinger 2000)
* **Cluster 3 (n=2, cells 1639, 1663): exotic**.
  * gnmda_dend_sivyer2013: +0.00588 uS (+115.6 sigma vs Sivyer 2013)
  * nap_dend_distal_stuart1999: +0.00441 S/cm^2 (+19.5 sigma vs Stuart 1999 / Goldfinger 2000)
  * rho0_gaba_de_rosenroll_2026: +4.73 dimensionless (+7.5 sigma vs de Rosenroll 2026)

## Synthesis

All clusters share the same dominant mechanism in PD-minus-ND attribution; they differ in parameter
scale (parameter-vector position in 54-d space) but not in which channel drives the PD response.
verdict = shared_mechanism_different_scale.

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
  reveal. A multi-replicate per-direction extension (e.g., 5 inner reps per direction) would reduce
  noise but cost ~5x wall-clock; deferred to a follow-up.
* **Representative-cell choice may not generalise**: the cluster representative is the cell closest
  to the centroid in 54-d Euclidean distance. Within-cluster mechanism heterogeneity (if any) is not
  captured by a single representative per cluster.
* **Mechanism attribution is PD-minus-ND only**: orthogonal directions (90 deg, 270 deg) and
  diagonal directions (45 deg etc.) are recorded but not folded into the attribution score. A full
  polar-attribution decomposition (per-direction fractional contributions integrated against the
  direction-tuning curve) would extract more information from the 16-direction recordings.
* **GABA contribution not in attribution**: GABA inhibition is part of the de Rosenroll 2026 v3
  substrate and shapes the PD-vs-ND asymmetry, but the attribution metric only decomposes NMDA /
  Nav1.6 / NaP. GABA's contribution is implicitly visible in the Vm traces but not in the fractional
  table.
* **Cluster instability with n=13 cells**: 13 cells in 54-d space is a small sample for KMeans /
  silhouette / BIC; bootstrap ARI = 0.583 indicates moderate stability. With more cells (e.g.,
  S-0086-04's 10-rep extension would not add cells, but S-0086-01's NSGA-II re-run with tightened
  NMDA bounds may), the cluster structure could differ.

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
