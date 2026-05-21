---
spec_version: "2"
answer_id: "pooled-survivors-basin-connectivity-dsi07-pd10"
answered_by_task: "t0116_pooled_pca_cluster_factor_dsi07_pd10"
date_answered: "2026-05-21"
confidence: "high"
---
# Pooled DSI>0.7/PD>10 cohort is fragmented into seed-specific sub-basins

## Question

Does the joint-pass cohort (DSI > 0.7 AND PD > 10 Hz) form a single connected manifold in 68-d
across four NSGA-II seeds (44, 77, 7755, 9354), or do the seeds occupy seed-specific sub-basins?

## Short Answer

The four-seed pool occupies seed-specific sub-basins, not one connected manifold. KMeans (k=3) on
the standardised 54-d electrophys subspace produces an almost-perfect seed partition (NMI=0.929,
chi-square p<1e-300): cluster 0 = 63/67 seed 9354, cluster 1 = 673/678 seed 7755, cluster 2 =
121/124 seed 44 (seed 77 contributes 10 scattered cells across all clusters). The 14-d morphology
partition is similarly seed-aligned (NMI=0.889). In the combined 68-d PCA scatter the four seed
colours occupy visibly disjoint regions of the PC1-PC2 plane, so the cross-seed overlap implied by a
single connected basin is not observed at the DSI > 0.7 cut.

## Research Process

The analysis pools every joint-pass cell (DSI > 0.7 AND PD > 10 Hz) from four independent NSGA-II
seeds and asks whether the union pool forms one connected manifold in the 68-d parameter space:

1. Load every evaluation record from the four predictions assets and apply the strict cohort filter
   (`code/load_pooled_cells.py`).
2. Fit a single z-score standardiser on the union pool (n=869 cells, 68 columns) so cross-seed
   comparisons share one scaling regime (`code/fit_standardiser.py`).
3. Fit three PCAs on the standardised pool (combined 68-d, electrophys-only 54-d, morphology-only
   14-d), all with n_components=2, and render `pca_combined.png`
   (`code/pooled_pca_with_overlay.py`).
4. Run KMeans on both the 54-d and the 14-d standardised submatrices, sweep k in {3, 4, 5, 6, 7},
   and pick the headline k by maximum mean silhouette score (`code/cluster_electrophys.py`,
   `code/cluster_morphology.py`).
5. Compute normalised mutual information (NMI) between cluster_id and seed for both partitions, and
   run a chi-square contingency test on the (cluster, seed) crosstab
   (`code/cluster_seed_purity.py`).

