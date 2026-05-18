---
spec_version: "2"
answer_id: "t0106-electrophys-clusters-morphology-signature"
answered_by_task: "t0108_t0106_cluster_factor_dsi05_pd10"
date_answered: "2026-05-18"
---

# Electrophys clusters carry only a weak morphology signature

## Question

When t0106 cells with DSI > 0.5 AND PD > 10 Hz are clustered by their 54-d electrophys parameters,
do the clusters carry a distinguishable morphological signature?

## Answer

Only weakly. K-means on the z-scored 54-d electrophys submatrix of the 150-cell strict cohort
produces an unbalanced k=2 split (10 vs 140; silhouette 0.496) that essentially separates a small
low-firing high-DSI outlier group from the bulk. Across 14 morphology parameters, only 3 differ
between the clusters at Bonferroni p < 0.05: mean_branching_angle_deg, branch_length_cv,
ais_length_um. Higher-k partitions degrade silhouette to ~0.13, so no further morphology-relevant
structure exists. The electrophys regime that produces high DSI and high PD is therefore largely
morphology-agnostic within this cohort.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen`
* Task: `t0108_t0106_cluster_factor_dsi05_pd10`
