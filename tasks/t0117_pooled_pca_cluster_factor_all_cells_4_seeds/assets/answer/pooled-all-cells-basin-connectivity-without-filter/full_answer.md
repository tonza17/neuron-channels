---
spec_version: "2"
answer_id: "pooled-all-cells-basin-connectivity-without-filter"
answered_by_task: "t0117_pooled_pca_cluster_factor_all_cells_4_seeds"
date_answered: "2026-05-22"
confidence: "high"
---
# Unfiltered 4-seed pool partially reconnects across seeds (NMI drops from 0.93 to 0.56)

## Question

Does the unfiltered pool (every NSGA-II evaluation, no DSI/PD cohort filter) form a single
connected manifold across seeds 44, 77, 7755, and 9354, or does the seed-specific basin pattern
observed at the strict cohort (t0116) persist when low-DSI / low-PD cells are also admitted?

## Short Answer

The seed-specific basin pattern partially dissolves once the cohort filter is removed: the pool
reconnects across seeds but does not form a single connected manifold. Electrophys KMeans NMI vs
seed drops from 0.929 (t0116, strict cohort) to 0.562 (t0117, no filter, n=4431 cells, k=4), and
morphology NMI drops from 0.889 to 0.313 — the morphology subspace shows much stronger
reconnection than the electrophys subspace. Even at the unfiltered pool both partitions remain
significantly seed-aligned (chi-square p<<0.001), so seed effects are detectable but no longer
dominant.

## Research Process

The pipeline mirrors t0116 verbatim with one change: the `dsi_vector_sum > 0.7 AND pd_rate_hz >
10.0` cohort filter is removed from `code/load_pooled_cells.py`. Every other module
(`code/cluster_helpers.py`, `code/factor_analysis.py`, `code/cluster_electrophys.py`,
`code/cluster_morphology.py`, `code/pooled_pca_with_overlay.py`, `code/morphology_rendering.py`,
`code/cluster_seed_purity.py`) is copied into `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/`
verbatim with namespace updates only — per the cross-task import rule.

1. Load every evaluation record from the four NSGA-II predictions assets (t0106 seed 44, t0112
   seed 77, t0114 seed 7755, t0115 seed 9354) with NO DSI / PD filter
   (`code/load_pooled_cells.py`).
2. Dedup by the 68-d vector rounded to 6 decimals (project convention from t0108 / t0116).
3. Fit a single union-pool z-score standardiser on the 4431-cell pool
   (`code/fit_standardiser.py`).
4. Fit three PCAs on the standardised pool (combined 68-d, electrophys-only 54-d,
   morphology-only 14-d), render `results/images/pca_combined.png`
   (`code/pooled_pca_with_overlay.py`).
5. Run KMeans on both 54-d and 14-d submatrices with `k ∈ {3, 4, 5, 6, 7}`, pick the headline k
   by maximum mean silhouette (`code/cluster_electrophys.py`, `code/cluster_morphology.py`).
6. Compute normalised mutual information (NMI) between cluster id and seed for both partitions,
   plus chi-square contingency test on the cluster × seed crosstab
   (`code/cluster_seed_purity.py`).
7. Produce the head-to-head comparison table by reading t0116's published numbers directly
   (`results/data/t0116_comparison.csv` via `code/methodology_and_comparison.py`).

Two-tier evidence: (a) visual inspection of the PCA scatter (qualitative) and (b) NMI +
chi-square (quantitative). NMI is robust to sparse cells in the contingency table; chi-square's
asymptotic relies on expected counts ≥ 5, which holds in every cell of t0117's larger pool (0/16
electrophys cells below 5, 0/20 morphology cells below 5 — see
`results/data/cluster_seed_purity.csv`).

## Evidence from Papers

No paper-based evidence was used. The basin-connectivity question is internal to this project's
NSGA-II survivor pool and has no published benchmark.

## Evidence from Internet Sources

No external internet sources were used.

## Evidence from Code or Experiments

Pool composition (`results/data/per_seed_pool_counts.csv`):

| Source | Seed | n_raw | n_unique |
| --- | --- | --- | --- |
| t0106 | 44 | 3744 | 1065 |
| t0112 | 77 | 2016 | 654 |
| t0114 | 7755 | 5952 | 1686 |
| t0115 | 9354 | 5280 | 1026 |
| TOTAL | - | 16992 | 4431 |

