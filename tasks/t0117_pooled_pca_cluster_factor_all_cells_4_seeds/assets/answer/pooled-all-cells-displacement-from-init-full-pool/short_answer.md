---
spec_version: "2"
answer_id: "pooled-all-cells-displacement-from-init-full-pool"
answered_by_task: "t0117_pooled_pca_cluster_factor_all_cells_4_seeds"
date_answered: "2026-05-22"
---
# Per-seed displacement collapses sharply at the unfiltered pool; relative ordering partially preserved

## Question

How far did NSGA-II travel from gen-0 (generation == 1) in each seed when the full quality range
is admitted (no DSI / PD filter), and is the per-seed displacement pattern observed at the
strict cohort (seed 44 furthest, seed 9354 closest) preserved at the unfiltered pool?

## Answer

Per-seed displacement drops by roughly 5-10x at the unfiltered pool: mean 68-d displacement
collapses from ~60 (all seeds, t0116) to ~9 (all seeds, t0117), and mean PC1+PC2 displacement
from 15.0 / 8.5 / 13.3 / 2.4 (seeds 44 / 77 / 7755 / 9354 at t0116) to 4.9 / 1.5 / 5.7 / 1.6
(t0117). The relative ordering is partially preserved — seeds 44 and 7755 remain the two
furthest from random init at t0117 (4.9 and 5.7 in PC12, top of the table), and seed 9354
remains close to its random init (1.6) — but seed 77 drops from second-furthest to nearly tied
with seed 9354 because the strict cohort retained only the Pareto-front tip of seed 77 (n=10),
while the unfiltered pool admits all 654 of its cells, dominated by lower-quality individuals
near gen-1.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen`
* Task: `t0112_t0106_seed77_replicate`
* Task: `t0114_seed7755_no_autostop`
* Task: `t0115_seed9354_no_autostop`
* Task: `t0116_pooled_pca_cluster_factor_dsi07_pd10`
* Task: `t0117_pooled_pca_cluster_factor_all_cells_4_seeds`
