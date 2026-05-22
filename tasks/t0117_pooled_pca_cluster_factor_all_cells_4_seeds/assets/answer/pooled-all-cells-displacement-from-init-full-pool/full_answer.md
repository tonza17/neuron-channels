---
spec_version: "2"
answer_id: "pooled-all-cells-displacement-from-init-full-pool"
answered_by_task: "t0117_pooled_pca_cluster_factor_all_cells_4_seeds"
date_answered: "2026-05-22"
confidence: "high"
---
# Per-seed displacement collapses sharply at the unfiltered pool; relative ordering partially preserved

## Question

How far did NSGA-II travel from gen-0 (generation == 1) in each seed when the full quality range
is admitted (no DSI / PD filter), and is the per-seed displacement pattern observed at the
strict cohort (seed 44 furthest, seed 9354 closest) preserved at the unfiltered pool?

## Short Answer

Per-seed displacement drops by roughly 5-10x at the unfiltered pool: mean 68-d displacement
collapses from ~60 (all seeds, t0116) to ~9 (all seeds, t0117), and mean PC1+PC2 displacement
from 15.0 / 8.5 / 13.3 / 2.4 (seeds 44 / 77 / 7755 / 9354 at t0116) to 4.9 / 1.5 / 5.7 / 1.6
(t0117). The relative ordering is partially preserved — seeds 44 and 7755 remain the two
furthest from random init at t0117 (4.9 and 5.7 in PC12, top of the table), and seed 9354
remains close to its random init (1.6) — but seed 77 drops from second-furthest to nearly tied
with seed 9354 because the strict cohort retained only the Pareto-front tip of seed 77 (n=10),
while the unfiltered pool admits all 654 of its cells, dominated by lower-quality individuals
near gen-1.

## Research Process

The displacement-from-init computation reuses t0116's exact procedure with one upstream change
(no cohort filter applied during pool load):

1. Load the unfiltered pool (n=4431; `code/load_pooled_cells.py`).
2. Load the gen-0 random init from each seed (`code/load_pooled_gen0.py`); exactly 96 cells per
   seed, totalling 384 cells.
3. Fit a single union-pool 68-d z-score standardiser on the 4431-cell pool
   (`code/fit_standardiser.py`).
4. Fit the combined 68-d PCA on the standardised pool (`code/pooled_pca_with_overlay.py`).
5. Project both the pool and the gen-0 cells onto the same combined 68-d PC1+PC2 plane.
6. For each seed, compute the per-cell Euclidean displacement from the seed's gen-0 centroid
   in (a) PC1+PC2 space and (b) the full 68-d z-scored space. Report mean and 95th percentile
   of these per-cell displacements.
7. Persist as `results/data/gen0_displacement.csv`.
8. Compare directly against t0116's `results/data/gen0_displacement.csv` via
   `code/methodology_and_comparison.py` -> `results/data/t0116_comparison.csv`.

## Evidence from Papers

No paper-based evidence was used.

## Evidence from Internet Sources

No external internet sources were used.

## Evidence from Code or Experiments

Per-seed displacement table at t0117 (`results/data/gen0_displacement.csv`):

| seed | mean_disp_pc12 | mean_disp_68d | p95_disp_pc12 | p95_disp_68d | n_cohort | n_gen0 |
| --- | --- | --- | --- | --- | --- | --- |
| 44 | 4.867 | 9.336 | 8.710 | 9.940 | 1065 | 96 |
| 77 | 1.487 | 9.142 | 2.958 | 9.988 | 654 | 96 |
| 7755 | 5.743 | 8.832 | 8.110 | 9.377 | 1686 | 96 |
| 9354 | 1.590 | 8.882 | 2.764 | 9.523 | 1026 | 96 |

Head-to-head comparison (`results/data/t0116_comparison.csv`):

| Quantity | t0116 | t0117 | Δ |
| --- | --- | --- | --- |
| mean_disp_pc12[seed 44] | 15.026 | 4.867 | −10.159 |
| mean_disp_68d[seed 44] | 61.252 | 9.336 | −51.916 |
| mean_disp_pc12[seed 77] | 8.501 | 1.487 | −7.015 |
| mean_disp_68d[seed 77] | 59.726 | 9.142 | −50.584 |
| mean_disp_pc12[seed 7755] | 13.305 | 5.743 | −7.562 |
| mean_disp_68d[seed 7755] | 60.576 | 8.832 | −51.744 |
| mean_disp_pc12[seed 9354] | 2.370 | 1.590 | −0.779 |
| mean_disp_68d[seed 9354] | 60.073 | 8.882 | −51.191 |

Two patterns are visible:

* **Absolute scale collapses uniformly**. The 68-d displacement drops from ~60 (very tight
  range: 59.7 / 60.1 / 60.6 / 61.3) at t0116 down to ~9 (also tight: 8.8 / 8.9 / 9.1 / 9.3) at
  t0117. The 68-d displacement is computed in z-scored space, and the z-score uses a different
  standardiser at each task (t0116's standardiser was fitted on the 869-cell cohort; t0117's
  was fitted on the 4431-cell pool). The drop therefore reflects two things: (a) the PCA's
  variance basis is different (t0117 captures less variance because the pool is much more
  heterogeneous), and (b) the unfiltered pool's mean cell is much closer to gen-0 than the
  strict cohort's mean cell, because most unfiltered cells are early-generation individuals
  that NSGA-II has not yet moved far from random init.