PCA variance explained on the unfiltered pool (`results/images/pca_combined.png`) is sharply
lower than at the strict cohort:

| Subspace | t0116 PC1 (%) | t0116 PC2 (%) | t0117 PC1 (%) | t0117 PC2 (%) |
| --- | --- | --- | --- | --- |
| Combined 68-d | 31.0 | 15.0 | 14.7 | 8.3 |
| Electrophys 54-d | 32.2 | 15.5 | 15.9 | 8.5 |
| Morphology 14-d | 30.6 | 18.5 | 16.0 | 13.3 |

The unfiltered pool has roughly half the PC1+PC2 variance fraction of the strict cohort because
admitting the low-quality cells (most NSGA-II offspring at any given generation) re-introduces
the full random-init dispersion that the strict cohort had eliminated.

KMeans silhouette sweep on the 54-d electrophys subspace
(`results/images/electrophys_silhouette.png`, `results/data/electrophys_clusters.csv`):

| k | t0117 silhouette | t0116 silhouette |
| --- | --- | --- |
| 3 | 0.145 | 0.472 |
| 4 (t0117 headline) | 0.158 | 0.294 |
| 5 | 0.105 | 0.303 |
| 6 | 0.112 | 0.277 |
| 7 | 0.115 | 0.231 |

At t0117 the chosen k is 4 with silhouette 0.158 — three to four times lower than t0116's k=3,
silhouette=0.472. The electrophys × seed crosstab at t0117 k=4
(`results/data/electrophys_clusters.csv`):

| seed | cluster 0 | cluster 1 | cluster 2 | cluster 3 |
| --- | --- | --- | --- | --- |
| 44 | 445 | 584 | 0 | 36 |
| 77 | 633 | 0 | 0 | 21 |
| 7755 | 313 | 0 | 1340 | 33 |
| 9354 | 273 | 1 | 0 | 752 |

Cluster 0 mixes all four seeds (445/633/313/273) — this is the basin-reconnection signal absent
in t0116. Cluster 2 still captures 1340 of 1686 seed-7755 cells, and cluster 3 still captures
752 of 1026 seed-9354 cells, so seed isolation is partial rather than complete.

KMeans silhouette sweep on the 14-d morphology subspace
(`results/images/morphology_silhouette.png`, `results/data/morphology_clusters.csv`):

| k | t0117 silhouette | t0116 silhouette |
| --- | --- | --- |
| 3 | 0.144 | 0.529 |
| 4 | 0.150 | 0.301 |
| 5 (t0117 headline) | 0.153 | 0.313 |
| 6 | 0.099 | 0.326 |
| 7 | 0.106 | 0.344 |

t0117 morphology k=5 mixes seeds heavily — every cluster contains contributions from all four
seeds in non-trivial proportions, in contrast to t0116's near-bijective seed-to-cluster mapping.

Cluster-vs-seed purity head-to-head (`results/data/cluster_seed_purity.csv`,
`results/data/t0116_comparison.csv`):

| Partition | t0116 NMI | t0117 NMI | Δ |
| --- | --- | --- | --- |
| Electrophys (k chosen) | 0.929 (k=3) | 0.562 (k=4) | −0.367 |
| Morphology (k chosen) | 0.889 (k=3) | 0.313 (k=5) | −0.576 |

Both chi-square contingency tests at t0117 still reject the null of seed-cluster independence
(p < 1e−300 in both partitions), but with much lower NMI than t0116. The morphology NMI drop
(0.889 → 0.313) is larger than the electrophys NMI drop (0.929 → 0.562), implying that the
seed-specific morphology basins observed in t0116 were primarily a strict-cohort artefact — at
the unfiltered pool the morphology subspace is dominated by the random init distribution which
is common across seeds, not by per-seed Pareto-front structure.

The per-cluster morphology grids (`results/images/electrophys_cluster_0_morphs.png` through
`electrophys_cluster_3_morphs.png`) confirm the cross-seed mixing in cluster 0: representatives
are drawn from all four seeds, in contrast to t0116 where each cluster's top-15 came from a
single seed.

## Synthesis