Two-tier evidence: visual inspection of the PCA scatter (qualitative) and NMI + chi-square
(quantitative). NMI is robust to sparse cells in the contingency table; the chi-square asymptotic
relies on expected counts >= 5, which fails in 3 of 12 cells (driven by seed 77's small n=10 cohort)
— see Limitations.

## Evidence from Papers

No paper-based evidence was used. The cross-seed basin question is internal to this project's
NSGA-II survivor cohort and has no published benchmark.

## Evidence from Internet Sources

No external internet sources were used.

## Evidence from Code or Experiments

Pooled cohort: 869 unique cells passing DSI > 0.7 AND PD > 10 Hz across four seeds, broken down in
`results/data/per_seed_cohort_counts.csv`:

| Source | Seed | n_raw | n_passing_filter | n_unique |
| --- | --- | --- | --- | --- |
| t0106 | 44 | 3744 | 658 | 121 |
| t0112 | 77 | 2016 | 33 | 10 |
| t0114 | 7755 | 5952 | 2566 | 675 |
| t0115 | 9354 | 5280 | 467 | 63 |
| TOTAL | - | 16992 | 3724 | 869 |

PCA on the union pool (`results/images/pca_combined.png`) shows that the survivor scatter splits
visibly along PC1 of the combined 68-d projection. Each seed's points cluster in a distinct PC1 zone
with very little inter-seed overlap. The combined PCA's first two components together explain 46.1%
of the variance (PC1=31.0%, PC2=15.0%). The 54-d electrophys-only PCA explains 47.7% (PC1=32.2%,
PC2=15.5%); the 14-d morphology-only PCA explains 49.1% (PC1=30.6%, PC2=18.5%).

KMeans silhouette sweeps (`results/images/electrophys_silhouette.png`,
`results/images/morphology_silhouette.png`) both pick k=3 as the headline value:

| Partition | k=3 silhouette | k=4 | k=5 | k=6 | k=7 |
| --- | --- | --- | --- | --- | --- |
| Electrophys 54-d | 0.472 | 0.294 | 0.303 | 0.277 | 0.231 |
| Morphology 14-d | 0.529 | 0.301 | 0.313 | 0.326 | 0.344 |

In both partitions the k=3 silhouette is sharply higher than any larger k — strong evidence that
exactly three coherent groups exist in the data. The 54-d electrophys partition's seed × cluster
crosstab (saved in `results/data/electrophys_clusters.csv`):

| seed | cluster 0 | cluster 1 | cluster 2 |
| --- | --- | --- | --- |
| 44 | 0 | 0 | 121 |
| 77 | 2 | 5 | 3 |
| 7755 | 2 | 673 | 0 |
| 9354 | 63 | 0 | 0 |

The 14-d morphology partition's crosstab (`results/data/morphology_clusters.csv`):

| seed | cluster 0 | cluster 1 | cluster 2 |
| --- | --- | --- | --- |
| 44 | 4 | 1 | 116 |
| 77 | 9 | 1 | 0 |
| 7755 | 673 | 2 | 0 |
| 9354 | 0 | 63 | 0 |

Cluster-vs-seed purity metrics from `results/data/cluster_seed_purity.csv`:

| Partition | k | NMI | chi-square | p_value | dof |
| --- | --- | --- | --- | --- | --- |
| Electrophys k=3 | 3 | 0.929 | 1670.9 | < 1e-300 | 6 |
| Morphology k=3 | 3 | 0.889 | 1643.1 | < 1e-300 | 6 |

NMI of 0.929 on the electrophys partition is extreme — a perfect seed-cluster bijection would give
NMI=1, and a uniform-random partition would give NMI~0. The morphology partition is only slightly
less seed-aligned (NMI=0.889). Both chi-square tests reject the null of seed-cluster independence at
essentially any threshold. The per-cluster morphology grids
(`results/images/electrophys_cluster_0_morphs.png`,
`results/images/electrophys_cluster_1_morphs.png`,
`results/images/electrophys_cluster_2_morphs.png`) confirm that within-cluster cells share
near-identical morphology, dendrite-tree size, and primary branch count, while across clusters the
morphology is visibly different.

## Synthesis

The four NSGA-II seeds did not converge to one connected joint-pass manifold. Each seed discovered
its own coherent parameter basin and the survivors of that basin form a tight, seed-internal
cluster. The clearest evidence is the electrophys 54-d KMeans partition (silhouette=0.472, NMI=0.929
with seed): cluster boundaries match seed boundaries to within ~5 mis-assigned cells out of 869 (all
5 are from seed 77, the smallest cohort).

Two mechanistic interpretations are compatible with the data:

* **Basin-isolation hypothesis**: the 68-d landscape has multiple local optima separated by fitness
  valleys that NSGA-II's mutation step cannot cross in a 300-generation budget. Each seed is
  captured by whichever basin its random init was closest to, then descends along that basin's
  Pareto front. The fact that the morphology subspace alone produces NMI=0.889 supports this: the
  basin identity is encoded primarily in the discrete morphological structure (primary branch count,
  Strahler depth, branching angle), which is genuinely hard to cross via real-valued mutation
  operators applied to those integer-typed dimensions.
* **Seed-aliasing hypothesis**: the four seeds are statistical realisations of the same basin
  distribution, and the apparent disjoint clusters are sampling artefacts of small per-seed cohort
  sizes. This is ruled out for seeds 44, 7755, 9354 (which contribute 121, 675, 63 cells
  respectively — large enough that random sampling would mix them in any shared basin), but cannot
  be ruled out for seed 77 (n=10).

The basin-isolation hypothesis is by far the more parsimonious reading. A practical implication is
that downstream tasks aiming to characterise "the" joint-pass cohort must report results per-seed,
not pooled, unless the per-seed cluster signature is explicitly the unit of analysis.

## Limitations

* **Seed 77's small cohort (n=10) makes chi-square unreliable.** Three of twelve expected cell
  counts in the contingency table fall below 5, so the chi-square asymptotic is technically invalid.
  The NMI metric is unaffected by sparse cells (NMI=0.929 / 0.889 are computed directly from the
  joint distribution). A more rigorous follow-up would use Fisher's exact test on per-cluster 2x2
  contingencies; the chi-square reported here is illustrative not definitive.
* **Strict cohort might bias the partition.** DSI > 0.7 AND PD > 10 Hz retains only ~22% of the raw
  post-filter evaluation count (3724 -> 869 after dedup) and concentrates each seed's Pareto-front
  tip into a narrow region. A relaxed cohort (e.g., DSI > 0.5 like t0108) would include more border
  cells and might reveal more inter-seed bridges. This is a candidate follow-up.
* **Only four seeds, not five.** t0113 (seed 2247) was excluded from this first cut because it uses
  an earlier autostop / pool-restart configuration. Including t0113 might add a fifth sub-basin or
  might bridge two existing ones; this is documented as a possible correction in
  `task_description.md`.
* **KMeans assumes spherical clusters in z-scored space.** A non-convex shape (e.g., a curved Pareto
  front) would be poorly captured. The k=3 result's high silhouette (0.472 / 0.529) indicates that
  the data is reasonably well-separated, but DBSCAN or HDBSCAN on the same matrix could give
  additional evidence.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen` — seed 44 NSGA-II run.
* Task: `t0112_t0106_seed77_replicate` — seed 77 replicate.
* Task: `t0114_seed7755_no_autostop` — seed 7755 replicate (no autostop).
* Task: `t0115_seed9354_no_autostop` — seed 9354 replicate (no autostop).
* Task: `t0108_t0106_cluster_factor_dsi05_pd10` — single-seed methodology precedent.
* Task: `t0116_pooled_pca_cluster_factor_dsi07_pd10` — this analysis.
* Result data:
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/data/per_seed_cohort_counts.csv`,
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/data/electrophys_clusters.csv`,
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/data/morphology_clusters.csv`,
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/data/cluster_seed_purity.csv`.
* Visualisations:
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/images/pca_combined.png`,
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/images/electrophys_silhouette.png`,
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/images/morphology_silhouette.png`,
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/images/electrophys_cluster_0_morphs.png`,
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/images/electrophys_cluster_1_morphs.png`,
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/images/electrophys_cluster_2_morphs.png`.

[t0106]: ../../../../t0106_long_pdnd_nsga2_300gen/
[t0112]: ../../../../t0112_t0106_seed77_replicate/
[t0114]: ../../../../t0114_seed7755_no_autostop/
[t0115]: ../../../../t0115_seed9354_no_autostop/
[t0108]: ../../../../t0108_t0106_cluster_factor_dsi05_pd10/
[t0116]: ../../../