* **Relative ordering partially preserved**. At t0116: seed 44 furthest in PC12 (15.0), then
  7755 (13.3), then 77 (8.5), then 9354 (2.4). At t0117: 7755 furthest in PC12 (5.7), then 44
  (4.9), then 9354 (1.6), then 77 (1.5). Seeds 44 and 7755 swap order (because t0117's pool
  composition gives 7755 more cells: 1686 vs t0117's 1065 for 44), but they remain the two
  furthest. Seed 9354 remains close to gen-0 in both. Seed 77 drops from clearly third
  (8.5 >> 2.4) to clearly fourth-but-tied (1.5 ≈ 1.6) — this is the largest qualitative change
  in ordering.

The PCA-with-gen0-overlay chart (`results/images/pca_with_gen0_overlay.png`) confirms visually
that t0117's gen-0 (grey x) cluster sits inside the dense centre of the unfiltered pool (o),
while at t0116 (not shown here; see `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/images/pca_with_gen0_overlay.png`)
the gen-0 cluster sat well outside the survivor scatter. This is the geometric expression of
the displacement-collapse finding: the strict-cohort cells sit on the periphery of the random-
init distribution (large displacement); the unfiltered cells are dominated by cells near gen-1
that have NOT been moved far (small displacement).

## Synthesis

The displacement-from-init result delivers two findings, one expected and one revisionist:

The expected finding is that absolute displacement collapses when the cohort filter is lifted:
the unfiltered pool includes every NSGA-II offspring at every generation, including the gen-1
random init itself and every offspring within a few mutation steps of it. The mean 68-d
displacement therefore drops from ~60 to ~9 because the unfiltered pool's centroid is no longer
the Pareto-front tip but the population centroid, which sits much closer to gen-0 by
construction. This is not a substrate-level finding but a population-composition finding.

The revisionist finding is more interesting. At t0116, the per-seed displacement ordering (seed
44 furthest, seed 9354 closest) was implicitly interpreted as "NSGA-II travelled further from
random init in seed 44 than in seed 9354". The t0117 unfiltered displacement ordering shows the
swap between 44 and 7755 in PC12 and (more importantly) the near-tie between 77 and 9354. Both
suggest the t0116 ordering reflected the strict cohort's per-seed sample composition (seed
9354's 63 cells were drawn from a region near gen-0 by chance; seed 44's 121 cells were drawn
from further), not a robust substrate-level "GA travels different distances per seed" claim.
Once the full pool is in play, the ordering depends much more on per-seed population size
(7755's 1686 cells vs 9354's 1026 cells) than on per-seed exploration distance.

For downstream tasks, the practical implication is: per-seed displacement is a sample-
composition artefact, not a substrate property. If the relevant question is "how far did
NSGA-II move from random init in each seed?", the correct measurement is the **per-generation
front advancement** (e.g., distance from gen-1 centroid to gen-300 centroid in PCA space, with
no DSI / PD filter), not the mean displacement of a quality-filtered cohort. This is documented
as a candidate follow-up suggestion.

## Limitations

* **PCA basis differs between t0116 and t0117**. The 68-d displacement number is computed in
  z-scored space using each task's own standardiser, so the t0116 value (~60) and t0117 value
  (~9) are NOT directly comparable as displacements in the same metric. The relative ordering
  within each task is well-defined; the cross-task absolute-scale comparison is only meaningful
  qualitatively (both shrink relative to gen-0 spread; t0117 shrinks more because pool is more
  random-init-like). To make absolute comparison rigorous, both tasks would need to share a
  single standardiser fitted on (e.g.) the gen-0 cells alone — this is documented as a possible
  follow-up.
* **Gen-0 is only 96 cells per seed**. The gen-0 centroid is estimated from 96 random-init
  cells per seed, which has non-trivial sampling noise. The fact that t0117 reports ~9 for
  every seed (very tight range 8.83-9.34) is partially the lower bound set by gen-0's own
  internal spread — at this scale further per-seed differentiation is hard to resolve.
* **PC1+PC2 captures only 22.9% of variance**. At t0117 the combined-PCA PC1+PC2 explains 22.9%
  of variance (vs t0116's 46.1%), so the PC12 displacement is a less informative summary than
  it was at t0116. The 68-d displacement is the more complete measure but, per above, requires
  a shared standardiser for cross-task comparison.
* **Per-seed n is uneven**. n_cohort varies from 654 (seed 77) to 1686 (seed 7755), so the
  ordering between 44 and 7755 reflects a 1065-vs-1686 sample-size difference as much as any
  substrate-level "exploration distance" difference.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen` — seed 44 NSGA-II run.
* Task: `t0112_t0106_seed77_replicate` — seed 77 replicate.
* Task: `t0114_seed7755_no_autostop` — seed 7755 replicate.
* Task: `t0115_seed9354_no_autostop` — seed 9354 replicate.
* Task: `t0116_pooled_pca_cluster_factor_dsi07_pd10` — strict-cohort head-to-head reference.
* Result data:
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/gen0_displacement.csv`,
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/t0116_comparison.csv`.
* Visualisation:
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/pca_with_gen0_overlay.png`.

[t0106]: ../../../../t0106_long_pdnd_nsga2_300gen/
[t0112]: ../../../../t0112_t0106_seed77_replicate/
[t0114]: ../../../../t0114_seed7755_no_autostop/
[t0115]: ../../../../t0115_seed9354_no_autostop/
[t0116]: ../../../../t0116_pooled_pca_cluster_factor_dsi07_pd10/