The unfiltered pool partially reconnects the cross-seed manifold but does not erase the
seed-specific signal entirely. The NMI numbers tell the full story: in the strict cohort
(t0116), cluster boundaries match seed boundaries to within ~5 of 869 cells (NMI=0.929 / 0.889);
in the unfiltered pool (t0117), 4431 cells distribute across 4 (electrophys) or 5 (morphology)
clusters with NMI=0.562 / 0.313. The morphology subspace reconnects much more strongly than the
electrophys subspace, which is consistent with the t0116 basin-isolation reading: the basin
identity was always encoded primarily in discrete morphological structure (primary branch
count, Strahler depth, branching angle), and admitting the gen-1 random-init population
re-injects the shared morphology distribution that all four seeds drew from at t=0.

This is essentially a confirmation of t0116's basin-isolation hypothesis with an important
refinement: the high NMI at the strict cohort was driven by the cohort filter itself, which
selectively keeps the late-generation Pareto-front tips and discards the early-generation cells
that occupy the shared random-init region. Once the filter is lifted, the late-generation
basins remain detectable as a residual signal (NMI > 0.3 in both partitions, p < 1e−300), but
they no longer dominate the cluster structure.

For downstream tasks, the practical implication is symmetric to t0116's: if the analysis is
about NSGA-II's high-quality Pareto-front structure, per-seed reporting is mandatory (the
strict cohort's NMI=0.929 makes seed a near-perfect proxy for cluster); if the analysis is
about substrate-level parameter regularities (factor structure, joint DSI-PD relationships, see
Q2), the unfiltered pool is the correct comparator because it preserves the random-init
distribution that the strict cohort genuinely erases.

## Limitations

* **Dedup ratio differs from t0116**. The unfiltered pool's dedup ratio is 4431/16992 = 26%,
  compared to t0116's filter-then-dedup ratio of 869/3724 = 23%. Most of the t0117 unique cells
  are from intermediate NSGA-II generations (not Pareto-front tips), which differ in vector
  composition from the strict-cohort cells. The reported NMI drops therefore conflate two
  effects: (a) genuine basin reconnection, and (b) the population-distribution shift away from
  Pareto-front tips. Disentangling these would require a graded-DSI analysis (e.g., relaxed
  thresholds like the suggested S-0116-02 DSI > 0.5 follow-up).
* **k differs across analyses**. t0116 picked k=3 in both partitions; t0117 picks k=4
  (electrophys) and k=5 (morphology). Comparing NMI at different k values is well-defined (NMI
  is normalised), but the cluster identities are no longer one-to-one comparable.
* **Only four seeds**. t0113 (seed 2247) remains excluded for the same reason as t0116 — its
  earlier autostop / pool-restart configuration would conflate the cohort-filter question with
  a seed-coverage question. Including t0113 might further reduce NMI or add a new sub-basin.
* **KMeans assumes spherical clusters**. The same assumption applies at t0117 as at t0116; the
  much lower silhouette (0.158 / 0.153 vs t0116's 0.472 / 0.529) indicates that the unfiltered
  pool's cluster structure is genuinely weaker, not that KMeans is mismatched to the geometry.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen` — seed 44 NSGA-II run.
* Task: `t0112_t0106_seed77_replicate` — seed 77 replicate.
* Task: `t0114_seed7755_no_autostop` — seed 7755 replicate.
* Task: `t0115_seed9354_no_autostop` — seed 9354 replicate.
* Task: `t0108_t0106_cluster_factor_dsi05_pd10` — single-seed methodology precedent.
* Task: `t0116_pooled_pca_cluster_factor_dsi07_pd10` — strict-cohort head-to-head reference.
* Result data:
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/per_seed_pool_counts.csv`,
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/electrophys_clusters.csv`,
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/morphology_clusters.csv`,
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/cluster_seed_purity.csv`,
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/t0116_comparison.csv`.
* Visualisations:
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/pca_combined.png`,
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/electrophys_silhouette.png`,
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/morphology_silhouette.png`,
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/electrophys_cluster_0_morphs.png`,
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/electrophys_cluster_1_morphs.png`,
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/electrophys_cluster_2_morphs.png`,
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/electrophys_cluster_3_morphs.png`.

[t0106]: ../../../../t0106_long_pdnd_nsga2_300gen/
[t0112]: ../../../../t0112_t0106_seed77_replicate/
[t0114]: ../../../../t0114_seed7755_no_autostop/
[t0115]: ../../../../t0115_seed9354_no_autostop/
[t0108]: ../../../../t0108_t0106_cluster_factor_dsi05_pd10/
[t0116]: ../../../../t0116_pooled_pca_cluster_factor_dsi07_pd10/
