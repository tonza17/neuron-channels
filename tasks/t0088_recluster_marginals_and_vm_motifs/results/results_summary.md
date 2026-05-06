---
spec_version: "2"
task_id: "t0088_recluster_marginals_and_vm_motifs"
date_completed: "2026-05-06"
---
# Results Summary -- t0088_recluster_marginals_and_vm_motifs

## Summary

Re-clustered the 13-cell pool of 6 Genuine + 7 Marginal cells from t0086 in the t0080 54-d v3
parameter space; KMeans + silhouette selected **best_k = 4 clusters**. Ran a t0084-style Vm-trace
deep-dive at 16 directions on the 4 representative cells (1604, 1634, 767, 1639) on local CPU, all
64 simulations stable. **Mechanism-distinctness verdict = `shared_mechanism_different_scale`**: all
4 cluster representatives are NaP-dominant in PD-minus-ND attribution (frac NaP 0.874-0.997, frac
Nav1.6 0.003-0.126, frac NMDA = 0.000); clusters differ in parameter scale within 54-d space but not
in which channel drives the PD response. This extends t0084's NaP-dominant cell 767 finding from a
single cell at 8 directions to four representative cells at 16 directions and confirms the v3
substrate's joint-pass / near-joint-pass cells systematically rely on NaP-driven sustained dendritic
depolarisation. All 4 clusters classified exotic by the biological scorecard (extending t0086's
exotic-NMDA verdict to the 13-cell pool).

## Metrics

* **Best k = 4** by silhouette (score 0.164, beat k = 2 at 0.163, k = 5 at 0.160, k = 3 at 0.111).
  Bootstrap stability ARI = **0.583 +/- 0.226** across 50 bootstrap samples (subsample 0.8) --
  moderate stability given small 13-cell pool.

* **Cluster membership at k = 4**:
  * Cluster 0 (n = 5): cells 1379, 1517, 1559, 1604, 1721 (mix: 1 Genuine + 4 Marginal).
    Representative: **cell 1604** (Genuine).
  * Cluster 1 (n = 4): cells 1304, 1504, 1624, 1634 (mix: 1 Genuine + 3 Marginal). Representative:
    **cell 1634** (Genuine).
  * Cluster 2 (n = 2): cells 767, 1677 (mix: 1 Genuine + 1 Marginal). Representative: **cell 767**
    (Marginal).
  * Cluster 3 (n = 2): cells 1639, 1663 (both Genuine). Representative: **cell 1639** (Genuine).

* **Cross-method ARI**: KMeans vs hierarchical-cosine = 0.799; KMeans vs hierarchical-euclidean =
  0.799 (both with average linkage). Cluster structure consistent across methods.

* **All 4 clusters classified exotic** by biological scorecard (worst-case across 9 priors). The two
  dominant exotic priors are gnmda_dend (Sivyer 2013, deviation +85 to +116 sigma across clusters)
  and nap_dend_distal (Stuart 1999, deviation +9.6 to +33.6 sigma).

* **Per-representative fractional channel attribution** at 16 directions (PD = 0 deg vs ND = 180
  deg, response window [200, 1200] ms):

| Cluster | Rep cell | NMDA frac | Nav1.6 frac | NaP frac | Dominant |
| --- | --- | --- | --- | --- | --- |
| 0 | 1604 | 0.000 | 0.012 | **0.988** | **nap** |
| 1 | 1634 | 0.000 | 0.126 | **0.874** | **nap** |
| 2 | 767 | 0.000 | 0.125 | **0.875** | **nap** |
| 3 | 1639 | 0.000 | 0.003 | **0.997** | **nap** |
* **Verdict: `shared_mechanism_different_scale`**. Compare to t0084's cell 767 attribution at 8
  directions (NaP 93%, Nav1.6 7%, NMDA 0%): the 16-direction re-evaluation here gives cell 767 NaP
  87.5% / Nav1.6 12.5%, consistent within angular-resolution noise, and confirms the NaP-dominant
  signature is shared across all 4 clusters.

* **Wall-clock**: Phase A ~10 min; Phase B ~50 min (50 NEURON sims at ~60 s each + warm-up); Phase C
  ~5 min. Total ~65 min local CPU. **Cost $0** (local-CPU only).

## Verification

* `verify_research_code`: PASSED (0 errors).
* `verify_plan`: PASSED (0 errors, 3 acceptable warnings).
* `verify_logs`: PASSED (0 errors, expected warnings to be cleared by capture_task_sessions).
* `verify_task_file`, `verify_task_dependencies`, `verify_task_folder`: PASSED.
