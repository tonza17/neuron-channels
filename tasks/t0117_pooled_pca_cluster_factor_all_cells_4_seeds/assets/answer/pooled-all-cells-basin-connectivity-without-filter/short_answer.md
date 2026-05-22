---
spec_version: "2"
answer_id: "pooled-all-cells-basin-connectivity-without-filter"
answered_by_task: "t0117_pooled_pca_cluster_factor_all_cells_4_seeds"
date_answered: "2026-05-22"
---
# Unfiltered 4-seed pool partially reconnects across seeds (NMI drops from 0.93 to 0.56)

## Question

Does the unfiltered pool (every NSGA-II evaluation, no DSI/PD cohort filter) form a single
connected manifold across seeds 44, 77, 7755, and 9354, or does the seed-specific basin pattern
observed at the strict cohort (t0116) persist when low-DSI / low-PD cells are also admitted?

## Answer

The seed-specific basin pattern partially dissolves once the cohort filter is removed: the pool
reconnects across seeds but does not form a single connected manifold. Electrophys KMeans NMI vs
seed drops from 0.929 (t0116, strict cohort) to 0.562 (t0117, no filter, n=4431 cells, k=4), and
morphology NMI drops from 0.889 to 0.313 — the morphology subspace shows much stronger
reconnection than the electrophys subspace. Even at the unfiltered pool both partitions remain
significantly seed-aligned (chi-square p<<0.001), so seed effects are detectable but no longer
dominant.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen`
* Task: `t0112_t0106_seed77_replicate`
* Task: `t0114_seed7755_no_autostop`
* Task: `t0115_seed9354_no_autostop`
* Task: `t0116_pooled_pca_cluster_factor_dsi07_pd10`
* Task: `t0117_pooled_pca_cluster_factor_all_cells_4_seeds`
