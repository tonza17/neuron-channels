---
spec_version: "2"
answer_id: "pooled-survivors-basin-connectivity-dsi07-pd10"
answered_by_task: "t0116_pooled_pca_cluster_factor_dsi07_pd10"
date_answered: "2026-05-21"
---
# Pooled DSI>0.7/PD>10 cohort is fragmented into seed-specific sub-basins

## Question

Does the joint-pass cohort (DSI > 0.7 AND PD > 10 Hz) form a single connected manifold in 68-d
across four NSGA-II seeds (44, 77, 7755, 9354), or do the seeds occupy seed-specific sub-basins?

## Answer

The four-seed pool occupies seed-specific sub-basins, not one connected manifold. KMeans (k=3) on
the standardised 54-d electrophys subspace produces an almost-perfect seed partition (NMI=0.929,
chi-square p<1e-300): cluster 0 = 63/67 seed 9354, cluster 1 = 673/678 seed 7755, cluster 2 =
121/124 seed 44 (seed 77 contributes 10 scattered cells across all clusters). The 14-d morphology
partition is similarly seed-aligned (NMI=0.889). In the combined 68-d PCA scatter the four seed
colours occupy visibly disjoint regions of the PC1-PC2 plane, so the cross-seed overlap implied by a
single connected basin is not observed at the DSI > 0.7 cut.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen`
* Task: `t0112_t0106_seed77_replicate`
* Task: `t0114_seed7755_no_autostop`
* Task: `t0115_seed9354_no_autostop`
* Task: `t0116_pooled_pca_cluster_factor_dsi07_pd10`
